from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session, jsonify
import os
import pandas as pd
from datetime import datetime, timedelta
import io
import tempfile
import csv
import re
import zipfile
import hashlib
import secrets
from rapidfuzz import fuzz
from werkzeug.utils import secure_filename

# Import the core processing functions from the new module
from attendance_processing import (
    process_sessions_for_file, parse_datetime, write_excel
)

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = 'your_secret_key_here'  # Change this in production

# Make get_remaining_time available to templates
@app.context_processor
def inject_remaining_time():
    return dict(get_remaining_time=get_remaining_time)

# Directory for temporary files
TEMP_DIR = tempfile.gettempdir()

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# In-memory user storage (in production, use a database)
users = {
    'superadmin@attendancify.com': {
        'password_hash': hashlib.sha256('admin'.encode()).hexdigest(),
        'role': 'superadmin',
        'created_at': datetime.now(),
        'expires_at': None,  # Permanent account
        'must_change_password': True,  # Force password change on first login
        'password_plain': 'admin'  # Store plain password for superadmin viewing (as requested)
    }
}

# ----------- Authentication Functions -----------
def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password_hash, provided_password):
    """Verify a stored password hash against one provided by user"""
    return stored_password_hash == hashlib.sha256(provided_password.encode()).hexdigest()

def is_logged_in():
    """Check if user is logged in"""
    return 'user_id' in session and 'token' in session

def is_admin():
    """Check if logged in user is admin"""
    if not is_logged_in():
        return False
    user = users.get(session['user_id'])
    return user and user.get('role') in ['admin', 'superadmin']

def is_superadmin():
    """Check if logged in user is superadmin"""
    if not is_logged_in():
        return False
    user = users.get(session['user_id'])
    return user and user.get('role') == 'superadmin'

def check_token_validity():
    """Check if user's token is still valid"""
    if not is_logged_in():
        return False
    
    user = users.get(session['user_id'])
    if not user:
        return False
    
    # Check if account has expired
    if user.get('expires_at') and datetime.now() > user['expires_at']:
        return False
    
    return True

def get_remaining_time(user_id):
    """Get remaining time for a user account"""
    user = users.get(user_id)
    if not user or not user.get('expires_at'):
        return None
    
    now = datetime.now()
    expires_at = user['expires_at']
    
    if expires_at <= now:
        return "Expired"
    
    remaining = expires_at - now
    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if days > 0:
        return f"{days} days, {hours} hours"
    elif hours > 0:
        return f"{hours} hours, {minutes} minutes"
    else:
        return f"{minutes} minutes"

# ----------- Authentication Decorator -----------
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in() or not check_token_validity():
            flash('Please log in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in() or not is_admin() or not check_token_validity():
            flash('Access denied. Admin privileges required.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def superadmin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in() or not is_superadmin() or not check_token_validity():
            flash('Access denied. Superadmin privileges required.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ----------- Authentication Routes -----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = users.get(email)
        if user and verify_password(user['password_hash'], password):
            # Check if account has expired
            if user.get('expires_at') and datetime.now() > user['expires_at']:
                flash('Account has expired.')
                return redirect(url_for('login'))
            
            # Generate a session token
            token = secrets.token_hex(16)
            
            # Store user info in session
            session['user_id'] = email
            session['token'] = token
            session['role'] = user.get('role', 'user')
            
            # Check if password change is required
            if user.get('must_change_password', False):
                session['force_password_change'] = True
                flash('You must change your password before continuing.', 'warning')
                return redirect(url_for('force_change_password'))
            
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')
    
    return render_template('login_advanced.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/force_change_password', methods=['GET', 'POST'])
@login_required
def force_change_password():
    """Force password change on first login"""
    if not session.get('force_password_change', False):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        user = users.get(session['user_id'])
        
        # Verify current password
        if not user or not verify_password(user['password_hash'], current_password):
            flash('Current password is incorrect.', 'error')
            return render_template('force_change_password.html')
        
        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return render_template('force_change_password.html')
        
        # Check password strength (minimum 6 characters)
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('force_change_password.html')
        
        # Update password
        user['password_hash'] = hash_password(new_password)
        user['must_change_password'] = False
        
        # Update plain password for superadmin viewing (as requested)
        if session.get('role') == 'superadmin' or user.get('role') == 'superadmin':
            user['password_plain'] = new_password
        else:
            user['password_plain'] = new_password
        
        # Remove force change flag from session
        session.pop('force_password_change', None)
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('force_change_password.html')

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        user = users.get(session['user_id'])
        
        # Verify current password
        if not user or not verify_password(user['password_hash'], current_password):
            flash('Current password is incorrect.')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Current password is incorrect.'}), 400
            return render_template('change_password.html')
        
        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match.')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'New passwords do not match.'}), 400
        
        # Update password
        user['password_hash'] = hash_password(new_password)
        flash('Password changed successfully.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Password changed successfully.'})
        return redirect(url_for('index'))
    
    return render_template('change_password.html')

@app.route('/admin/create_user', methods=['GET', 'POST'])
@admin_required
def create_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'user')
        expires_at = request.form.get('expires_at')
        
        # Superadmin can create admins and users, admins can only create users
        current_user_role = session.get('role', 'user')
        if current_user_role == 'admin' and role == 'admin':
            flash('Admins cannot create other admins. Only superadmins can create admins.')
            return redirect(url_for('admin_panel'))
        
        if email in users:
            flash('User already exists.')
        else:
            # Set default expiration for normal users (15 days)
            if role == 'user' and not expires_at:
                expires_at = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%dT%H:%M')
            
            user_data = {
                'password_hash': hash_password(password),
                'role': role,
                'created_at': datetime.now(),
                'expires_at': datetime.strptime(expires_at, '%Y-%m-%dT%H:%M') if expires_at else None,
                'must_change_password': True,  # Force password change on first login
                'password_plain': password  # Store plain password for superadmin viewing
            }
            users[email] = user_data
            flash('User created successfully. They will be required to change password on first login.')
            return redirect(url_for('admin_panel'))
    
    return render_template('create_user.html', show_navigation=True)

@app.route('/admin')
@admin_required
def admin_panel():
    # Get list of all users except the superadmin
    user_list = []
    for email, user_data in users.items():
        if email != 'satendra@aiadmin.com':  # Don't show the superadmin
            user_list.append({
                'email': email,
                'role': user_data.get('role', 'user'),
                'created_at': user_data.get('created_at'),
                'expires_at': user_data.get('expires_at')
            })
    
    return render_template('admin_panel.html', users=user_list, show_navigation=True)

@app.route('/admin/edit_user/<user_id>', methods=['GET', 'POST'])
@superadmin_required
def edit_user(user_id):
    user = users.get(user_id)
    if not user:
        flash('User not found.')
        return redirect(url_for('admin_panel'))
    
    if request.method == 'POST':
        # Only superadmin can edit users
        if session.get('role') != 'superadmin':
            flash('Only superadmins can edit users.')
            return redirect(url_for('admin_panel'))
        
        # Update user data
        if 'role' in request.form:
            user['role'] = request.form['role']
        
        if 'expires_at' in request.form:
            expires_at = request.form['expires_at']
            user['expires_at'] = datetime.strptime(expires_at, '%Y-%m-%dT%H:%M') if expires_at else None
        
        # Handle email change
        if 'email' in request.form and request.form['email'] != user_id:
            new_email = request.form['email']
            if new_email in users:
                flash('Email already exists.')
                return render_template('edit_user.html', user=user, user_id=user_id, show_navigation=True)
            # Update the users dictionary
            users[new_email] = user
            del users[user_id]
            flash('User email updated successfully.')
            return redirect(url_for('edit_user', user_id=new_email))
        
        flash('User updated successfully.')
        return redirect(url_for('admin_panel'))
    
    return render_template('edit_user.html', user=user, user_id=user_id, show_navigation=True)

@app.route('/admin/view_password/<user_id>')
@superadmin_required
def view_user_password(user_id):
    """Only superadmin can view passwords"""
    if session.get('role') != 'superadmin':
        flash('Access denied. Only superadmin can view passwords.')
        return redirect(url_for('admin_panel'))
    
    user = users.get(user_id)
    if not user:
        flash('User not found.')
        return redirect(url_for('admin_panel'))
    
    # Return the plain password stored for superadmin viewing
    password = user.get('password_plain', '[Not available - password was hashed before update]')
    
    return jsonify({'success': True, 'email': user_id, 'password': password})

@app.route('/admin/change_password/<user_id>', methods=['POST'])
@admin_required
def admin_change_password(user_id):
    # Only superadmin and admin can change passwords
    if session.get('role') not in ['admin', 'superadmin']:
        flash('Access denied.')
        return redirect(url_for('admin_panel'))
    
    user = users.get(user_id)
    if not user:
        flash('User not found.')
        return redirect(url_for('admin_panel'))
    
    new_password = request.form.get('new_password')
    if not new_password:
        flash('New password is required.')
        return redirect(url_for('admin_panel'))
    
    # Update password
    user['password_hash'] = hash_password(new_password)
    flash(f'Password for {user_id} changed successfully.')
    return redirect(url_for('admin_panel'))

# ----------- Name Normalization -----------
def normalize_name(name: str) -> str:
    if not isinstance(name, str):
        name = str(name)
    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip().lower()

# ----------- Raw Excel Generator Functions -----------
SHEET_NAME = "Attendance"

def extract_raw_from_excel(xl_path):
    # Always extract sheet named "Attendance"
    xl = pd.ExcelFile(xl_path)
    if SHEET_NAME not in xl.sheet_names:
        raise ValueError(f"Sheet '{SHEET_NAME}' not found in the file.")
    df = xl.parse(SHEET_NAME)
    name_col = next((c for c in df.columns if str(c).strip().lower() in ("name", "participant name")), None)
    if not name_col:
        raise ValueError("No 'Name' column found.")
    session_cols = [c for c in df.columns if str(df[c].dropna().unique()).strip("[]").replace("'", "").lower() in ("p, a", "p", "a")]
    # Fallback for cases session columns have headers with "Session" or contain P/A markers
    if not session_cols:
        session_cols = [c for c in df.columns if "session" in str(c).lower()]
    out = df[[name_col]+session_cols].copy()
    out.columns = ["Name"] + [str(c) for c in session_cols]
    # Only keep "P"/"A", replace anything else with "N/A"
    for col in session_cols:
        out[col] = out[col].apply(lambda x: x if str(x).strip().upper() in ("P","A") else "N/A")
    return out

# ----------- Attendance Matching Functions -----------
def read_raw_file(raw_path: str) -> pd.DataFrame:
    df = pd.read_csv(raw_path) if raw_path.lower().endswith(".csv") else pd.read_excel(raw_path)
    df.columns = [str(c).strip() for c in df.columns]
    name_col = next((c for c in df.columns if c.lower() in ("name", "participant name")), None)
    if name_col is None:
        raise ValueError("Raw file needs a 'Name' column.")
    session_cols = [c for c in df.columns if c != name_col]
    if not session_cols:
        raise ValueError("Raw file contains no session/status columns.")
    def norm(x): return x if str(x) in ("P", "A") else "N/A"
    for col in session_cols:
        df[col] = df[col].apply(norm)
    out = df[[name_col] + session_cols].copy()
    out.columns = ["Name"] + session_cols
    return out

def postprocess_attendance(df, session_cols):
    # Replace P→present, A→absent (case-insensitive), but only in session columns
    for col in session_cols:
        df[col] = df[col].replace({"P": "present", "A": "absent", "p": "present", "a": "absent"})
    return df

def match_and_write(master_file: str, raw_file: str, out_fmt: str = "xlsx") -> str:
    mdf = pd.read_csv(master_file) if master_file.lower().endswith(".csv") else pd.read_excel(master_file)
    email_col = next((c for c in mdf.columns if str(c).strip().lower() in ("email", "email_id")), None)
    name_col = next((c for c in mdf.columns if str(c).strip().lower() in ("participant name", "name")), None)
    if email_col is None or name_col is None:
        raise ValueError("Master file must have 'Email' and 'Participant Name' columns.")
    mdf = mdf[[email_col, name_col]].copy()
    mdf.columns = ["Email", "Participant Name"]
    rdf = read_raw_file(raw_file)
    session_cols = list(rdf.columns[1:])
    raw_norm_names = [normalize_name(n) for n in list(rdf["Name"])]
    matched_df = mdf.copy()
    for col in session_cols:
        matched_df[col] = "N/A"
    threshold = 85
    matched_indices = set()
    for idx, row in matched_df.iterrows():
        master_name = normalize_name(str(row["Participant Name"]))
        best_score, best_j = -1, None
        for j, raw_norm in enumerate(raw_norm_names):
            score = fuzz.token_set_ratio(master_name, raw_norm)
            if score > best_score:
                best_score = score
                best_j = j
        if best_score >= threshold:
            raw_row = rdf.iloc[best_j]
            for col in session_cols:
                matched_df.at[idx, col] = raw_row[col]
            matched_indices.add(best_j)
    unmatched_df = rdf.iloc[[i for i in range(len(rdf)) if i not in matched_indices]].copy()
    if not unmatched_df.empty:
        unmatched_df.rename(columns={"Name": "Raw Name (not found in Master)"}, inplace=True)
    # ---- Here: replace P/A
    matched_df = postprocess_attendance(matched_df, session_cols)
    if not unmatched_df.empty:
        unmatched_df = postprocess_attendance(unmatched_df, session_cols)
    out_dir = os.path.dirname(master_file)
    mbase = os.path.splitext(os.path.basename(master_file))[0]
    rbase = os.path.splitext(os.path.basename(raw_file))[0]
    if out_fmt == "xlsx":
        out_path = os.path.join(out_dir, f"{mbase}_matched_with_{rbase}_attendance.xlsx")
        with pd.ExcelWriter(out_path, engine="openpyxl") as w:
            matched_df.to_excel(w, index=False, sheet_name="Matched")
            if not unmatched_df.empty:
                unmatched_df.to_excel(w, index=False, sheet_name="Unmatched Raw")
            pd.DataFrame([], columns=["email_id", "attendance(absent/present/leave)"]).to_excel(w, index=False, sheet_name="Summary")
        return out_path
    prefix = os.path.join(out_dir, f"{mbase}_matched_with_{rbase}_")
    matched_df.to_csv(prefix + "matched.csv", index=False)
    if not unmatched_df.empty:
        unmatched_df.to_csv(prefix + "unmatched.csv", index=False)
    pd.DataFrame([], columns=["email_id", "attendance(absent/present/leave)"]).to_csv(prefix + "summary.csv", index=False)
    return prefix + "matched.csv"

# ----------- Routes -----------
@app.route('/')
def index():
    # Allow public access to the homepage
    return render_template('comprehensive_index.html', show_navigation=True)

# ----------- Attendance Generator Routes -----------
@app.route('/attendance_generator')
def attendance_generator():
    # Allow public viewing of the tool UI
    return render_template('attendance_generator.html', show_navigation=True)

@app.route('/upload_attendance', methods=['POST'])
@login_required
def upload_attendance_file():
    # Get the mode (single or multiple)
    mode = request.form.get('mode', 'single')
    
    if mode == 'single':
        if 'csv_file' not in request.files:
            flash('No file selected')
            return redirect(url_for('attendance_generator'))
        
        file = request.files['csv_file']
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('attendance_generator'))
        
        if file:
            # Save file temporarily
            filename = secure_filename(file.filename)
            file_path = os.path.join(TEMP_DIR, filename)
            file.save(file_path)
            
            # Store file info in session
            session['file_path'] = file_path
            session['filename'] = filename
            session['mode'] = 'single'
            
            return redirect(url_for('configure_attendance_sessions'))
    else:  # multiple mode
        files = request.files.getlist('csv_files')
        if not files or not any(f.filename for f in files):
            flash('No files selected')
            return redirect(url_for('attendance_generator'))
        
        # Save all files
        file_paths = []
        file_names = []
        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(TEMP_DIR, filename)
                file.save(file_path)
                file_paths.append(file_path)
                file_names.append(filename)
        
        # Store file info in session
        session['file_paths'] = file_paths
        session['file_names'] = file_names
        session['mode'] = 'multiple'
        
        return redirect(url_for('configure_attendance_sessions'))

@app.route('/configure_attendance_sessions')
@login_required
def configure_attendance_sessions():
    mode = session.get('mode', 'single')
    if mode == 'single':
        return render_template('configure_attendance.html', mode='single', show_navigation=True)
    else:
        file_names = session.get('file_names', [])
        return render_template('configure_attendance.html', mode='multiple', file_names=file_names, show_navigation=True)

@app.route('/process_attendance', methods=['POST'])
@login_required
def process_attendance():
    try:
        mode = session.get('mode', 'single')
        
        if mode == 'single':
            # Get session data
            file_path = session.get('file_path')
            if not file_path or not os.path.exists(file_path):
                flash('File not found. Please upload again.')
                return redirect(url_for('attendance_generator'))
            
            # Get session configurations from form
            sessions_info = []
            session_count = int(request.form.get('session_count', 0))
            
            for i in range(session_count):
                start_str = request.form.get(f'start_time_{i}')
                end_str = request.form.get(f'end_time_{i}')
                time_required = float(request.form.get(f'time_required_{i}', 30))
                
                if start_str and end_str:
                    # Convert datetime-local format to our expected format
                    session_start = datetime.strptime(start_str, '%Y-%m-%dT%H:%M')
                    session_end = datetime.strptime(end_str, '%Y-%m-%dT%H:%M')
                    
                    if session_start >= session_end:
                        flash(f'Error in session {i+1}: Start time must be before end time.')
                        return redirect(url_for('configure_attendance_sessions'))
                    
                    sessions_info.append({
                        "session_start": session_start,
                        "session_end": session_end,
                        "time_required": time_required
                    })
            
            if not sessions_info:
                flash('Please add at least one session.')
                return redirect(url_for('configure_attendance_sessions'))
            
            # Process the attendance
            output_records, session_labels, session_summary = process_sessions_for_file(file_path, sessions_info)
            
            # Calculate statistics
            total_people = len(output_records)
            total_sessions = len(sessions_info)
            
            # Count present/absent across all sessions
            present_count = 0
            absent_count = 0
            
            for record in output_records:
                for i in range(total_sessions):
                    session_key = f'Session_{i+1}_Status'
                    if session_key in record:
                        if record[session_key] == 'P':
                            present_count += 1
                        elif record[session_key] == 'A':
                            absent_count += 1
            
            # Calculate averages
            avg_present = round(present_count / total_sessions, 1) if total_sessions > 0 else 0
            avg_absent = round(absent_count / total_sessions, 1) if total_sessions > 0 else 0
            
            # Store statistics in session
            session['processing_stats'] = {
                'total_people': total_people,
                'total_sessions': total_sessions,
                'avg_present': avg_present,
                'avg_absent': absent_count,
                'success': True,
                'message': f'Successfully processed {total_people} attendees across {total_sessions} session(s)'
            }
            
            # Read raw log data
            with open(file_path, 'r', encoding='utf-8') as f:
                sample = f.read(1024)
                f.seek(0)
                dialect = csv.Sniffer().sniff(sample)
                raw_data = list(csv.reader(f, dialect))
            raw_log_df = pd.DataFrame(raw_data)
            
            # Create output Excel file
            output_filename = os.path.splitext(session['filename'])[0] + '_processed.xlsx'
            output_path = os.path.join(TEMP_DIR, output_filename)
            
            write_excel(raw_log_df, output_records, output_path)
            
            # Store output path in session
            session['output_path'] = output_path
            session['output_filename'] = output_filename
            
            # Automatically download the file after processing
            flash('Processing Complete! Your attendance reports have been generated.', 'success')
            return send_file(output_path, as_attachment=True, download_name=output_filename)
        else:  # multiple mode
            file_paths = session.get('file_paths', [])
            file_names = session.get('file_names', [])
            
            if not file_paths:
                flash('No files found. Please upload again.')
                return redirect(url_for('attendance_generator'))
            
            # Get session configurations from form
            # In multiple mode, we need to associate sessions with specific files
            sessions_by_file = {}
            
            # Get the number of session rows
            session_row_count = int(request.form.get('session_row_count', 0))
            
            for i in range(session_row_count):
                file_name = request.form.get(f'file_name_{i}')
                start_str = request.form.get(f'start_time_{i}')
                end_str = request.form.get(f'end_time_{i}')
                time_required = float(request.form.get(f'time_required_{i}', 30))
                
                if file_name and start_str and end_str:
                    # Convert datetime-local format to our expected format
                    session_start = datetime.strptime(start_str, '%Y-%m-%dT%H:%M')
                    session_end = datetime.strptime(end_str, '%Y-%m-%dT%H:%M')
                    
                    if session_start >= session_end:
                        flash(f'Error in session for file {file_name}: Start time must be before end time.')
                        return redirect(url_for('configure_attendance_sessions'))
                    
                    # Find the file path for this file name
                    file_path = None
                    for j, name in enumerate(file_names):
                        if name == file_name:
                            file_path = file_paths[j]
                            break
                    
                    if file_path:
                        session_info = {
                            "session_start": session_start,
                            "session_end": session_end,
                            "time_required": time_required
                        }
                        
                        if file_path not in sessions_by_file:
                            sessions_by_file[file_path] = {
                                "file_name": file_name,
                                "sessions": []
                            }
                        
                        sessions_by_file[file_path]["sessions"].append(session_info)
            
            if not sessions_by_file:
                flash('Please add at least one session.')
                return redirect(url_for('configure_attendance_sessions'))
            
            # Process each file
            output_files = []
            summary_all = {}
            
            for file_path, file_data in sessions_by_file.items():
                file_name = file_data["file_name"]
                sessions_info = file_data["sessions"]
                
                try:
                    # Process the attendance
                    output_records, session_labels, session_summary = process_sessions_for_file(file_path, sessions_info)
                    
                    # Read raw log data
                    with open(file_path, 'r', encoding='utf-8') as f:
                        sample = f.read(1024)
                        f.seek(0)
                        dialect = csv.Sniffer().sniff(sample)
                        raw_data = list(csv.reader(f, dialect))
                    raw_log_df = pd.DataFrame(raw_data)
                    
                    # Create output Excel file
                    output_filename = os.path.splitext(file_name)[0] + '_processed.xlsx'
                    output_path = os.path.join(TEMP_DIR, output_filename)
                    
                    write_excel(raw_log_df, output_records, output_path)
                    
                    output_files.append({
                        'path': output_path,
                        'name': output_filename
                    })
                    
                    summary_all[file_name] = "\n".join(session_summary)
                except Exception as e:
                    flash(f'Error processing file {file_name}: {str(e)}')
                    return redirect(url_for('configure_attendance_sessions'))
            
            # Store output files in session
            session['attendance_output_files'] = output_files
            
            # Automatically download files as zip
            flash('Processing Complete! Your attendance reports have been generated.', 'success')
            
            if len(output_files) == 1:
                # Single file - download directly
                file_info = output_files[0]
                return send_file(file_info['path'], as_attachment=True, download_name=file_info['name'])
            else:
                # Multiple files - create zip
                zip_filename = 'attendance_reports.zip'
                zip_path = os.path.join(TEMP_DIR, zip_filename)
                
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for file_info in output_files:
                        zipf.write(file_info['path'], file_info['name'])
                
                return send_file(zip_path, as_attachment=True, download_name=zip_filename)
        
    except Exception as e:
        flash(f'Error processing attendance: {str(e)}')
        return redirect(url_for('configure_attendance_sessions'))

@app.route('/download_attendance')
@login_required
def download_attendance():
    mode = session.get('mode', 'single')
    
    # Check if user wants to download (not first visit)
    download_now = request.args.get('download', 'false') == 'true'
    
    if mode == 'single':
        output_path = session.get('output_path')
        output_filename = session.get('output_filename')
        
        if not output_path or not os.path.exists(output_path):
            flash('Processed file not found.')
            return redirect(url_for('attendance_generator'))
        
        # If download requested, send file directly
        if download_now:
            return send_file(output_path, as_attachment=True, download_name=output_filename)
        
        # First visit - show template with statistics popup
        return render_template('download_attendance.html', 
                             files=[{'name': output_filename, 'path': output_path}],
                             single_file=True)
    else:
        output_files = session.get('attendance_output_files', [])
        
        # Check if a specific file is requested for download
        requested_file = request.args.get('file')
        if requested_file and download_now:
            for file_info in output_files:
                if file_info['name'] == requested_file:
                    return send_file(file_info['path'], as_attachment=True, download_name=file_info['name'])
        
        if not output_files:
            flash('No processed files found.')
            return redirect(url_for('attendance_generator'))
        
        # Render template to show all files with popup
        return render_template('download_attendance.html', 
                             files=output_files,
                             single_file=False)

# ----------- Raw Excel Generator Routes -----------
@app.route('/raw_excel_generator')
def raw_excel_generator():
    # Allow public viewing of the tool UI
    return render_template('raw_excel_generator.html', show_navigation=True)

@app.route('/process_raw_excel', methods=['POST'])
@login_required
def process_raw_excel():
    try:
        # Get uploaded files
        files = request.files.getlist('excel_files')
        if not files or not any(f.filename for f in files):
            flash('No files selected')
            return redirect(url_for('raw_excel_generator'))
        
        # Process each file
        output_files = []
        for file in files:
            if file.filename:
                # Save file temporarily
                filename = secure_filename(file.filename)
                file_path = os.path.join(TEMP_DIR, filename)
                file.save(file_path)
                
                # Process the file
                raw_df = extract_raw_from_excel(file_path)
                
                # Create output file
                output_filename = os.path.splitext(filename)[0] + '-RAW.xlsx'
                output_path = os.path.join(TEMP_DIR, output_filename)
                raw_df.to_excel(output_path, index=False)
                
                output_files.append({
                    'path': output_path,
                    'name': output_filename
                })
        
        # Store output files in session
        session['raw_output_files'] = output_files
        
        return redirect(url_for('download_raw_excel'))
        
    except Exception as e:
        flash(f'Error processing files: {str(e)}')
        return redirect(url_for('raw_excel_generator'))

@app.route('/download_raw_excel')
@login_required
def download_raw_excel():
    output_files = session.get('raw_output_files', [])
    
    # Check if a specific file is requested
    requested_file = request.args.get('file')
    if requested_file:
        for file_info in output_files:
            if file_info['name'] == requested_file:
                return send_file(file_info['path'], as_attachment=True, download_name=file_info['name'])
    
    if not output_files:
        flash('No processed files found.')
        return redirect(url_for('raw_excel_generator'))
    
    # If only one file, download it directly
    if len(output_files) == 1:
        file_info = output_files[0]
        return send_file(file_info['path'], as_attachment=True, download_name=file_info['name'])
    else:
        # Create a zip file with all outputs
        zip_filename = 'raw_excel_files.zip'
        zip_path = os.path.join(TEMP_DIR, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_info in output_files:
                zipf.write(file_info['path'], file_info['name'])
        
        return send_file(zip_path, as_attachment=True, download_name=zip_filename)

# ----------- Attendance Matching Routes -----------
@app.route('/attendance_matching')
def attendance_matching():
    # Allow public viewing of the tool UI
    return render_template('attendance_matching.html', show_navigation=True)

@app.route('/process_attendance_matching', methods=['POST'])
@login_required
def process_attendance_matching():
    try:
        # Get uploaded files
        master_files = request.files.getlist('master_files')
        raw_files = request.files.getlist('raw_files')
        
        if not master_files or not raw_files:
            flash('Please select both master and raw files')
            return redirect(url_for('attendance_matching'))
        
        # Get output format
        output_format = request.form.get('output_format', 'xlsx')
        
        # Save master files
        master_file_paths = []
        master_file_names = []
        for file in master_files:
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(TEMP_DIR, filename)
                file.save(file_path)
                master_file_paths.append(file_path)
                master_file_names.append(filename)
        
        # Save raw files
        raw_file_paths = []
        raw_file_names = []
        for file in raw_files:
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(TEMP_DIR, filename)
                file.save(file_path)
                raw_file_paths.append(file_path)
                raw_file_names.append(filename)
        
        # Process file pairs
        output_files = []
        
        # Match files by index (first master with first raw, etc.)
        max_pairs = min(len(master_file_paths), len(raw_file_paths))
        
        for i in range(max_pairs):
            master_path = master_file_paths[i]
            master_name = master_file_names[i]
            raw_path = raw_file_paths[i]
            raw_name = raw_file_names[i]
            
            # Process the matching
            output_path = match_and_write(master_path, raw_path, output_format)
            
            output_files.append({
                'path': output_path,
                'name': os.path.basename(output_path)
            })
        
        # Store output files in session
        session['matching_output_files'] = output_files
        
        return redirect(url_for('download_attendance_matching'))
        
    except Exception as e:
        flash(f'Error processing files: {str(e)}')
        return redirect(url_for('attendance_matching'))

@app.route('/download_attendance_matching')
@login_required
def download_attendance_matching():
    output_files = session.get('matching_output_files', [])
    
    # Check if a specific file is requested
    requested_file = request.args.get('file')
    if requested_file:
        for file_info in output_files:
            if file_info['name'] == requested_file:
                return send_file(file_info['path'], as_attachment=True, download_name=file_info['name'])
    
    if not output_files:
        flash('No processed files found.')
        return redirect(url_for('attendance_matching'))
    
    # If only one file, download it directly
    if len(output_files) == 1:
        file_info = output_files[0]
        return send_file(file_info['path'], as_attachment=True, download_name=file_info['name'])
    else:
        # Create a zip file with all outputs
        zip_filename = 'matching_results.zip'
        zip_path = os.path.join(TEMP_DIR, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_info in output_files:
                zipf.write(file_info['path'], file_info['name'])
        
        return send_file(zip_path, as_attachment=True, download_name=zip_filename)

if __name__ == '__main__':
    print("Starting Attendance Tools Suite...")
    print("Open your web browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0')
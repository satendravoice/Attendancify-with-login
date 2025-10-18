# 🚀 Deployment Guide - Attendancify

This guide will help you deploy Attendancify to production environments.

## 📋 Table of Contents

- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [GitHub Setup](#github-setup)
- [PythonAnywhere Deployment](#pythonanywhere-deployment)
- [Heroku Deployment](#heroku-deployment)
- [Production Best Practices](#production-best-practices)

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All dependencies are listed in `requirements.txt`
- [ ] `.gitignore` is configured properly
- [ ] Default superadmin password will be changed after first login
- [ ] Environment variables are set (if any)
- [ ] Debug mode is OFF in production
- [ ] Static files are properly configured
- [ ] Database/session management is secure

---

## 🐙 GitHub Setup

### 1. Initialize Git Repository

```bash
cd d:\Python\Attendancify
git init
git add .
git commit -m "Initial commit: Attendancify with login system"
```

### 2. Connect to GitHub Repository

```bash
git remote add origin https://github.com/satendravoice/Attendancify-with-login.git
git branch -M main
git push -u origin main
```

### 3. Verify Upload

Visit: https://github.com/satendravoice/Attendancify-with-login

---

## 🌐 PythonAnywhere Deployment

### Step 1: Create Account

1. Go to [PythonAnywhere](https://www.pythonanywhere.com/)
2. Sign up for a free account
3. Verify your email

### Step 2: Clone Repository

Open a **Bash console** in PythonAnywhere:

```bash
# Clone your repository
git clone https://github.com/satendravoice/Attendancify-with-login.git

# Navigate to directory
cd Attendancify-with-login

# Install dependencies
pip3.9 install --user -r requirements.txt
```

### Step 3: Create Web App

1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.9** or higher

### Step 4: Configure WSGI File

Click on **WSGI configuration file** link and replace content with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/Attendancify-with-login'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable for Flask
os.environ['FLASK_APP'] = 'comprehensive_app.py'

# Import Flask app
from comprehensive_app import app as application

# IMPORTANT: Disable debug mode in production
application.config['DEBUG'] = False
```

**Important**: Replace `YOUR_USERNAME` with your actual PythonAnywhere username!

### Step 5: Configure Static Files

In the **Web** tab, under **Static files**:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR_USERNAME/Attendancify-with-login/static/` |

### Step 6: Set Working Directory

In **Code** section:
- **Source code**: `/home/YOUR_USERNAME/Attendancify-with-login`
- **Working directory**: `/home/YOUR_USERNAME/Attendancify-with-login`

### Step 7: Reload Web App

1. Scroll to top of **Web** tab
2. Click green **Reload** button
3. Your app will be live at: `https://YOUR_USERNAME.pythonanywhere.com`

### Step 8: First Login

1. Visit your app URL
2. Login with:
   - Email: `superadmin@attendancify.com`
   - Password: `admin`
3. **Change password immediately** when prompted

---

## 🚢 Heroku Deployment

### Prerequisites

```bash
# Install Heroku CLI
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
# Mac: brew tap heroku/brew && brew install heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 1: Create Procfile

Create `Procfile` in project root:

```
web: gunicorn comprehensive_app:app
```

### Step 2: Update requirements.txt

```bash
pip freeze > requirements.txt
# Ensure gunicorn is included
echo "gunicorn==20.1.0" >> requirements.txt
```

### Step 3: Create runtime.txt

```
python-3.9.16
```

### Step 4: Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create attendancify-app

# Push to Heroku
git push heroku main

# Open app
heroku open
```

### Step 5: Configure Environment

```bash
# Set Flask secret key (generate a random one)
heroku config:set FLASK_SECRET_KEY="your-secret-key-here"

# View logs
heroku logs --tail
```

---

## 🔐 Production Best Practices

### 1. Security

#### Change Secret Key
In `comprehensive_app.py`:

```python
import os
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback-secret-key-for-development')
```

Set environment variable:
- **PythonAnywhere**: Add in WSGI file
- **Heroku**: `heroku config:set FLASK_SECRET_KEY="random-string"`

#### Disable Debug Mode

```python
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

#### Force HTTPS (Production)

```python
from flask_talisman import Talisman

Talisman(app, content_security_policy=None)
```

### 2. Performance

#### Enable Gzip Compression

```python
from flask_compress import Compress

Compress(app)
```

#### Add Caching Headers

```python
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response
```

### 3. Database (Future Enhancement)

For production, consider:
- **SQLite** → Migrate to **PostgreSQL** or **MySQL**
- Use **SQLAlchemy** for ORM
- Implement proper database migrations

### 4. File Storage

Current implementation uses temporary files. For production:
- Use cloud storage (AWS S3, Google Cloud Storage)
- Implement file cleanup cron jobs
- Add file size limits

### 5. Monitoring

#### Add Logging

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('attendancify.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Attendancify startup')
```

#### Error Tracking

Consider integrating:
- **Sentry** for error tracking
- **Google Analytics** for usage statistics
- **Uptime monitoring** (UptimeRobot, Pingdom)

### 6. Backup Strategy

- Regular database backups (if using database)
- Export user data periodically
- Version control all code changes
- Document configuration changes

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Static Files Not Loading

**Solution**: Check static file paths in WSGI configuration

#### 2. Module Import Errors

**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --user
```

#### 3. Permission Errors

**Solution**: Check file permissions:
```bash
chmod -R 755 /home/username/Attendancify-with-login
```

#### 4. App Crashes on Startup

**Solution**: Check error logs:
- **PythonAnywhere**: Error log tab
- **Heroku**: `heroku logs --tail`

### Getting Help

- 📚 Check existing [GitHub Issues](https://github.com/satendravoice/Attendancify-with-login/issues)
- 🐛 Report bugs with detailed error messages
- 💬 Include server logs when asking for help

---

## 📊 Post-Deployment

### 1. Test Functionality

- [ ] Login works correctly
- [ ] Password change on first login works
- [ ] Attendance generation processes files
- [ ] Downloads work properly
- [ ] All three tools are functional
- [ ] User creation works (admin/superadmin)

### 2. Performance Check

- [ ] Page load times are acceptable
- [ ] File uploads handle large files
- [ ] No memory leaks during processing

### 3. Security Audit

- [ ] Default password changed
- [ ] HTTPS enabled (if possible)
- [ ] Session timeout configured
- [ ] File upload restrictions in place

---

## 🎉 Success!

Your Attendancify application should now be live and accessible to users!

**Next Steps:**
1. Share the URL with users
2. Create user accounts for administrators
3. Monitor logs for any issues
4. Collect feedback for improvements

---

## 📞 Support

Need help with deployment?

- 📧 Email: Check GitHub profile
- 📱 Instagram: [@satendragoswamii](https://www.instagram.com/satendragoswamii/)
- 🐛 Issues: [GitHub Issues](https://github.com/satendravoice/Attendancify-with-login/issues)

---

**Developed by Satendra Goswami** | © 2025 Attendancify

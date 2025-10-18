# 🚀 Quick Start Guide - Attendancify

## ⚡ 30-Second Setup

### 1. Install & Run

```bash
# Clone repository
git clone https://github.com/satendravoice/Attendancify-with-login.git
cd Attendancify-with-login

# Install dependencies
pip install -r requirements.txt

# Run application
python comprehensive_app.py
```

### 2. Access Application

Open browser: **http://localhost:5000**

### 3. Login

```
Email: superadmin@attendancify.com
Password: admin
```

⚠️ **You'll be forced to change password on first login** (for security)

---

## 🎯 What Can You Do?

### Tool 1: Attendance Generator
Upload Zoom CSV → Configure sessions → Auto-download attendance report

### Tool 2: Raw Excel Generator  
Upload Excel files → Extract attendance data → Download standardized format

### Tool 3: Attendance Matching
Upload master list + raw data → AI matching → Download matched report

---

## 👥 User Roles

| Role | Can Do |
|------|--------|
| **Superadmin** | Everything + view all passwords |
| **Admin** | Create users + process attendance |
| **User** | Process attendance only |

---

## 📁 File Formats

**Zoom CSV Required Columns:**
- Name, User Email, Join Time, Leave Time, Duration

**Master List (Excel):**
- Email, Participant Name

---

## 🆘 Quick Troubleshooting

**Q: Can't login?**  
A: Use exact credentials above. Check caps lock.

**Q: File won't upload?**  
A: Max size is 100MB. Check file format.

**Q: Processing fails?**  
A: Verify CSV columns match requirements.

**Q: Download doesn't start?**  
A: Check browser download settings/popup blocker.

---

## 📚 More Help

- **Full Documentation**: [README.md](README.md)
- **Deployment**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **User Management**: [PASSWORD_MANAGEMENT_SYSTEM.md](PASSWORD_MANAGEMENT_SYSTEM.md)

---

**Developed by Satendra Goswami** | [Instagram](https://instagram.com/satendragoswamii)

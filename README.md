# 🎓 Attendancify

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3.2-000000?logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Automated, Accurate, and Intelligent Attendance Management for Modern Education**

[Live Demo](https://zoomattendancify.pythonanywhere.com/) • [Features](#-features) • [Installation](#-installation) • [Documentation](#-usage)

</div>

---

## 📖 Overview

Attendancify is a web-based attendance management system that automates tracking for online sessions. Built for educators and training coordinators, it intelligently processes Zoom session logs and generates accurate attendance reports with second-level precision.

## ✨ Features

- **🔐 Secure Authentication** - Login-protected dashboard with user management
- **📝 Format Converter** - Convert Zoom reports to standardized Excel format
- **⏱️ Duration Calculator** - Calculate precise attendance duration for each participant
- **🤝 Smart Name Merger** - AI-powered fuzzy matching handles name variations
- **🎯 Attendance Matcher** - Match Zoom logs against student lists and flag discrepancies
- **📊 Advanced Analytics** - Visualize attendance patterns and trends
- **📱 Responsive Design** - Works seamlessly on desktop, tablet, and mobile

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/satendravoice/Attendancify-with-login.git
cd Attendancify-with-login

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

Access the application at `http://localhost:5000`

### Default Credentials

```
Username: admin
Password: admin123
```

**⚠️ Change these immediately after first login!**

## 💻 Tech Stack

**Backend:** Python 3.9+, Flask 2.3.2, Pandas, RapidFuzz, Werkzeug  
**Frontend:** Bootstrap 5.3, JavaScript/jQuery, HTML5/CSS3  
**Storage:** JSON authentication, Excel/CSV processing

## 📖 Usage

1. **Login** with your credentials
2. **Select a tool** from the dashboard:
   - Format Converter: Standardize Zoom CSV/Excel files
   - Duration Calculator: Calculate attendance time
   - Name Merger: Merge similar name variations (80% threshold)
   - Attendance Matcher: Generate final attendance reports
3. **Upload files** and process
4. **Download** generated reports

## 🎯 Live Demo

Try Attendancify without installation: [https://zoomattendancify.pythonanywhere.com/](https://zoomattendancify.pythonanywhere.com/)

**Demo Credentials:** `admin / admin123`

## 🤝 Contributing

Contributions are welcome! Fork the repo, create a feature branch, and submit a pull request.

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Satendra Goswami**  
[![Instagram](https://img.shields.io/badge/Instagram-@satendragoswamii-E4405F?logo=instagram&logoColor=white)](https://www.instagram.com/satendragoswamii/)
[![GitHub](https://img.shields.io/badge/GitHub-satendravoice-181717?logo=github&logoColor=white)](https://github.com/satendravoice)

---

<div align="center">

**Attendancify** © 2025 | Made with 💙 for Educators Worldwide

⭐ **Star this repo if you find it helpful!**

</div>
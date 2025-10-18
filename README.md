# 🎓 Attendancify – Professional Attendance Management System

<div align="center">

![Attendancify Banner](https://img.shields.io/badge/Attendancify-Intelligent_Attendance_Automation-6366f1?style=for-the-badge)

[![![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![![Flask](https://img.shields.io/badge/Flask-2.3.2-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Automated, Accurate, and Intelligent Attendance Management for Modern Education**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Live Demo](#-live-demo) • [Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Default Credentials](#-default-credentials)
- [Usage Guide](#-usage-guide)
- [Tools Overview](#-tools-overview)
- [File Formats](#-file-formats)
- [Live Demo](#-live-demo)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)
- [Developer](#-developer)

---

## 🌟 Overview

**Attendancify** is a comprehensive web-based attendance management system designed specifically for educators, training coordinators, and organizations conducting online sessions via Zoom or similar platforms. It automates the tedious process of attendance tracking by intelligently processing session logs and generating accurate, detailed reports.

### Why Attendancify?

- ⏱️ **Save Time**: Automate hours of manual attendance tracking
- 🎯 **Precision**: Second-level accuracy in attendance calculation
- 🤖 **Smart Matching**: AI-powered fuzzy name matching handles variations
- 📊 **Comprehensive**: Supports Zoom, manual lists, and multiple data formats
- 🔐 **Secure**: Login-protected dashboard with user management

---

## ✨ Features

### 🎯 Core Capabilities

| Feature | Description |
|---------|-------------|
| 🔐 **Secure Authentication** | Login-protected dashboard with user management |
| 📱 **Responsive Design** | Works seamlessly on desktop, tablet, and mobile |
| 📊 **Advanced Analytics** | Visualize attendance patterns and trends |
| 🔄 **Batch Processing** | Handle multiple sessions simultaneously |
| 📈 **Real-time Updates** | Live processing status and progress tracking |
| 🎨 **Modern UI** | Clean, intuitive interface built with Bootstrap 5 |

### 🛠️ Tool Suite

#### 1. 📝 Format Converter
- Convert Zoom attendance reports to standard Excel format
- Clean and normalize participant names
- Handle multiple file uploads

#### 2. ⏱️ Duration Calculator
- Calculate precise attendance duration for each participant
- Second-level accuracy
- Support for multiple join/leave cycles

#### 3. 🤝 Smart Name Merger
- AI-powered fuzzy matching for name variations
- Configurable similarity thresholds
- Handles typos, spacing, and formatting differences

#### 4. 🎯 Attendance Matcher
- Match Zoom logs against enrolled student lists
- Flag missing/extra participants
- Generate comprehensive attendance reports

---

## 💻 Tech Stack

### Backend
- **Python 3.9+**: Core programming language
- **Flask 2.3.2**: Lightweight web framework
- **Pandas**: Data manipulation and analysis
- **RapidFuzz**: Fuzzy string matching
- **Werkzeug**: Security utilities

### Frontend
- **Bootstrap 5.3**: Responsive UI framework
- **JavaScript/jQuery**: Interactive elements
- **HTML5/CSS3**: Modern web standards

### Storage
- JSON-based user authentication
- Excel/CSV file handling
- Temporary file management

---

## 📦 Installation

### Prerequisites

```bash
# Python 3.9 or higher
python --version

# pip package manager
pip --version
```

### Step 1: Clone the Repository

```bash
git clone https://github.com/satendravoice/Attendancify-with-login.git
cd Attendancify-with-login
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python main.py
```

The application will start at `http://localhost:5000`

---

## 🔑 Default Credentials

**⚠️ IMPORTANT: Change these immediately after first login!**

```
Username: admin
Password: admin123
```

### Change Password Steps:
1. Login with default credentials
2. Navigate to user management
3. Update password immediately
4. Store new credentials securely

---

## 📖 Usage Guide

### 1. Login
1. Navigate to `http://localhost:5000`
2. Enter credentials
3. Access the main dashboard

### 2. Format Converter
1. Select "Format Converter" tool
2. Upload Zoom attendance CSV/Excel file
3. Click "Convert"
4. Download formatted Excel file

### 3. Duration Calculator
1. Select "Duration Calculator" tool
2. Upload formatted attendance file
3. Process file
4. Download duration report

### 4. Name Merger
1. Select "Name Merger" tool
2. Upload attendance file
3. Set similarity threshold (default: 80%)
4. Review merged names
5. Download cleaned file

### 5. Attendance Matcher
1. Select "Attendance Matcher" tool
2. Upload Zoom attendance log
3. Upload enrolled student list
4. Process matching
5. Download final report with:
   - Present students
   - Absent students
   - Extra participants
   - Duration details

---

## 🔧 Tools Overview

### Format Converter

**Input**: Raw Zoom attendance CSV/Excel  
**Output**: Standardized Excel format

**Features**:
- Removes duplicate entries
- Standardizes column names
- Cleans participant data

### Duration Calculator

**Input**: Formatted attendance file  
**Output**: Duration report

**Features**:
- Calculates total attendance time
- Handles multiple join/leave cycles
- Provides second-level precision

### Smart Name Merger

**Input**: Attendance file with name variations  
**Output**: Merged and cleaned file

**Features**:
- AI-powered fuzzy matching
- Configurable similarity threshold
- Preview before merging

### Attendance Matcher

**Input**: Zoom log + Student list  
**Output**: Comprehensive attendance report

**Features**:
- Identifies present/absent students
- Flags unauthorized participants
- Generates detailed reports

---

## 📄 File Formats

### Input Files

#### Zoom Attendance File
```csv
Name,Email,Join Time,Leave Time,Duration (Minutes)
John Doe,john@example.com,2024-01-15 10:00:00,2024-01-15 11:30:00,90
```

#### Student List File
```csv
Student Name,Student ID,Email
John Doe,12345,john@example.com
```

### Output Files

#### Attendance Report
```csv
Student Name,Status,Duration,Join Time,Leave Time
John Doe,Present,01:30:00,10:00:00,11:30:00
```

---

## 🎯 Live Demo

**Try Attendancify online without any installation!**

🔗 **Live Application**: [https://zoomattendancify.pythonanywhere.com/](https://zoomattendancify.pythonanywhere.com/)

**Demo Credentials**:
```
Username: admin
Password: admin123
```

**Note**: This is a demo environment. Your data is not permanently stored.

---

## 🚀 Deployment

### Local Deployment
```bash
python main.py
```

### Production Deployment

#### Heroku
```bash
heroku create attendancify-app
git push heroku master
heroku open
```

#### PythonAnywhere
1. Create PythonAnywhere account
2. Upload project files
3. Configure WSGI
4. Set environment variables
5. Reload web app

#### Docker
```bash
docker build -t attendancify .
docker run -p 5000:5000 attendancify
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit** your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write clear commit messages
- Add tests for new features
- Update documentation

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Satendra Goswami

Permission is hereby granted, free of charge, to any person obtaining a copy...
```

---

## 💬 Support

### Get Help

- 📖 **Documentation**: Check this README and code comments
- 🐛 **Bug Reports**: [Open an issue](https://github.com/satendravoice/Attendancify-with-login/issues)
- 💡 **Feature Requests**: [Submit a request](https://github.com/satendravoice/Attendancify-with-login/issues)
- 📧 **Contact**: Reach out via Instagram (below)

### Community

- ⭐ **Star** this repo if you find it helpful!
- 🍴 **Fork** and contribute
- 📢 **Share** with educators and administrators

---

## 👨‍💻 Developer

<div align="center">

**Developed with ❤️ by**

### Satendra Goswami

[![![Instagram](https://img.shields.io/badge/Instagram-@satendragoswamii-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/satendragoswamii/)
[![![GitHub](https://img.shields.io/badge/GitHub-satendravoice-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/satendravoice)

*Professional Python Developer | AI Enthusiast | EdTech Innovator*

</div>

---

## 🙏 Acknowledgments

- Built with **Flask** for robust backend
- **Pandas** for efficient data processing
- **RapidFuzz** for intelligent name matching
- **Bootstrap 5** for responsive, modern UI
- Inspired by the need for accurate remote attendance tracking in modern education

---

## ⚠️ Important Notes

- **AI-Based Tool**: While highly accurate, please verify critical attendance data
- **Security**: Always change default passwords immediately
- **Backup**: Keep backup copies of original attendance files
- **Privacy**: Handle student data responsibly and comply with data protection regulations

---

<div align="center">

### 🌟 If this project helped you, please give it a star! 🌟

**Attendancify** © 2025 | Made with 💙 for Educators Worldwide

</div>

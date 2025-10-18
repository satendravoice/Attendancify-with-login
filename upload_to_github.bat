@echo off
echo ========================================
echo   Attendancify - GitHub Upload Script
echo ========================================
echo.

echo Step 1: Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo Please download Git from: https://git-scm.com/downloads
    pause
    exit /b 1
)
echo ✓ Git is installed
echo.

echo Step 2: Navigating to project directory...
cd /d "%~dp0"
echo ✓ Current directory: %CD%
echo.

echo Step 3: Initializing Git repository (if needed)...
if not exist ".git" (
    git init
    echo ✓ Git repository initialized
) else (
    echo ✓ Git repository already exists
)
echo.

echo Step 4: Staging all files...
git add .
echo ✓ Files staged
echo.

echo Step 5: Creating commit...
git commit -m "feat: Complete Attendancify system with authentication and modern UI - Added secure login system with role-based access - Implemented three attendance tools (Generator, Raw Excel, Matching) - Modern responsive UI with dark/light theme - Password management with forced change on first login - Comprehensive user management for superadmin - Automatic download after processing - Statistics popup with attendance data - Professional documentation and deployment guide"
echo ✓ Commit created
echo.

echo Step 6: Adding remote repository...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/satendravoice/Attendancify-with-login.git
echo ✓ Remote repository configured
echo.

echo Step 7: Setting main branch...
git branch -M main
echo ✓ Branch set to main
echo.

echo ========================================
echo   Ready to Push to GitHub!
echo ========================================
echo.
echo Repository: https://github.com/satendravoice/Attendancify-with-login
echo.
echo IMPORTANT: You will need to authenticate with GitHub.
echo Use your GitHub Personal Access Token as password.
echo.
echo How to get a Personal Access Token:
echo 1. Go to GitHub.com → Settings → Developer settings
echo 2. Click "Personal access tokens" → "Tokens (classic)"
echo 3. Click "Generate new token (classic)"
echo 4. Select scope: "repo" (full control)
echo 5. Generate and copy the token
echo 6. Use it as password when prompted
echo.
echo ========================================
pause
echo.

echo Step 8: Pushing to GitHub...
git push -u origin main --force
echo.

if %errorlevel% equ 0 (
    echo ========================================
    echo   ✓ SUCCESS! Project uploaded to GitHub
    echo ========================================
    echo.
    echo Visit your repository at:
    echo https://github.com/satendravoice/Attendancify-with-login
    echo.
    echo Next steps:
    echo 1. Check README.md displays correctly
    echo 2. Update repository description and topics
    echo 3. Create a release (v1.0.0)
    echo 4. Deploy to PythonAnywhere (see DEPLOYMENT_GUIDE.md)
    echo.
) else (
    echo ========================================
    echo   × ERROR: Failed to push to GitHub
    echo ========================================
    echo.
    echo Common issues:
    echo 1. Authentication failed - Use Personal Access Token
    echo 2. Repository doesn't exist - Create it on GitHub first
    echo 3. No internet connection - Check your network
    echo.
    echo See GITHUB_UPLOAD.md for detailed troubleshooting
    echo.
)

echo ========================================
pause

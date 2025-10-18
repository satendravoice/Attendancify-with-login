#!/bin/bash

echo "========================================"
echo "  Attendancify - GitHub Upload Script"
echo "========================================"
echo ""

echo "Step 1: Checking Git installation..."
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed!"
    echo "Install Git: https://git-scm.com/downloads"
    exit 1
fi
echo "✓ Git is installed"
echo ""

echo "Step 2: Navigating to project directory..."
cd "$(dirname "$0")"
echo "✓ Current directory: $(pwd)"
echo ""

echo "Step 3: Initializing Git repository (if needed)..."
if [ ! -d ".git" ]; then
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already exists"
fi
echo ""

echo "Step 4: Staging all files..."
git add .
echo "✓ Files staged"
echo ""

echo "Step 5: Creating commit..."
git commit -m "feat: Complete Attendancify system with authentication and modern UI

- Added secure login system with role-based access
- Implemented three attendance tools (Generator, Raw Excel, Matching)
- Modern responsive UI with dark/light theme
- Password management with forced change on first login
- Comprehensive user management for superadmin
- Automatic download after processing
- Statistics popup with attendance data
- Professional documentation and deployment guide"
echo "✓ Commit created"
echo ""

echo "Step 6: Adding remote repository..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/satendravoice/Attendancify-with-login.git
echo "✓ Remote repository configured"
echo ""

echo "Step 7: Setting main branch..."
git branch -M main
echo "✓ Branch set to main"
echo ""

echo "========================================"
echo "  Ready to Push to GitHub!"
echo "========================================"
echo ""
echo "Repository: https://github.com/satendravoice/Attendancify-with-login"
echo ""
echo "IMPORTANT: You will need to authenticate with GitHub."
echo "Use your GitHub Personal Access Token as password."
echo ""
echo "How to get a Personal Access Token:"
echo "1. Go to GitHub.com → Settings → Developer settings"
echo "2. Click 'Personal access tokens' → 'Tokens (classic)'"
echo "3. Click 'Generate new token (classic)'"
echo "4. Select scope: 'repo' (full control)"
echo "5. Generate and copy the token"
echo "6. Use it as password when prompted"
echo ""
echo "========================================"
read -p "Press Enter to continue..."
echo ""

echo "Step 8: Pushing to GitHub..."
git push -u origin main --force
echo ""

if [ $? -eq 0 ]; then
    echo "========================================"
    echo "  ✓ SUCCESS! Project uploaded to GitHub"
    echo "========================================"
    echo ""
    echo "Visit your repository at:"
    echo "https://github.com/satendravoice/Attendancify-with-login"
    echo ""
    echo "Next steps:"
    echo "1. Check README.md displays correctly"
    echo "2. Update repository description and topics"
    echo "3. Create a release (v1.0.0)"
    echo "4. Deploy to PythonAnywhere (see DEPLOYMENT_GUIDE.md)"
    echo ""
else
    echo "========================================"
    echo "  × ERROR: Failed to push to GitHub"
    echo "========================================"
    echo ""
    echo "Common issues:"
    echo "1. Authentication failed - Use Personal Access Token"
    echo "2. Repository doesn't exist - Create it on GitHub first"
    echo "3. No internet connection - Check your network"
    echo ""
    echo "See GITHUB_UPLOAD.md for detailed troubleshooting"
    echo ""
fi

echo "========================================"
read -p "Press Enter to exit..."

# Detailed Setup Guide

## Chemical Equipment Parameter Visualizer

This guide provides step-by-step instructions for setting up the Chemical Equipment Visualizer on your local machine.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Backend Setup](#backend-setup)
3. [Web Frontend Setup](#web-frontend-setup)
4. [Desktop Frontend Setup](#desktop-frontend-setup)
5. [Verification](#verification)
6. [Common Issues](#common-issues)

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **Node.js**: Version 14.0 or higher
- **npm**: Version 6.0 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB free space

### Software Prerequisites

1. **Python** - [Download](https://www.python.org/downloads/)
   ```bash
   python --version  # Should show 3.8 or higher
   ```

2. **Node.js and npm** - [Download](https://nodejs.org/)
   ```bash
   node --version  # Should show v14 or higher
   npm --version   # Should show v6 or higher
   ```

3. **Git** (optional) - [Download](https://git-scm.com/)
   ```bash
   git --version
   ```

## Backend Setup

### Step 1: Extract Project Files

Extract the project ZIP file to your desired location:
```
C:\Projects\chemical-equipment-visualizer  (Windows)
/Users/username/Projects/chemical-equipment-visualizer  (macOS)
/home/username/Projects/chemical-equipment-visualizer  (Linux)
```

### Step 2: Navigate to Backend Directory

```bash
cd chemical-equipment-visualizer/backend
```

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Django 4.2.7
- djangorestframework
- django-cors-headers
- pandas
- numpy
- reportlab
- Pillow
- python-decouple

### Step 5: Initialize Database

```bash
python manage.py makemigrations
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, equipment_api, sessions, authtoken
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Step 6: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email address: admin@example.com
Password: ******** (minimum 8 characters)
Password (again): ********
Superuser created successfully.
```

### Step 7: Start Backend Server

```bash
python manage.py runserver
```

Expected output:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
February 03, 2026 - 12:00:00
Django version 4.2.7, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

✅ **Backend is now running at `http://localhost:8000`**

Test the API:
- Visit `http://localhost:8000/admin` - You should see the Django admin login
- Visit `http://localhost:8000/api/` - You should see API endpoints

Keep this terminal window open. The backend must stay running.

## Web Frontend Setup

### Step 1: Open New Terminal

Keep the backend terminal running and open a new terminal window.

### Step 2: Navigate to Web Frontend Directory

```bash
cd chemical-equipment-visualizer/frontend-web
```

### Step 3: Install Dependencies

```bash
npm install
```

This will install:
- react
- react-router-dom
- axios
- chart.js
- react-chartjs-2
- And other dependencies

Installation may take 2-5 minutes depending on your internet speed.

### Step 4: Start Development Server

```bash
npm start
```

Expected output:
```
Compiled successfully!

You can now view chemical-equipment-web in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.

webpack compiled successfully
```

✅ **Web frontend is now running at `http://localhost:3000`**

Your default browser should automatically open to `http://localhost:3000`.

### Step 5: Verify Web Frontend

1. You should see the login page
2. Click "Register here" to create an account
3. Fill in the registration form
4. After registration, you'll be redirected to the dashboard

## Desktop Frontend Setup

### Step 1: Open New Terminal

Open a third terminal window.

### Step 2: Navigate to Desktop Frontend Directory

```bash
cd chemical-equipment-visualizer/frontend-desktop
```

### Step 3: Create Virtual Environment (Optional but Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- PyQt5
- requests
- pandas
- matplotlib
- numpy

Installation may take a few minutes.

### Step 5: Run Desktop Application

```bash
python main.py
```

✅ **Desktop application window should appear**

### Step 6: Verify Desktop Frontend

1. Login window should appear
2. Use the same credentials you created for the web app
3. Or create a new account using "Create New Account" button

## Verification

### Testing the Complete System

1. **Backend Running**: `http://localhost:8000`
   - Admin panel accessible: `http://localhost:8000/admin`
   - API responding: `http://localhost:8000/api/`

2. **Web Frontend Running**: `http://localhost:3000`
   - Login page loads
   - Registration works
   - Dashboard accessible after login

3. **Desktop Frontend Running**:
   - Login window appears
   - Can login with web credentials
   - Desktop app opens after login

### Test Data Upload

1. **Locate Sample File**: `sample_equipment_data.csv` in project root

2. **Upload via Web**:
   - Login to web frontend
   - Click "Choose CSV File"
   - Select `sample_equipment_data.csv`
   - File should upload successfully
   - Dataset appears in list

3. **Upload via Desktop**:
   - Login to desktop app
   - Go to "Upload Dataset" tab
   - Click "Select CSV File to Upload"
   - Select `sample_equipment_data.csv`
   - Success message should appear

4. **View Analytics**:
   - Both frontends should show the uploaded dataset
   - Click "View Details" to see visualizations
   - Generate PDF report

## Common Issues

### Issue 1: Port Already in Use

**Problem**: Backend says port 8000 is already in use

**Solution**:
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# macOS/Linux:
lsof -ti:8000
kill -9 <process_id>

# Or use different port:
python manage.py runserver 8001
```

If you use a different port, update `API_BASE_URL` in:
- `frontend-web/src/services/api.js`
- `frontend-desktop/main.py`

### Issue 2: Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'django'`

**Solution**:
1. Ensure virtual environment is activated
2. Reinstall requirements:
   ```bash
   pip install -r requirements.txt
   ```

### Issue 3: CORS Errors in Web Frontend

**Problem**: Browser console shows CORS errors

**Solution**:
1. Check that backend is running
2. Verify `CORS_ALLOW_ALL_ORIGINS = True` in `backend/config/settings.py`
3. Clear browser cache
4. Restart backend server

### Issue 4: Desktop App Won't Start

**Problem**: PyQt5 import error or display issues

**Solution**:

**Windows**:
```bash
pip install PyQt5 --upgrade
```

**Linux** (if you get Qt platform plugin errors):
```bash
sudo apt-get install python3-pyqt5
sudo apt-get install libxcb-xinerama0
```

**macOS**:
```bash
pip install PyQt5 --upgrade
# If issues persist:
brew install pyqt5
```

### Issue 5: Database Migration Errors

**Problem**: Migration errors when running `makemigrations` or `migrate`

**Solution**:
1. Delete `db.sqlite3` file in backend directory
2. Delete all migration files in `backend/equipment_api/migrations/` except `__init__.py`
3. Run migrations again:
   ```bash
   python manage.py makemigrations equipment_api
   python manage.py migrate
   python manage.py createsuperuser
   ```

### Issue 6: npm Install Fails

**Problem**: npm install shows errors or warnings

**Solution**:
1. Clear npm cache:
   ```bash
   npm cache clean --force
   ```
2. Delete `node_modules` folder and `package-lock.json`
3. Run `npm install` again

### Issue 7: Chart.js Not Displaying

**Problem**: Charts don't show in web frontend

**Solution**:
1. Check browser console for errors
2. Verify data is being fetched (Network tab in DevTools)
3. Try refreshing the page
4. Clear browser cache

## Environment Variables (Optional)

For production deployment, create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

Then update `settings.py` to use these variables with `python-decouple`.

## Next Steps

After successful setup:

1. **Explore the Admin Panel**: `http://localhost:8000/admin`
   - View all datasets
   - Manage users
   - Monitor uploads

2. **Test All Features**:
   - Upload multiple CSV files
   - Generate PDF reports
   - View different visualizations
   - Test both web and desktop interfaces

3. **Read User Guide**: See `docs/USER_GUIDE.md` for detailed usage instructions

4. **Review API Documentation**: See `docs/API_DOCUMENTATION.md` for API details

## Production Deployment

For deploying to production:

### Backend
```bash
# Install gunicorn
pip install gunicorn

# Collect static files
python manage.py collectstatic

# Run with gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Web Frontend
```bash
# Build production version
npm run build

# Serve with any static server
# e.g., with nginx or Apache
```

### Desktop App
```bash
# Create standalone executable
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## Support

If you encounter issues not covered here:

1. Check the main `README.md` file
2. Review error messages carefully
3. Check Django and React documentation
4. Ensure all prerequisites are installed correctly

## Summary

You should now have:
- ✅ Backend running on port 8000
- ✅ Web frontend running on port 3000
- ✅ Desktop application installed and running
- ✅ Sample data ready to upload
- ✅ User account created

Congratulations! Your Chemical Equipment Visualizer is ready to use. 🎉

# Quick Start Guide

## Chemical Equipment Visualizer

Get up and running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8+ installed (`python --version`)
- ✅ Node.js 14+ installed (`node --version`)
- ✅ pip installed (`pip --version`)

## Automated Setup (Recommended)

### Windows
```cmd
setup.bat
```

### macOS/Linux
```bash
chmod +x setup.sh
./setup.sh
```

## Manual Setup (3 Steps)

### 1. Backend (Django)
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
✅ Backend running at http://localhost:8000

### 2. Web Frontend (React)
```bash
# Open new terminal
cd frontend-web
npm install
npm start
```
✅ Web app running at http://localhost:3000

### 3. Desktop App (PyQt5)
```bash
# Open new terminal
cd frontend-desktop
pip install -r requirements.txt
python main.py
```
✅ Desktop app window opens

## First Use

1. **Create Account**
   - Web: Go to http://localhost:3000/register
   - Desktop: Click "Create New Account"

2. **Upload Sample Data**
   - Use `sample_equipment_data.csv` from project root
   - Click "Choose CSV File" or "Select CSV File to Upload"

3. **View Analytics**
   - Dashboard shows statistics
   - Charts display automatically
   - Click "View Details" for more visualizations

4. **Generate Report**
   - Click "Generate PDF Report"
   - Save PDF to desired location

## Troubleshooting

**Port 8000 in use?**
```bash
python manage.py runserver 8001
# Update API_BASE_URL in frontend files
```

**ModuleNotFoundError?**
```bash
pip install -r requirements.txt
```

**npm errors?**
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## Default Credentials

Create your own with:
```bash
cd backend
python manage.py createsuperuser
```

Admin panel: http://localhost:8000/admin

## What's Included

- 📊 **Backend**: Django REST API (Port 8000)
- 🌐 **Web**: React dashboard (Port 3000)
- 💻 **Desktop**: PyQt5 application
- 📄 **Sample**: 20 equipment records
- 📚 **Docs**: Complete documentation

## Next Steps

1. Read the full [README.md](README.md)
2. Check [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for details
3. Review [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)
4. Try all features!

## Features to Try

- [ ] Register and login
- [ ] Upload CSV file
- [ ] View statistics
- [ ] Explore charts
- [ ] Generate PDF report
- [ ] Test both web and desktop
- [ ] Upload multiple datasets
- [ ] Check history management (5 max)

## Need Help?

- Backend issues → Check Django terminal for errors
- Web issues → Check browser console (F12)
- Desktop issues → Check terminal output
- General → See README.md

## Success Checklist

- [ ] Backend server running (port 8000)
- [ ] Web frontend running (port 3000)
- [ ] Desktop app opens
- [ ] Can register/login
- [ ] Can upload CSV
- [ ] Can view charts
- [ ] Can generate PDF
- [ ] Both interfaces work

---

**You're all set! 🎉**

Enjoy analyzing your chemical equipment data!

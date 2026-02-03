# Getting Started - First Run

## Chemical Equipment Parameter Visualizer

Welcome! Follow these simple steps to get started.

---

## Step 1: Setup (One-Time)

### Automated Setup (Recommended)

**Windows:**
```cmd
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

See QUICKSTART.md or README.md for detailed instructions.

---

## Step 2: Start the Application

You need to run THREE components in separate terminals:

### Terminal 1: Backend Server
```bash
cd backend
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
python manage.py runserver
```
✅ Backend should be running at http://localhost:8000

### Terminal 2: Web Frontend (Optional)
```bash
cd frontend-web
npm start
```
✅ Web app should open at http://localhost:3000

### Terminal 3: Desktop App (Optional)
```bash
cd frontend-desktop
# Windows: venv\Scripts\activate  
# macOS/Linux: source venv/bin/activate
python main.py
```
✅ Desktop window should appear

**Note:** Backend (Terminal 1) is REQUIRED. Choose either Web OR Desktop or run both.

---

## Step 3: Create Your Account

### First Time Setup

1. **Run Backend** (see Terminal 1 above)

2. **Create Admin Account** (Optional - for admin panel access)
   ```bash
   cd backend
   python manage.py createsuperuser
   ```
   Enter:
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: `admin123456` (or your choice, min 8 chars)

3. **Create User Account** (For using the app)
   - **Web**: Open http://localhost:3000/register
   - **Desktop**: Click "Create New Account"
   
   Fill in:
   - Username: `testuser` (your choice)
   - Email: `test@example.com` (your email)
   - Password: `testpass123` (min 8 characters)
   - Confirm password
   - (Optional) First name, Last name

4. **Login**
   - Use the username and password you just created
   - Web: http://localhost:3000/login
   - Desktop: Login window

---

## Step 4: Upload Sample Data

1. **Login** to your account

2. **Upload CSV**
   - **Web**: Click "Choose CSV File" button
   - **Desktop**: Go to "Upload Dataset" tab, click "Select CSV File"

3. **Select File**
   - Navigate to project folder
   - Select: `sample_equipment_data.csv`
   - Click Open

4. **Wait for Upload**
   - File processes automatically
   - Success message appears
   - Dataset appears in list

---

## Step 5: Explore Features

### View Analytics
- Click "View Details" on any dataset
- See charts and statistics
- Browse equipment table

### Generate PDF Report
- Select a dataset
- Click "Generate PDF Report"
- Choose save location
- PDF downloads automatically

### Try Different Views
- **Web**: Modern, responsive interface
- **Desktop**: Native application with matplotlib charts
- Both show same data, different visualizations!

---

## Quick Reference

### Default Ports
- Backend API: http://localhost:8000
- Web App: http://localhost:3000
- Admin Panel: http://localhost:8000/admin

### Sample Accounts

Create your own accounts - no default users exist initially.

**Admin Account** (for Django admin panel):
```bash
cd backend
python manage.py createsuperuser
```

**Regular User** (for app usage):
- Register through web: http://localhost:3000/register
- Register through desktop: "Create New Account" button

### Sample Data

**Location**: `sample_equipment_data.csv` in project root

**Contents**: 20 equipment records including:
- Reactors
- Heat Exchangers
- Pumps
- Compressors
- Storage Tanks
- And more...

**Columns**:
- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature

---

## Common Issues

### Backend won't start
- Check if port 8000 is free
- Activate virtual environment first
- Run migrations: `python manage.py migrate`

### Can't login
- Ensure you created an account first
- Check username/password (case-sensitive)
- Verify backend is running

### Upload fails
- Check CSV file format
- Ensure all required columns present
- Verify file is not corrupted

### Desktop app won't open
- Install PyQt5: `pip install PyQt5`
- Check if backend is running
- Try running from terminal to see errors

---

## Video Tutorial

Want to see it in action? Follow the DEMO_SCRIPT.md to create a walkthrough video or just follow the steps described there.

---

## Need More Help?

1. **QUICKSTART.md** - Fast setup guide
2. **README.md** - Complete documentation
3. **docs/SETUP_GUIDE.md** - Detailed setup steps
4. **docs/API_DOCUMENTATION.md** - API reference

---

## Test Checklist

After setup, verify:

- [ ] Backend running (http://localhost:8000)
- [ ] Can access admin panel (http://localhost:8000/admin)
- [ ] Can register new account (web or desktop)
- [ ] Can login successfully
- [ ] Can upload sample CSV
- [ ] Can view dashboard statistics
- [ ] Can see charts/visualizations
- [ ] Can view equipment table
- [ ] Can generate PDF report
- [ ] Both web and desktop work (if running both)

---

## What's Next?

Once everything works:

1. **Upload your own data** - Create CSV with same format
2. **Explore different charts** - View various visualizations
3. **Generate reports** - Create PDF documentation
4. **Try admin panel** - Manage data at http://localhost:8000/admin
5. **Read documentation** - Learn about all features

---

## Pro Tips

💡 **Keep backend running** - Frontend won't work without it
💡 **Use sample data first** - Test with provided CSV before using your own
💡 **Check browser console** - F12 for debugging web issues
💡 **Watch terminal output** - Backend shows helpful error messages
💡 **Create superuser** - Access Django admin for advanced features

---

## Architecture Overview

```
User Device
    ↓
[Web Browser] ← Port 3000 → [React Frontend]
                                  ↓
                            [API Calls]
                                  ↓
[Desktop App] ← [PyQt5 GUI] → [API Calls]
                                  ↓
                            Port 8000
                                  ↓
                    [Django REST Framework]
                                  ↓
                          [SQLite Database]
```

Both frontends connect to the same backend API!

---

## Success! 🎉

You should now have:
- ✅ Backend running smoothly
- ✅ User account created
- ✅ Sample data uploaded
- ✅ Charts displaying
- ✅ Full system operational

**Enjoy analyzing your chemical equipment data!**

For detailed usage instructions, see the complete documentation in the project files.

---

**Note**: This is a development setup. For production deployment, refer to the deployment section in README.md.

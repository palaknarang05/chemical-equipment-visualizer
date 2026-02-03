# Demo Video Script

## Chemical Equipment Parameter Visualizer
**Duration: 2-3 minutes**

---

## Introduction (15 seconds)

"Hello! Today I'll demonstrate the Chemical Equipment Parameter Visualizer - a hybrid application with both web and desktop interfaces for analyzing chemical equipment data."

**Show**: Project folder structure briefly

---

## Part 1: Backend & Authentication (30 seconds)

### Start Backend
"First, let's start the Django backend server."

**Show**: 
```bash
cd backend
python manage.py runserver
```

**Show**: Terminal output showing server running

### Registration
"Let me register a new user account."

**Show**: Registration form (web or desktop)
- Fill in: username, email, password
- Click "Create Account"

**Show**: Successful registration, redirect to dashboard

---

## Part 2: Web Interface (45 seconds)

### Dashboard Overview
"Here's the web dashboard with a modern, responsive design."

**Show**:
- Clean interface
- Statistics cards (0 datasets initially)
- Upload section

### Upload Dataset
"Let's upload the sample equipment data."

**Show**:
- Click "Choose CSV File"
- Select `sample_equipment_data.csv`
- Show upload progress
- Success message appears

**Show**:
- Statistics update (20 equipment)
- Dataset card appears with summary

### View Analytics
"Now let's view the detailed analytics."

**Show**:
- Click "View Details"
- Scroll through:
  - Equipment type distribution pie chart
  - Average parameters bar chart
  - Parameter comparison chart
  - Equipment data table

### Generate PDF Report
"We can generate a professional PDF report."

**Show**:
- Click "Generate PDF Report"
- PDF downloads
- Open PDF briefly to show contents

---

## Part 3: Desktop Interface (45 seconds)

### Open Desktop App
"The desktop application provides the same functionality."

**Show**:
```bash
python main.py
```

**Show**: Desktop app opens with login window

### Login
"I'll login with the same credentials."

**Show**:
- Enter username and password
- Click "Login"
- Main window opens

### Dashboard Tour
"The desktop app has three tabs."

**Show**:
1. **Upload Dataset tab**
   - Show file selection
   - Upload another CSV (or show previous data)

2. **View Datasets tab**
   - Show list of datasets
   - Click "View Details"

3. **Visualizations tab**
   - Show matplotlib charts:
     - Pie chart for equipment types
     - Bar chart for averages
     - Grouped bar chart for comparisons

### Generate Report
"PDF generation works here too."

**Show**:
- Select dataset
- Click "Generate PDF Report"
- Save dialog
- Confirmation message

---

## Part 4: Key Features Highlight (20 seconds)

**Show quick montage of**:
- Both interfaces side by side
- Charts updating
- Data table scrolling
- Multiple datasets

"Key features include:
- User authentication
- CSV upload with validation
- Real-time analytics
- Interactive visualizations
- PDF report generation
- History of last 5 datasets
- Identical functionality on both platforms"

---

## Part 5: Technical Stack (15 seconds)

**Show**: Code editor or project structure

"Built with:
- Django REST Framework backend
- React.js web frontend with Chart.js
- PyQt5 desktop frontend with Matplotlib
- Pandas for data processing
- ReportLab for PDF generation"

---

## Conclusion (10 seconds)

"This hybrid application demonstrates full-stack development, data visualization, and cross-platform compatibility - perfect for chemical equipment analysis."

**Show**: 
- Both applications running
- Sample PDF report
- Project documentation

"Thank you for watching! All source code and documentation are included."

---

## Recording Tips

### Tools Needed
- Screen recording software (OBS Studio, QuickTime, Windows Game Bar)
- Multiple windows/terminals open
- Sample CSV file ready
- Both frontends prepared

### Before Recording
1. Close unnecessary applications
2. Clear browser cache/history
3. Prepare terminal windows
4. Test all features once
5. Ensure good screen resolution (1920x1080 recommended)

### During Recording
- Speak clearly and at moderate pace
- Use mouse movements to guide viewer attention
- Pause briefly between major actions
- Show success messages clearly
- Keep transitions smooth

### After Recording
- Trim any mistakes
- Add simple annotations if needed
- Export in MP4 format
- Keep under 3 minutes

### What to Show Clearly
1. ✅ Registration/Login process
2. ✅ CSV file upload
3. ✅ Dashboard statistics
4. ✅ All chart types (pie, bar, line)
5. ✅ Data table
6. ✅ PDF generation and download
7. ✅ Both web and desktop interfaces
8. ✅ Successful operations (success messages)

### What to Avoid
- ❌ Long pauses
- ❌ Typing errors (practice first)
- ❌ Going too fast
- ❌ Showing errors (unless fixing them)
- ❌ Unnecessary clicking around

---

## Alternative: Quick Demo (90 seconds)

For a shorter version:

1. **Intro (10s)**: "Hybrid chemical equipment visualizer"
2. **Web Upload (20s)**: Login → Upload → See charts
3. **Desktop App (20s)**: Login → View datasets → Charts
4. **PDF Report (15s)**: Generate and show PDF
5. **Features (15s)**: List key features
6. **Tech Stack (10s)**: Mention technologies

---

## Screenshot Checklist

If creating static screenshots instead:

- [ ] Login page
- [ ] Registration page
- [ ] Web dashboard with statistics
- [ ] Upload section
- [ ] Dataset list
- [ ] Pie chart (equipment types)
- [ ] Bar chart (averages)
- [ ] Line/grouped chart (comparison)
- [ ] Data table
- [ ] Desktop login window
- [ ] Desktop main window
- [ ] Desktop charts
- [ ] PDF report pages
- [ ] Code structure

---

Good luck with your demo! 🎥

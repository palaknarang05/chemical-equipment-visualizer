# Chemical Equipment Parameter Visualizer

##  Overview

A professional hybrid web and desktop application for analyzing and visualizing chemical equipment parameters. Built with Django REST Framework backend, React.js web frontend, and PyQt5 desktop frontend.

##  Live Demo & Quick Access

### Web Application

- **Frontend URL**: https://chemical-equipment-visualizer-a12f.onrender.com
- **Backend API**: https://chemical-equipment-backend-bjfj.onrender.com
  
### Demo Credentials (if admin account exists)
**Username:** `admin`  
**Password:** `admin12345`
  
###  Desktop Application - Step-by-Step Guide

### Prerequisites
- Backend server must be running
- Python 3.8+ installed
- Dependencies installed

### Step 1: Start Backend Server (Required)
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Start server
python manage.py runserver
```
**Keep this terminal running.** Backend must be active for desktop app to work.

### Step 2: Launch Desktop Application
```bash
# Open a NEW terminal window
# Navigate to desktop frontend directory
cd frontend-desktop

# Activate virtual environment (if created)
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Run desktop application
python main.py
```

### Step 3: Create Account (First Time Only)

1. Click **"Create New Account"** button
2. Fill in the registration form:
   - **Username**: Choose a username (minimum 3 characters)
   - **Email**: Enter your email address
   - **Password**: Enter password (minimum 8 characters)
   - **Confirm Password**: Re-enter the same password
3. Click **"Register"**
4. Wait for success message: "Account created successfully! Please login."
5. **Close the desktop application**

### Step 4: Restart and Login

```bash
# Rerun the desktop application
python main.py
```

1. Enter your **username** and **password**
2. Click **"Login"**
3. You will be logged into the dashboard


##  Features

### Core Features
-  **User Authentication**: Secure login and registration system with token-based authentication
-  **CSV Upload**: Upload equipment data with automatic validation
-  **Data Analytics**: Automatic calculation of summary statistics and averages
-  **Interactive Visualizations**: 
  - Equipment type distribution (Pie charts)
  - Average parameter comparison (Bar charts)
  - Multi-parameter equipment comparison
-  **History Management**: Automatically maintains last 5 uploaded datasets
-  **PDF Report Generation**: Professional PDF reports with ReportLab
-  **Dual Frontend**: Both web and desktop interfaces with identical functionality
-  **REST API**: Complete API documentation and endpoints

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Django 4.2 + Django REST Framework | API server & business logic |
| **Frontend (Web)** | React.js 18 + Chart.js | Modern web interface |
| **Frontend (Desktop)** | PyQt5 + Matplotlib | Native desktop application |
| **Data Processing** | Pandas + NumPy | CSV parsing & analytics |
| **Database** | SQLite | Data persistence |
| **Reports** | ReportLab | PDF generation |
| **Authentication** | Token Authentication | Secure user sessions |

##  Project Structure

```
chemical-equipment-visualizer/
├── backend/                          # Django Backend
│   ├── config/                       # Django project settings
│   │   ├── __init__.py
│   │   ├── settings.py              # Main settings
│   │   ├── urls.py                  # URL routing
│   │   └── wsgi.py                  # WSGI config
│   ├── equipment_api/               # Main API app
│   │   ├── __init__.py
│   │   ├── admin.py                 # Admin interface
│   │   ├── apps.py                  # App configuration
│   │   ├── models.py                # Database models
│   │   ├── serializers.py           # API serializers
│   │   ├── urls.py                  # API endpoints
│   │   ├── views.py                 # API views/logic
│   │   ├── uploads/                 # Uploaded CSV files
│   │   └── reports/                 # Generated PDF reports
│   ├── manage.py                    # Django management
│   └── requirements.txt             # Python dependencies
│
├── frontend-web/                     # React Web Frontend
│   ├── public/
│   │   └── index.html               # HTML template
│   ├── src/
│   │   ├── components/              # Reusable components
│   │   ├── pages/
│   │   │   ├── Login.js            # Login page
│   │   │   ├── Register.js         # Registration page
│   │   │   └── Dashboard.js        # Main dashboard
│   │   ├── services/
│   │   │   └── api.js              # API client
│   │   ├── App.js                  # Main app component
│   │   ├── App.css                 # Styling
│   │   ├── index.js                # Entry point
│   │   └── index.css               # Global styles
│   └── package.json                # npm dependencies
│
├── frontend-desktop/                 # PyQt5 Desktop Frontend
│   ├── main.py                      # Main application
│   └── requirements.txt             # Python dependencies
│
├── docs/                            # Documentation
│   ├── API_DOCUMENTATION.md        # API reference
│   ├── SETUP_GUIDE.md              # Detailed setup
│   └── USER_GUIDE.md               # User manual
│
├── sample_equipment_data.csv        # Sample dataset
└── README.md                        # This file
```

##  Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- pip and virtualenv

###  **Demo Login Credentials**

**Username:** `admin`  
**Password:** `admin12345`

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Backend will run at: `http://localhost:8000`

### 2. Web Frontend Setup (React)

```bash
# Navigate to web frontend directory
cd frontend-web

# Install dependencies
npm install

# Start development server
npm start
```

Web app will open at: `http://localhost:3000`

### 3. Desktop Frontend Setup (PyQt5)

```bash
# Navigate to desktop frontend directory
cd frontend-desktop

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run desktop application
python main.py
```

##  Usage Guide

### First Time Setup

1. **Start the Backend Server** (required for both frontends)
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Register a New Account**
   - Web: Navigate to `http://localhost:3000/register`
   - Desktop: Click "Create New Account" button
   - Fill in username, email, and password (minimum 8 characters)

3. **Upload a Dataset**
   - Use the provided `sample_equipment_data.csv` or your own CSV file
   - Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature
   - Maximum 5 datasets per user (oldest automatically deleted)

4. **View Analytics**
   - View summary statistics
   - Interactive charts and graphs
   - Equipment type distribution
   - Parameter comparisons

5. **Generate Reports**
   - Click "Generate PDF Report" for any dataset
   - Professional PDF with statistics, charts, and equipment details

### CSV File Format

Your CSV file must have these columns (exact names):

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-A1,Reactor,150.5,25.3,180.2
Heat Exchanger-HX01,Heat Exchanger,200.0,15.8,120.5
Pump-P101,Pump,85.3,45.0,65.0
```

##  API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `GET /api/auth/user/` - Get current user

### Datasets
- `POST /api/upload/` - Upload CSV file
- `GET /api/datasets/` - List all user datasets
- `GET /api/datasets/{id}/` - Get dataset details
- `DELETE /api/datasets/{id}/delete/` - Delete dataset
- `GET /api/datasets/{id}/report/` - Generate PDF report

### Statistics
- `GET /api/statistics/` - Get user statistics

For detailed API documentation, see [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

##  Features Showcase

### Web Frontend (React)
- Modern, responsive design
- Real-time data visualization with Chart.js
- Interactive dashboard
- Mobile-friendly interface
- Beautiful gradient UI

### Desktop Frontend (PyQt5)
- Native desktop application
- Professional matplotlib charts
- Multi-tab interface
- File upload dialog
- Offline capability (with backend)

### Backend (Django REST)
- RESTful API design
- Token-based authentication
- Automatic data validation
- CSV processing with Pandas
- PDF generation with ReportLab
- SQLite database
- Admin panel at `/admin`

##  Security Features

- Token-based authentication
- Password hashing with Django's built-in security
- CSRF protection
- Input validation and sanitization
- Secure file upload handling
- SQL injection protection (Django ORM)

##  Sample Data

The project includes `sample_equipment_data.csv` with 20 equipment records:
- Multiple equipment types (Reactors, Heat Exchangers, Pumps, etc.)
- Realistic flowrate, pressure, and temperature values
- Ready for immediate testing

## 🛠️ Development

### Running Tests
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend-web
npm test
```

### Building for Production

**Backend:**
```bash
python manage.py collectstatic
gunicorn config.wsgi:application
```

**Web Frontend:**
```bash
npm run build
# Serve the 'build' folder with any static server
```

**Desktop Application:**
```bash
# Package with PyInstaller
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

##  Troubleshooting

### Common Issues

**Backend won't start:**
- Ensure virtual environment is activated
- Check if port 8000 is available
- Run migrations: `python manage.py migrate`

**Frontend connection errors:**
- Verify backend is running on port 8000
- Check CORS settings in Django settings.py
- Clear browser cache

**Desktop app login fails:**
- Ensure backend API is running
- Check API_BASE_URL in main.py
- Verify network connectivity

**CSV upload fails:**
- Check CSV format matches required columns
- Ensure file is not corrupted
- Verify column names are exact

##  Dependencies

### Backend (Python)
- Django 4.2.7
- djangorestframework 3.14.0
- django-cors-headers 4.3.1
- pandas 2.1.3
- numpy 1.26.2
- reportlab 4.0.7
- Pillow 10.1.0

### Web Frontend (JavaScript)
- react 18.2.0
- react-router-dom 6.20.0
- axios 1.6.2
- chart.js 4.4.0
- react-chartjs-2 5.2.0

### Desktop Frontend (Python)
- PyQt5 5.15.10
- requests 2.31.0
- pandas 2.1.3
- matplotlib 3.8.2
- numpy 1.26.2

##  User Credentials for Demo

After setting up, create your own user account. For admin access:

```bash
python manage.py createsuperuser
```

Admin panel: `http://localhost:8000/admin`

##  Additional Documentation

- [API Documentation](docs/API_DOCUMENTATION.md) - Complete API reference
- [Setup Guide](docs/SETUP_GUIDE.md) - Detailed installation steps
- [User Guide](docs/USER_GUIDE.md) - End-user manual

##  Project Highlights

 **Professional Code Quality**
- Clean, well-documented code
- Follows industry best practices
- Modular and maintainable architecture

 **Complete Feature Set**
- All required features implemented
- Additional enhancements included
- Production-ready application

 **User Experience**
- Intuitive interfaces
- Responsive design
- Professional styling

 **Security**
- Authentication and authorization
- Input validation
- Secure data handling

##  License

This project is created for the Intern Screening Task.

##  Developer Notes

This project demonstrates:
- Full-stack development skills
- RESTful API design
- Modern React development
- Desktop application development
- Data visualization
- PDF report generation
- Database design
- Authentication systems
- Professional UI/UX design

##  Future Enhancements

Potential additions:
- Real-time data streaming
- Advanced analytics (ML predictions)
- Export to Excel
- Email notifications
- Multi-user collaboration
- Cloud deployment
- Docker containerization
- Comprehensive test coverage

---



For questions or issues, please refer to the documentation files or create an issue in the repository.

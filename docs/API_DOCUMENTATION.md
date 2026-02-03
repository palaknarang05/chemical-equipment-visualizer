# API Documentation

## Chemical Equipment Visualizer REST API

Base URL: `http://localhost:8000/api`

## Authentication

All endpoints (except login and register) require authentication using Token Authentication.

### Token Format
Include the token in the Authorization header:
```
Authorization: Token <your-token-here>
```

---

## Authentication Endpoints

### 1. Register User

**Endpoint**: `POST /api/auth/register/`

**Description**: Create a new user account

**Authentication**: Not required

**Request Body**:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response** (201 Created):
```json
{
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "message": "User registered successfully"
}
```

**Error Response** (400 Bad Request):
```json
{
  "username": ["A user with that username already exists."],
  "email": ["Enter a valid email address."]
}
```

---

### 2. Login User

**Endpoint**: `POST /api/auth/login/`

**Description**: Authenticate user and get token

**Authentication**: Not required

**Request Body**:
```json
{
  "username": "johndoe",
  "password": "securepass123"
}
```

**Response** (200 OK):
```json
{
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "message": "Login successful"
}
```

**Error Response** (401 Unauthorized):
```json
{
  "error": "Invalid credentials"
}
```

---

### 3. Logout User

**Endpoint**: `POST /api/auth/logout/`

**Description**: Logout user and delete token

**Authentication**: Required

**Headers**:
```
Authorization: Token <your-token>
```

**Response** (200 OK):
```json
{
  "message": "Logout successful"
}
```

---

### 4. Get Current User

**Endpoint**: `GET /api/auth/user/`

**Description**: Get current authenticated user details

**Authentication**: Required

**Headers**:
```
Authorization: Token <your-token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

---

## Dataset Endpoints

### 5. Upload CSV File

**Endpoint**: `POST /api/upload/`

**Description**: Upload and process CSV file containing equipment data

**Authentication**: Required

**Headers**:
```
Authorization: Token <your-token>
Content-Type: multipart/form-data
```

**Request Body** (multipart/form-data):
```
file: <CSV file>
```

**CSV Format**:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-A1,Reactor,150.5,25.3,180.2
Heat Exchanger-HX01,Heat Exchanger,200.0,15.8,120.5
```

**Response** (201 Created):
```json
{
  "message": "File uploaded successfully",
  "dataset": {
    "id": 1,
    "filename": "equipment_data.csv",
    "upload_date": "2026-02-03T12:00:00Z",
    "total_equipment": 20,
    "avg_flowrate": 132.54,
    "avg_pressure": 24.67,
    "avg_temperature": 98.35,
    "username": "johndoe",
    "equipment": [
      {
        "id": 1,
        "equipment_name": "Reactor-A1",
        "equipment_type": "Reactor",
        "flowrate": 150.5,
        "pressure": 25.3,
        "temperature": 180.2
      },
      ...
    ]
  }
}
```

**Error Responses**:

400 Bad Request - No file:
```json
{
  "error": "No file provided"
}
```

400 Bad Request - Wrong format:
```json
{
  "error": "Only CSV files are allowed"
}
```

400 Bad Request - Missing columns:
```json
{
  "error": "Missing required columns: Type, Flowrate"
}
```

**Notes**:
- Only last 5 datasets are kept per user
- Older datasets are automatically deleted
- CSV must have exact column names (case-sensitive)

---

### 6. List All Datasets

**Endpoint**: `GET /api/datasets/`

**Description**: Get list of all datasets for current user

**Authentication**: Required

**Headers**:
```
Authorization: Token <your-token>
```

**Response** (200 OK):
```json
[
  {
    "id": 3,
    "filename": "latest_data.csv",
    "upload_date": "2026-02-03T14:30:00Z",
    "total_equipment": 15,
    "avg_flowrate": 125.5,
    "avg_pressure": 22.3,
    "avg_temperature": 95.2,
    "username": "johndoe"
  },
  {
    "id": 2,
    "filename": "equipment_data.csv",
    "upload_date": "2026-02-02T10:15:00Z",
    "total_equipment": 20,
    "avg_flowrate": 132.54,
    "avg_pressure": 24.67,
    "avg_temperature": 98.35,
    "username": "johndoe"
  }
]
```

**Note**: Returns datasets in descending order by upload date (newest first)

---

### 7. Get Dataset Details

**Endpoint**: `GET /api/datasets/{dataset_id}/`

**Description**: Get detailed information about a specific dataset

**Authentication**: Required

**Headers**:
```
Authorization: Token <your-token>
```

**URL Parameters**:
- `dataset_id` (integer): ID of the dataset

**Example**: `GET /api/datasets/1/`

**Response** (200 OK):
```json
{
  "dataset": {
    "id": 1,
    "filename": "equipment_data.csv",
    "upload_date": "2026-02-03T12:00:00Z",
    "total_equipment": 20,
    "avg_flowrate": 132.54,
    "avg_pressure": 24.67,
    "avg_temperature": 98.35,
    "username": "johndoe",
    "equipment": [
      {
        "id": 1,
        "equipment_name": "Reactor-A1",
        "equipment_type": "Reactor",
        "flowrate": 150.5,
        "pressure": 25.3,
        "temperature": 180.2
      },
      {
        "id": 2,
        "equipment_name": "Heat Exchanger-HX01",
        "equipment_type": "Heat Exchanger",
        "flowrate": 200.0,
        "pressure": 15.8,
        "temperature": 120.5
      },
      ...
    ]
  },
  "type_distribution": {
    "Reactor": 3,
    "Heat Exchanger": 3,
    "Pump": 3,
    "Compressor": 2,
    "Storage Tank": 1,
    "Mixer": 1,
    "Filter": 1,
    "Separator": 1,
    "Valve": 1,
    "Dryer": 1,
    "Crystallizer": 1,
    "Evaporator": 1,
    "Distillation Column": 1
  }
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "Dataset not found"
}
```

---

### 8. Delete Dataset

**Endpoint**: `DELETE /api/datasets/{dataset_id}/delete/`

**Description**: Delete a specific dataset

**Authentication**: Required

**Headers**:
```
Authorization: Token <your-token>
```

**URL Parameters**:
- `dataset_id` (integer): ID of the dataset to delete

**Example**: `DELETE /api/datasets/1/delete/`

**Response** (200 OK):
```json
{
  "message": "Dataset deleted successfully"
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "Dataset not found"
}
```

**Note**: Deletes both database records and uploaded CSV file

---

### 9. Generate PDF Report

**Endpoint**: `GET /api/datasets/{dataset_id}/report/`

**Description**: Generate and download PDF report for a dataset

**Authentication**: Required

**Headers**:
```
Authorization: Token <your-token>
```

**URL Parameters**:
- `dataset_id` (integer): ID of the dataset

**Example**: `GET /api/datasets/1/report/`

**Response** (200 OK):
- Content-Type: `application/pdf`
- Content-Disposition: `attachment; filename="report_1_20260203_120000.pdf"`
- Binary PDF data

**Error Response** (404 Not Found):
```json
{
  "error": "Dataset not found"
}
```

**Report Contents**:
- Report header with timestamp
- Dataset information
- Summary statistics table
- Equipment type distribution table
- Complete equipment details table

---

## Statistics Endpoint

### 10. Get User Statistics

**Endpoint**: `GET /api/statistics/`

**Description**: Get overall statistics for current user

**Authentication**: Required

**Headers**:
```
Authorization: Token <your-token>
```

**Response** (200 OK):
```json
{
  "total_datasets": 5,
  "total_equipment": 87,
  "username": "johndoe"
}
```

---

## Error Codes

| Status Code | Description |
|------------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Invalid or missing token |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error - Server error |

---

## Rate Limiting

Currently no rate limiting is implemented. For production deployment, consider implementing rate limiting using Django REST Framework's throttling classes.

---

## Data Models

### User Model
```python
{
  "id": integer,
  "username": string,
  "email": string,
  "first_name": string,
  "last_name": string
}
```

### Dataset Model
```python
{
  "id": integer,
  "user": integer (user_id),
  "filename": string,
  "upload_date": datetime,
  "file_path": string,
  "total_equipment": integer,
  "avg_flowrate": float,
  "avg_pressure": float,
  "avg_temperature": float
}
```

### Equipment Model
```python
{
  "id": integer,
  "dataset": integer (dataset_id),
  "equipment_name": string,
  "equipment_type": string,
  "flowrate": float,
  "pressure": float,
  "temperature": float
}
```

---

## Examples Using curl

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### Upload CSV
```bash
curl -X POST http://localhost:8000/api/upload/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -F "file=@equipment_data.csv"
```

### Get Datasets
```bash
curl -X GET http://localhost:8000/api/datasets/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Get Dataset Details
```bash
curl -X GET http://localhost:8000/api/datasets/1/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Generate Report
```bash
curl -X GET http://localhost:8000/api/datasets/1/report/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -o report.pdf
```

### Delete Dataset
```bash
curl -X DELETE http://localhost:8000/api/datasets/1/delete/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## Examples Using JavaScript (Axios)

### Setup Axios
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// Add token to all requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});
```

### Register
```javascript
const register = async () => {
  const response = await api.post('/auth/register/', {
    username: 'testuser',
    email: 'test@example.com',
    password: 'testpass123',
    password_confirm: 'testpass123'
  });
  return response.data;
};
```

### Upload File
```javascript
const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  return response.data;
};
```

### Get Datasets
```javascript
const getDatasets = async () => {
  const response = await api.get('/datasets/');
  return response.data;
};
```

---

## Examples Using Python (Requests)

### Setup
```python
import requests

BASE_URL = 'http://localhost:8000/api'
token = None

def set_token(new_token):
    global token
    token = new_token

def get_headers():
    headers = {}
    if token:
        headers['Authorization'] = f'Token {token}'
    return headers
```

### Register
```python
def register(username, email, password):
    url = f'{BASE_URL}/auth/register/'
    data = {
        'username': username,
        'email': email,
        'password': password,
        'password_confirm': password
    }
    response = requests.post(url, json=data)
    return response.json()
```

### Upload File
```python
def upload_csv(file_path):
    url = f'{BASE_URL}/upload/'
    headers = get_headers()
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, headers=headers, files=files)
    return response.json()
```

### Get Datasets
```python
def get_datasets():
    url = f'{BASE_URL}/datasets/'
    response = requests.get(url, headers=get_headers())
    return response.json()
```

---

## Security Considerations

1. **Token Security**: Store tokens securely (localStorage for web, secure storage for mobile)
2. **HTTPS**: Use HTTPS in production
3. **CORS**: Configure CORS properly for your domain
4. **File Validation**: Backend validates file types and content
5. **Rate Limiting**: Implement in production
6. **Input Validation**: All inputs are validated on the backend

---

## Testing the API

### Using Postman

1. Import the API endpoints
2. Set base URL: `http://localhost:8000/api`
3. For authenticated requests, add header:
   - Key: `Authorization`
   - Value: `Token YOUR_TOKEN_HERE`

### Using Django Rest Framework Browsable API

Visit any endpoint in your browser while logged in to use the interactive API interface:
- `http://localhost:8000/api/datasets/`
- `http://localhost:8000/api/statistics/`

---

## Support

For issues or questions about the API:
1. Check error messages in the response
2. Verify authentication token
3. Check request format
4. Review Django logs in the terminal

---

**API Version**: 1.0  
**Last Updated**: February 2026

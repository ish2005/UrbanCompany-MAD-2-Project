# UrbanClap - Household Services Platform (MAD-2 Project, IIT Madras)

[Youtube Tutorial Link](https://youtu.be/zytYrw2HVlk)  

## 📌 Project Overview
UrbanClap is a full-stack web application that connects service professionals with customers, providing a platform for booking and managing various home services. This project is part of **Modern Application Development - II (MAD-2)** at **IIT Madras**.

## 🚀 Features
### 1️⃣ User Management
- **Customers**: Book services and manage requests.
- **Service Professionals**: Offer services and manage work.
- **Administrators**: Manage the platform.

### 2️⃣ Service Management
- Service listing (name, description, base price, time required)
- Service categorization
- Dynamic pricing
- Availability tracking

### 3️⃣ Booking System
- Create service requests
- Real-time status tracking
- Payment integration
- Reviews & ratings

### 4️⃣ Location Management
- City-based service availability
- Pincode verification
- Service area management

### 5️⃣ Admin Dashboard
- User management (block/unblock users)
- Professional verification
- Service & city management
- Analytics & reporting
- CSV Export

### 6️⃣ Automated Notifications
- Daily reminders for pending services
- Monthly reports
- Email notifications using **Flask-Mail**
- Background task processing using **Celery**

## 🛠️ Tech Stack
### Backend
- **Flask** (Python)
- **SQLite + SQLAlchemy** ORM
- **JWT Authentication**
- **Redis** (Caching & Task Queue)
- **Celery** (Background tasks)
- **Flask-Mail** (Email Notifications)

### Frontend
- **Vue.js**
- **Vue Router** (Routing)
- **Bootstrap** (UI)
- **Axios** (API Integration)

## 🔒 Security Features
- JWT-based authentication
- Password hashing
- Role-based access control
- CORS protection
- Input validation

## 🏗️ Architecture
- **MVC Pattern** (Model-View-Controller)
- **API-First Design** (RESTful API endpoints)
- **Modular Structure**
- **Scalable Design**

---

## ⚡ Setup Guide
### 1️⃣ Start Redis Server
Ensure Redis is installed and running:
```sh
redis-server
```

### 2️⃣ Start MailHog
Start MailHog to capture email notifications:
```sh
mailhog
```

### 3️⃣ Backend Setup
Navigate to the backend directory:
```sh
cd backend
```
Create and activate a virtual environment:
```sh
python3 -m venv env
source env/bin/activate  # For Linux/macOS
env\Scripts\activate    # For Windows
```
Install dependencies:
```sh
pip install -r requirements.txt
```
Run the Flask application:
```sh
python app.py
```

### 4️⃣ Frontend Setup
Navigate to the frontend directory:
```sh
cd frontend
```
Install dependencies:
```sh
npm install
```
Start the development server:
```sh
npm run dev
```

## 🎯 Usage
- Access the frontend at **http://localhost:5173**
- Backend runs at **http://127.0.0.1:5000**
- MailHog UI: **http://localhost:8025**

## 📌 Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature-branch`
5. Create a pull request.

## 🔗 License
This project is licensed under the MIT License.


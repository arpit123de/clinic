# 🏥 Clinic Token System

A comprehensive web-based appointment booking and token management system for clinics, built with Flask and SQLAlchemy.

## ✨ Features

### Patient Features
- 📅 Online appointment booking with date and time slot selection
- 🎫 Automatic token generation for each appointment
- 📱 SMS notifications for appointment confirmation (Twilio integration)
- 👨‍⚕️ Multiple doctor selection
- 📋 View appointment status

### Admin Features
- 🔐 Secure admin authentication
- 📊 Dashboard with statistics (total, today, cancelled appointments)
- 👀 View all appointments with details
- 📈 Track booking trends by date
- 🔄 Real-time appointment status management

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Twilio account (for SMS notifications - optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/arpit123de/clinic.git
   cd clinic
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (Optional - for SMS)
   
   Create a `.env` file in the root directory:
   ```env
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Patient Portal: `http://127.0.0.1:5000`
   - Admin Panel: `http://127.0.0.1:5000/admin/login`

## 🔑 Default Admin Credentials

- **Username:** `admin`
- **Password:** `lavanys123`

⚠️ **Important:** Change the default password after first login!

## 📁 Project Structure

```
clinic-token-system/
├── app.py                      # Main Flask application
├── database.py                 # Database utilities (alternative)
├── requirements.txt            # Python dependencies
├── runtime.txt                # Python version for deployment
├── templates/                  # HTML templates
│   ├── index.html             # Patient booking page
│   ├── admin-login.html       # Admin login page
│   └── admin_dashboard.html   # Admin dashboard
├── static/                     # Static files (CSS, JS)
│   ├── style.css
│   └── script.js
└── instance/
    └── clinic.db              # SQLite database (auto-created)
```

## 🗄️ Database Schema

### Appointment Table
- `id` - Primary key
- `name` - Patient name
- `phone` - Contact number (10 digits)
- `doctor` - Selected doctor
- `date` - Appointment date
- `time_slot` - Time slot
- `token` - Auto-generated token number
- `status` - confirmed/cancelled
- `created_at` - Timestamp

### AdminUser Table
- `id` - Primary key
- `username` - Admin username
- `password_hash` - Hashed password

## 🌐 Deployment

### Deploy to Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your repository
4. Set environment variables (Twilio credentials)
5. Deploy!

**Build Command:** `pip install -r requirements.txt`

**Start Command:** `gunicorn app:app`

### Deploy to Heroku

```bash
heroku create your-app-name
git push heroku main
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
```

## 🔧 Configuration

### SMS Notifications
The system uses Twilio for SMS notifications. To enable:
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token
3. Add credentials to `.env` file
4. Update phone number in `app.py` (line 49)

### Database
- Default: SQLite (`clinic.db`)
- Can be configured to use PostgreSQL or MySQL by updating `SQLALCHEMY_DATABASE_URI`

## 📱 API Endpoints

### Patient Endpoints
- `GET /` - Home/booking page
- `POST /api/book` - Create new appointment

### Admin Endpoints
- `GET /admin/login` - Admin login page
- `POST /admin/login` - Admin authentication
- `GET /admin/dashboard` - View all appointments
- `GET /admin/logout` - Logout admin

## 🛡️ Security Features

- Password hashing using Werkzeug
- Session-based authentication
- CSRF protection
- Secure admin panel access
- Input validation

## 🐛 Troubleshooting

### Common Issues

**Issue:** Admin panel shows "Internal Server Error"
- **Solution:** Ensure template file is named `admin-login.html` (with hyphen)

**Issue:** SMS not sending
- **Solution:** Check Twilio credentials in `.env` file

**Issue:** Database not created
- **Solution:** Delete existing `clinic.db` and restart application

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Developer

Built with ❤️ for modern clinics

## 🙏 Acknowledgments

- Flask framework
- SQLAlchemy ORM
- Twilio API
- Bootstrap (for UI components)

---

**Note:** This is a demo application. For production use, implement additional security measures and customize according to your requirements.
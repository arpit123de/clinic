from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from twilio.rest import Client

# ---------------- BASIC SETUP ----------------
load_dotenv()

app = Flask(__name__)
app.secret_key = "super-secret-key-clinic-2025"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- MODELS ----------------
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    doctor = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)
    token = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="confirmed")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

# ---------------- INIT DB ----------------
with app.app_context():
    db.create_all()
    if not AdminUser.query.filter_by(username="admin").first():
        admin = AdminUser(
            username="admin",
            password_hash=generate_password_hash("lavanys123")
        )
        db.session.add(admin)
        db.session.commit()

# ---------------- TWILIO ----------------
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = "+19143505214"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(phone, message):
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=f"+91{phone}"
        )
    except Exception as e:
        print("SMS FAILED:", e)

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

# -------- ADMIN LOGIN (AUTO-LOGIN FIXED) --------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    # 🔥 IMPORTANT: page open hote hi session clear
    if request.method == "GET":
        session.clear()

    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = AdminUser.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Invalid username or password"

    return render_template("admin-login.html", error=error)

# -------- ADMIN DASHBOARD --------
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    appointments = Appointment.query.order_by(
        Appointment.date.desc(), Appointment.token
    ).all()

    stats = {
        "total": Appointment.query.count(),
        "today": Appointment.query.filter_by(
            date=datetime.now().strftime("%Y-%m-%d")
        ).count(),
        "cancelled": Appointment.query.filter_by(status="cancelled").count()
    }

    return render_template(
        "admin_dashboard.html",
        appointments=appointments,
        stats=stats
    )

# -------- ADMIN LOGOUT --------
@app.route("/admin/logout")
def admin_logout():
    session.clear()   # 🔥 full logout
    return redirect(url_for("admin_login"))

# -------- BOOKING API --------
@app.route("/api/book", methods=["POST"])
def api_book():
    data = request.get_json()

    name = data.get("name")
    phone = data.get("phone")
    doctor = data.get("doctor")
    date_ = data.get("date")
    time_slot = data.get("time")

    if not all([name, phone, doctor, date_, time_slot]):
        return jsonify(success=False, message="Missing fields"), 400

    token = Appointment.query.filter_by(date=date_).count() + 1

    ap = Appointment(
        name=name,
        phone=phone,
        doctor=doctor,
        date=date_,
        time_slot=time_slot,
        token=token
    )
    db.session.add(ap)
    db.session.commit()

    send_sms(phone, f"Your token {token} is confirmed for {date_}")

    return jsonify(success=True, token=token)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)

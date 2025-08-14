# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    inquiry_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    current_position = db.Column(db.String(100))
    current_company = db.Column(db.String(100))
    experience_years = db.Column(db.String(20))
    work_description = db.Column(db.Text)
    education = db.Column(db.String(100))
    field_of_study = db.Column(db.String(100))
    institution = db.Column(db.String(100))
    graduation_year = db.Column(db.String(10))
    technical_skills = db.Column(db.Text)
    soft_skills = db.Column(db.Text)
    certifications = db.Column(db.Text)
    resume_filename = db.Column(db.String(255))
    cover_letter_filename = db.Column(db.String(255))
    availability = db.Column(db.String(50))
    salary_expectation = db.Column(db.String(100))
    work_location = db.Column(db.String(50))
    additional_info = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "experience_years": self.experience_years,
            "technical_skills": self.technical_skills,
            "education": self.education,
            "city": self.city,
            "state": self.state,
            "resume_filename": self.resume_filename
        }
from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    ROLE_EMPLOYEE = 1
    ROLE_ADMIN = 2
    ROLE_VENDOR = 3


    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    company_name = db.Column(db.String(150), nullable=True)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Integer, default=ROLE_EMPLOYEE)


    hourly_rate = db.Column(db.Float, nullable=True)

    # 👇 Relationships
    timesheets = db.relationship('Timesheet', backref='user', lazy=True)
    vendor_links = db.relationship('EmployeeVendor', backref='employee', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# 🏢 Vendor model
class Vendor(db.Model):
    __tablename__ = 'vendor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    terms = db.Column(db.String(200))
    address = db.Column(db.String(200))

    invoices = db.relationship('Invoice', backref='vendor', lazy=True)
    employee_links = db.relationship('EmployeeVendor', backref='vendor', lazy=True)

class EmployeeVendor(db.Model):
    __tablename__ = 'employee_vendor'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id', ondelete='CASCADE'), nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)

    __table_args__ = (db.UniqueConstraint('employee_id', 'vendor_id', name='uq_employee_vendor_combo'),)

# Timesheet (already pointing to users.id — good!)
class Timesheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    project_description = db.Column(db.String(255))
    status = db.Column(db.String(20), default='Pending')


# 🧾 Invoice
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    month = db.Column(db.String(20), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Draft")  # Draft, Sent, Paid
    due_date = db.Column(db.Date)
    sent_date = db.Column(db.Date)
    paid_date = db.Column(db.Date)

    items = db.relationship('InvoiceItem', backref='invoice', lazy=True)
    payments = db.relationship('Payment', backref='invoice', lazy=True)

# InvoiceItem — update FK from employee.id → users.id
class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hours = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    employee = db.relationship('User')


# 💳 Payments
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    paid_on = db.Column(db.Date, default=datetime.utcnow)

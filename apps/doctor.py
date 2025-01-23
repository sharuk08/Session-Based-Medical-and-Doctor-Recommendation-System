from flask import Blueprint, request, redirect, url_for, session, flash, render_template
from models import DoctorModel
import csv

doctor = Blueprint("doctor", __name__)

@doctor.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('current_user'):
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = DoctorModel.check_user(email)

        if not user or not user.check_password(password):
            flash("Invalid email or password", "danger")
            return redirect(url_for("doctor.login"))
        
        session['current_user'] = user.to_json()
        session['role'] = 'DOCTOR'

        next_url = request.args.get("next")
        if next_url:
            return redirect(next_url)
        
        return redirect(url_for("main.index"))
    
    return render_template("doctor/login.html")

@doctor.route("/register", methods=['GET', 'POST'])
def register():
    depts = [
        "Dermatologist",
        "Aesthetic Dermatologist",
        "Cosmetologist",
        "Hair Transplant Surgeon",
        "Dermatosurgeon",
        "Trichologist",
        "Sexologist",
        "Pediatric Dermatologist",
        "Immunodermatologist",
        "Vascular Surgeon",
        "Andrologist",
        "Urologist",
        "Urological Surgeon",
        "Rheumatologist",
        "General Surgeon",
        "Proctologist",
        "Laparoscopic Surgeon",
        "Advanced Laparoscopic Surgeon",
        "Advanced Laser Proctologist",
        "Pulmonologist",
        "General Physician",
        "Joint Replacement Surgeon",
        "Orthopedic Surgeon",
        "Neurologist",
        "Neurosurgeon",
        "Geriatric Neurologist",
        "Gastroenterologist",
        "Endocrinologist",
        "Interventional Cardiologist",
        "Cardiologist",
        "Orthopaedic",
        "ENT (Ear Nose Throat)",
        "Neuro Surgeon"
    ]

    if session.get('current_user'):
        return redirect(url_for('main.index'))
    
    if request.method == 'POST': 
        age = request.form.get("age")
        fee = request.form.get("fee")
        city = request.form.get("city")
        email = request.form.get("email")
        state = request.form.get("state")
        gender = request.form.get("gender")
        degree = request.form.get("degree")
        address = request.form.get("address")
        username = request.form.get("username")
        password = request.form.get("password")
        hospital = request.form.get("hospital ")
        experience = request.form.get("experience")
        qualification = request.form.get("qualification")

        user = DoctorModel.check_user(email)
        if user:
            flash("user already exists with same email", "danger")
            return redirect(url_for("doctor.register"))
        
        new_doctor = DoctorModel(
            age = age,
            fee = fee,
            city = city,
            email = email,
            state = state,
            gender = gender,
            degree = degree,
            address = address,
            hospital = hospital,
            username = username,
            experience = experience,
            qualification = qualification,
        )
        new_doctor.set_password(password)
        new_doctor.save()


        flash("account created successfully", "success")
        return redirect(url_for("doctor.login"))
    
    return render_template("doctor/register.html", depts=depts)

@doctor.route("/profile")
def profile():    
    return render_template("doctor/profile.html")

@doctor.route("/insert")
def insert():
    csv_file_path = r'api\data\Doctors.csv'



    def insert_doctors_from_csv(file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            i = 1
            for row in reader:
                doctor = DoctorModel(
                    id = i,
                    username=row['Name'],
                    qualification=row['Specialization'],
                    experience=row['Experience (years)'],
                    degree=row['Degrees'],
                    address=row['Address'],
                    city=row['City'],
                    state=row['State'],
                    contact=row.get('contact', 'not provided'),
                    email=row.get('Email', 'not provided'),
                    rating= float(0 if row.get('Rating') == 'not provided' else row.get('Rating')),
                    fee=float(row['Consultation Fee (INR)']),
                    hospital=row['Hospital'],
                    timings=row['day and timings'],
                    gender='Unknown'  # Add gender if available in the data
                )
                

                doctor.set_password("doctor")
                doctor.save()
                i += 1

    insert_doctors_from_csv(csv_file_path)

    return "success"


@doctor.route("/search", methods=['GET', 'POST'])
def search():
    # Available departments
    depts = [
        "Dermatologist",
        "Aesthetic Dermatologist",
        "Cosmetologist",
        "Hair Transplant Surgeon",
        "Dermatosurgeon",
        "Trichologist",
        "Sexologist",
        "Pediatric Dermatologist",
        "Immunodermatologist",
        "Vascular Surgeon",
        "Andrologist",
        "Urologist",
        "Urological Surgeon",
        "Rheumatologist",
        "General Surgeon",
        "Proctologist",
        "Laparoscopic Surgeon",
        "Advanced Laparoscopic Surgeon",
        "Advanced Laser Proctologist",
        "Pulmonologist",
        "General Physician",
        "Joint Replacement Surgeon",
        "Orthopedic Surgeon",
        "Neurologist",
        "Neurosurgeon",
        "Geriatric Neurologist",
        "Gastroenterologist",
        "Endocrinologist",
        "Interventional Cardiologist",
        "Cardiologist",
        "Orthopaedic",
        "ENT (Ear Nose Throat)",
        "Neuro Surgeon"
    ]

    if request.method == 'POST':
        department = request.form.get("department", "").strip()
        rating = request.form.get("rating", "").strip()
        fee = request.form.get("fee", "").strip()

        min_rating = float(rating) if rating else None
        max_fee = float(fee) if fee else None

        if department and min_rating is not None and max_fee is not None:
            doctor = filter_all(department, min_rating, max_fee)
            se = f"departmant = {department}, rating >= {min_rating} and fee <= {max_fee}"

        elif department and min_rating is not None:
            doctor = filter_dept_rating(department, min_rating)
            se = f"departmant = {department} and rating >= {min_rating}"

        elif department and max_fee is not None:
            doctor = filter_dept_fee(department, max_fee)
            se = f"departmant = {department} and fee <= {max_fee}"

        elif min_rating is not None and max_fee is not None:
            doctor = filter_fee_rating(min_rating, max_fee)
            se = f"rating >= {min_rating} and fee <= {max_fee}"

        elif department:
            doctor = filter_doctors_by_departments(department)
            se = f"departmant = {department}"

        elif min_rating is not None:
            doctor = filter_doctors_by_rating(min_rating)
            se = f"rating >= {min_rating}"

        elif max_fee is not None:
            doctor = filter_doctors_by_fee(max_fee)
            se = f"fee <= {max_fee}"
        else:
            doctor = DoctorModel.query.all()
            se = "No filter applied"

        return render_template("doctor/find-doctor.html", depts=depts, doctor=doctor, cnt = len(doctor), se = se)

    # Default behavior for GET request
    d=DoctorModel.query.all()
    return render_template("doctor/find-doctor.html", depts=depts, doctor=d, cnt = len(d))


# Filter functions
def filter_all(department, min_rating, max_fee):
    return DoctorModel.query.filter(
        DoctorModel.qualification.like(f'%{department}%'),
        DoctorModel.rating >= min_rating,
        DoctorModel.fee <= max_fee
    ).all()

def filter_dept_rating(department, min_rating):
    return DoctorModel.query.filter(
        DoctorModel.qualification.like(f'%{department}%'),
        DoctorModel.rating >= min_rating
    ).all()

def filter_fee_rating(min_rating, max_fee):
    return DoctorModel.query.filter(
        DoctorModel.rating >= min_rating,
        DoctorModel.fee <= max_fee
    ).all()

def filter_dept_fee(department, max_fee):
    return DoctorModel.query.filter(
        DoctorModel.qualification.like(f'%{department}%'),
        DoctorModel.fee <= max_fee
    ).all()

def filter_doctors_by_departments(department):
    return DoctorModel.query.filter(
        DoctorModel.qualification.like(f'%{department}%')
    ).all()

def filter_doctors_by_rating(min_rating):
    return DoctorModel.query.filter(
        DoctorModel.rating >= min_rating
    ).all()

def filter_doctors_by_fee(max_fee):
    return DoctorModel.query.filter(
        DoctorModel.fee <= max_fee
    ).all()
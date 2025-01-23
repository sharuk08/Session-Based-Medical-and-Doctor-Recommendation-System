from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from models import UserModel, DoctorModel

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('current_user'):
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = UserModel.check_user(email)

        if not user or not user.check_password(password):
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.login"))
        
        session['current_user'] = user.to_json()
        session['role'] = 'PATIENT'

        next_url = request.args.get("next")
        if next_url:
            return redirect(next_url)
        
        return redirect(url_for("main.index"))
    
    return render_template("auth/login.html")

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if session.get('current_user'):
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        age = request.form.get("age")
        email = request.form.get("email")
        gender = request.form.get("gender")
        username = request.form.get("username")
        password = request.form.get("password")

        user = UserModel.check_user(email)

        if user:
            flash("user already exists with same email", "danger")
            return redirect(url_for("auth.register"))
        
        else:
            new_user = UserModel(
                age=age,
                email=email,
                gender=gender,
                username=username
            )
            new_user.set_password(password)
            new_user.save()

            flash("account created successfully", "success")
            return redirect(url_for("auth.login"))
    
    return render_template("auth/register.html")

@auth.route("/logout", methods=['GET', 'POST'])
def logout():
    if not session.get('current_user'):
        flash("login to access this route", "danger")
        return redirect(url_for('auth.login', next="logout"))
    
    session.pop('current_user', None)

    flash("successfully logged out", "success")
    return redirect(url_for('auth.login'))

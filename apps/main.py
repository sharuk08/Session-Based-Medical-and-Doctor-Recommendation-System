from flask import Blueprint, render_template, session, flash, redirect, url_for

main = Blueprint("main", __name__)

@main.route("/")
def index():
    if not session.get('current_user'):
        return render_template("index.2.html")
    
    return render_template("index.html")

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/contact")
def contact():
    return render_template("contact.html")

@main.route("/predict")
def predict():
    return render_template("predict.html")

@main.route("/profile")
def profile():
    if not session.get('current_user'):
        flash("login to access this route", "danger")
        return redirect(url_for('auth.login', next="/"))
    
    if session.get("role") == 'PATIENT':
        return redirect(url_for('main.user_profile'))
    
    if session.get("role") == 'DOCTOR':
        return redirect(url_for('doctor.profile'))

@main.route("/user/profile")
def user_profile():
       
    return render_template("profile.html")

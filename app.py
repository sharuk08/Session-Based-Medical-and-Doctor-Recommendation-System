from flask import Flask
from apps.auth import auth
from apps.main import main
from apps.doctor import doctor
from extensions import db, cors

# from api.api import api

app = Flask(__name__)

app.config.from_prefixed_env()

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']="this-is-secret"


db.init_app(app)
cors.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(doctor, url_prefix="/doctor")

# api.init_app(app)

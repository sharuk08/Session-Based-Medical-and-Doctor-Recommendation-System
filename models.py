from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
from uuid import uuid4

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(), primary_key=True, default=str(uuid4()))
    age = db.Column(db.Integer())
    email = db.Column(db.String())
    gender = db.Column(db.String())
    username = db.Column(db.String())
    password = db.Column(db.String()) 

    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_json(self):
        return {
            'id' : self.id,
            'age' : self.age,
            'email' : self.email,
            'gender' : self.gender,
            'username' : self.username,
            'password' : self.password
        }
    
    @classmethod
    def check_user(cls, email):
        user = cls.query.filter_by(email=email).one_or_none()
        return user
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

class DoctorModel(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.String(), primary_key=True, default=str(uuid4()))
    fee = db.Column(db.Float)
    age = db.Column(db.Integer())
    city = db.Column(db.String())
    email = db.Column(db.String())
    address = db.Column(db.Text())
    state = db.Column(db.String())
    rating = db.Column(db.Float)
    degree = db.Column(db.String())
    contact = db.Column(db.String())
    gender = db.Column(db.String())
    timings = db.Column(db.String())
    hospital = db.Column(db.String())
    username = db.Column(db.String())
    password = db.Column(db.String()) 
    experience = db.Column(db.String())
    qualification = db.Column(db.String())

    def __repr__(self):
        return f"<Doctor {self.username}>"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_json(self):
        return {
            "fee" :self.fee, 
            "age" :self.age, 
            "city" :self.city, 
            "email" :self.email, 
            "state" :self.state, 
            "degree" :self.degree, 
            "gender" :self.gender, 
            "rating": self.rating,
            "contact" :self.contact, 
            "timings" :self.timings, 
            "address" :self.address, 
            "hospital" :self.hospital, 
            "username" :self.username, 
            "password" :self.password,  
            "experience" :self.experience, 
            "qualification" :self.qualification, 
        }
    
    @classmethod
    def check_user(cls, email):
        user = cls.query.filter_by(email=email).one_or_none()
        return user
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

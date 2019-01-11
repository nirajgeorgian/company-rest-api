from flask_bcrypt import generate_password_hash
from db import db


class UserModel(db.Model):
    """This represent's base class for User Type Database."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    employee_id = db.relationship('EmployeeModel', cascade="all,delete", backref='user_employee', lazy=True, uselist=False)  # noqa E501
    admin_id = db.relationship('AdminModel', cascade="all,delete", backref='user_admin_id', lazy=True, uselist=False)

    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def hash_password(self):
        password = generate_password_hash(self.password, 10)
        self.password = password.decode("utf8", "ignore")
        return self

    def json(self):
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "username": self.username,
            "email": self.email
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

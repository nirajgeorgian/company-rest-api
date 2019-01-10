from db import db


class AdminModel(db.Model):
    """Default Overall Admin"""

    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    companies = db.relationship('CompanyModel', cascade="all,delete", backref='company', lazy=True)

    def __init__(self, **kwargs):
        super(AdminModel, self).__init__(**kwargs)

    def __repr__(self):
        return "<Admin: {}>".format(self.id)

    @classmethod
    def query_for_admin(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(user_id=_id).first()

    def get_admin(self, user):
        admin_id = self.id
        firstname = user.firstname
        lastname = user.lastname
        username = user.username
        email = user.email
        return {
            "id": user.id,
            "employee_id": admin_id,
            "firstname": firstname,
            "lastname": lastname,
            "username": username,
            "email": email
        }

    def json(self):
        return {
            "admin_id": self.id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

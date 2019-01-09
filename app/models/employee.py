from db import db


class EmployeeModel(db.Model):
    """This represent's Employee table"""

    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    isAdmin = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, **kwargs):
        super(EmployeeModel, self).__init__(**kwargs)

    def __repr__(self):
        return '<Employee {}>'.format(self.id)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(user_id=_id).first()

    def json(self):
        return {
            "isAdmin": self.isAdmin,
            "id": self.id
        }

    @classmethod
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

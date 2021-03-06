from app.db import db


class CompanyModel(db.Model):
    """Company Database Table."""

    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(120))
    company_employees = db.relationship('EmployeeModel', cascade="all,delete", backref='company_employee', lazy=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def __init__(self, **kwargs):
        super(CompanyModel, self).__init__(**kwargs)

    def __repr__(self):
        return '<Company %r>' % self.name

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, _name):
        return cls.query.filter_by(name=_name).first()

    @classmethod
    def delete_by_id(cls, _id):
        pass

    def json(self):
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

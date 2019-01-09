from db import db


class CompanyModel(db.Model):
    """Company Database Table."""

    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    company_employees = db.relationship('EmployeeModel', backref='company_employee', lazy=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def __init__(self, **kwargs):
        super(CompanyModel, self).__init__(**kwargs)

    def __repr__(self):
        return '<Company %r>' % self.name

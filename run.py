from app import create_app
from db import db

app = create_app()
db.init_app(app)

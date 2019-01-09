from os import getenv
from flask_migrate import Migrate

# import them so that they are discoverable in flask db migrate
from app.models import user, admin, company, employee
from db import db
from app import create_app

config_name = getenv('APP_SETTINGS', 'development')
app = create_app(config_name)
migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    port = int(getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

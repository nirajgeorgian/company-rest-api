from os import getenv
from app import create_app


if __name__ == '__main__':
    config_name = getenv('APP_SETTINGS', 'development')
    app = create_app(config_name)
    port = int(getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

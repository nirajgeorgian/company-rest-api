from os import getenv
from app import create_app


if __name__ == '__main__':
    app = create_app()
    port = int(getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

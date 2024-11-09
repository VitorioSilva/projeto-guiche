from flask import Flask
from config import configure_app
from routes.auth_routes import auth_blueprint
from routes.service_routes import service_blueprint

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
configure_app(app)

app.register_blueprint(auth_blueprint, url_prefix='/')
app.register_blueprint(service_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
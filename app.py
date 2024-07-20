from flask import Flask
from flask_restful import Api
from config import Config
from extensions import db, jwt, ma
from resources import SignupResource, LoginResource, ProfileResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app)
    api.add_resource(SignupResource, '/signup', methods=['POST'])
    api.add_resource(LoginResource, '/login', methods=['POST'])
    api.add_resource(ProfileResource, '/profile', methods=['GET', 'PUT'])

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

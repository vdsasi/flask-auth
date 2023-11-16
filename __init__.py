
from flask import Flask
import os
import flask_sqlalchemy
import flask_praetorian
import flask_cors
from .views import auth_blue_print

db = flask_sqlalchemy.SQLAlchemy()
guard = flask_praetorian.Praetorian()
cors = flask_cors.CORS()

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(auth_blue_print)

    from .models.User import User

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models/database.db'
    app.config['SECRET_KEY'] = 'top secret'
    app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
    app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['debug'] = True

    # Initialize db, guard, and cors with the app
    guard.init_app(app, User)
    db.init_app(app)
    cors.init_app(app)


    with app.app_context():
        db.create_all()

    @app.route('/')
    def hello_world():
        return 'Hello, newone'

    return app

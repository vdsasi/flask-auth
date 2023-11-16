from flask import Blueprint, request
import flask_praetorian
import flask

auth_blue_print = Blueprint('api_blue_print', __name__)

@auth_blue_print.route('/api')
def hello():
    return "Hello from api"

@auth_blue_print.route('/api/login', methods=['POST'])
def login():
    from api import guard
    from api.models.User import User

    req = flask.request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # Password is correct, issue a JWT token
        ret = {'access_token': guard.encode_jwt_token(user)}
        return ret, 200
    else:
        # Invalid username or password
        return {'message': 'Invalid username or password'}, 401

@auth_blue_print.route('/api/refresh', methods=['POST'])
def refresh():
    print("refresh request")
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200

@auth_blue_print.route('/api/protected')
@flask_praetorian.auth_required
def protected():
    return {'message': f'protected endpoint (allowed user {flask_praetorian.current_user().username})'}

@auth_blue_print.route('/api/register', methods=['POST'])
def register():
    from api.models.User import User
    from api import db

    print(request)

    username = request.json['username']
    password = request.json['password']

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return {'message': 'Username already exists'}, 400
    
    new_user = User(username=username)
    new_user.set_password(password)  
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'User registered successfully'}, 201


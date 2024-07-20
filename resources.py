from flask import request, jsonify
from flask_restful import Resource
from models import User
from extensions import db, jwt
from schemas import user_schema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from flask import request
from flask_restful import Resource
from models import User
from extensions import db
from schemas import user_schema

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        address = data.get('address')
        phone = data.get('phone')
        profile_picture = data.get('profile_picture')

        if User.query.filter_by(email=email).first():
            return {"message": "User already exists"}, 400

        new_user = User(
            email=email,
            name=name,
            address=address,
            phone=phone,
            profile_picture=profile_picture
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user), 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200
        return {"message": "Invalid credentials"}, 401

class ProfileResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return user_schema.dump(user), 200

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()

        user.name = data.get('name', user.name)
        user.address = data.get('address', user.address)
        user.phone = data.get('phone', user.phone)
        user.profile_picture = data.get('profile_picture', user.profile_picture)

        new_email = data.get('email')
        if new_email and new_email != user.email:
            if User.query.filter_by(email=new_email).first():
                return {"message": "Email already in use"}, 400
            user.email = new_email

        db.session.commit()
        return user_schema.dump(user), 200

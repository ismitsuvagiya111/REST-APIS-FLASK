from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
    create_refresh_token,
    get_jwt_identity
)
from passlib.hash import pbkdf2_sha256
from flask import render_template, request, jsonify
from db import db
from models import UserModel, BlocklistModel
from schemas import UserSchema

blp = Blueprint("users", __name__, description="Operations on Users")



@blp.route("/register", methods=['GET', 'POST'])
class UserRegister(MethodView):
    def get(self):
        return render_template('register.html')

    #@blp.arguments(UserSchema)
    def post(self):
        # Get user data from the form
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if username already exists
        if UserModel.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 409

        # Check if passwords match
        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400

        hashed_password = pbkdf2_sha256.hash(password)
        # Create a new user
        new_user = UserModel(
            username=username,
            password=hashed_password
        )
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), 201
   
@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        
        abort(401, message ="Invalid Credentials")

@blp.route('/refresh')
class Token_refresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        blocklist_entry = BlocklistModel(token=jti)
        db.session.add(blocklist_entry)
        db.session.commit()
        return {"access_token": new_token}
            

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        blocklist_entry = BlocklistModel(token=jti)
        db.session.add(blocklist_entry)
        db.session.commit()
        return {"message": "Successfully logged out"}, 200


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully."}
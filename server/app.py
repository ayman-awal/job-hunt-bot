import os
from dotenv import load_dotenv
from models import db
from models.User import User
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
import pymysql
from datetime import timedelta
pymysql.install_as_MySQLdb()

load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES")))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

db.init_app(app)

jwt = JWTManager(app)

with app.app_context():
    db.create_all()


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    roles = data.get('roles')
    experienceLevel = data.get('experienceLevel')
    skills = data.get('skills')
    keywordsToAvoid = data.get('keywordsToAvoid')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    new_user = User(
        name=name,
        email=email,
        roles=roles,
        experienceLevel=experienceLevel,
        skills=skills,
        keywordsToAvoid=keywordsToAvoid
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit() 

    return jsonify({"message": "User created successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "Account with this email does not exist"}), 400
    else:
        if user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"message": "Wrong password"}), 400

@app.route('/users', methods=['GET'])
def get_users_data():
    users = User.query.all()

    if not users:
        return jsonify({"message": "No users found"}), 400
    
    user_list = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "roles": user.roles,
            "experienceLevel": user.experienceLevel,
            "skills": user.skills,
            "keywordsToAvoid": user.keywordsToAvoid
        }
        for user in users
    ]
    
    return jsonify(user_list), 200


if __name__ == '__main__':
    app.run(debug=True)

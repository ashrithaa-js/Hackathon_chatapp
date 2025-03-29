import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from cryptography.fernet import Fernet

# Flask App Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Encryption Key
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    receiver = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Authentication Routes
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        token = create_access_token(identity=user.username)
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

# Secure Messaging API
@app.route('/chat/send', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json()
    sender = get_jwt_identity()  # Get logged-in user
    encrypted_msg = cipher.encrypt(data['message'].encode()).decode()
    msg = Message(sender=sender, receiver=data['receiver'], content=encrypted_msg)
    db.session.add(msg)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully'})

@app.route('/chat/messages', methods=['GET'])
@jwt_required()
def get_messages():
    receiver = get_jwt_identity()  # Get logged-in user
    messages = Message.query.filter_by(receiver=receiver).all()
    decrypted_messages = [{'sender': msg.sender, 'message': cipher.decrypt(msg.content.encode()).decode()} for msg in messages]
    return jsonify(decrypted_messages)

# File Upload API
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/file/upload', methods=['POST'])
@jwt_required()
def upload_file():
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    return jsonify({'message': 'File uploaded'})

@app.route('/file/files', methods=['GET'])
@jwt_required()
def list_files():
    return jsonify({'files': os.listdir(app.config['UPLOAD_FOLDER'])})

# Frontend
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

# Run App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

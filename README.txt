Secure Chat App

This project is a secure chat application with features like user authentication, end-to-end encrypted messaging, and secure file sharing.

Tech Stack

Backend: Flask, Flask-SQLAlchemy, Flask-JWT-Extended

Encryption: Cryptography (Fernet)

Database: SQLite

Frontend: HTML

Prerequisites

Python (version 3.x)

pip (Python package installer)

Installation

Clone the repository or download the project files.

Navigate to the project directory:

cd secure-chat-app

Install dependencies:

pip install flask flask_sqlalchemy flask_jwt_extended cryptography

Running the Application

Initialize the database:

python app.py

The server will start at:

http://127.0.0.1:5000

API Endpoints

Authentication

Register: POST /auth/register

Payload: {"username": "testuser", "password": "testpass"}

Login: POST /auth/login

Payload: {"username": "testuser", "password": "testpass"}

Response: { "token": "<JWT Token>" }

Messaging

Send Message: POST /chat/send (Requires JWT)

Headers: { "Authorization": "Bearer <JWT Token>" }

Payload: { "receiver": "user2", "message": "Hello!" }

Get Messages: GET /chat/messages (Requires JWT)

Headers: { "Authorization": "Bearer <JWT Token>" }

File Upload

Upload File: POST /file/upload (Requires JWT)

Form-data: file

List Files: GET /file/files (Requires JWT)

Notes

All messages are encrypted with Fernet before storage and decrypted when fetched.

The encryption key is generated every time the app restarts, meaning stored messages won't be accessible after a restart.

Future Enhancements

Implement persistent encryption key storage.

Add password hashing for user authentication.

Improve frontend with React.js or other frameworks

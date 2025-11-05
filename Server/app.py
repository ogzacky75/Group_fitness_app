import os
from flask import Flask, jsonify, session
from flask_cors import CORS
from flask_restful import Api
from flask_migrate import Migrate
from flask_session import Session
from models import db, User

from routes.User_routes import user_bp
from routes.Workout_routes import  workout_bp
from routes.Progress_routes import progress_bp
from routes.Friends_routes import friends_bp
from routes.Workout_session_routes import workout_session_bp


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_P9IURFYvT5uG@ep-weathered-recipe-adiyrtye-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev_secret")

    db.init_app(app)
    Migrate(app, db)

    app.config["SESSION_TYPE"] = "sqlalchemy"
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = False
    app.config['SESSION_KEY_PREFIX'] = 'fitfam:'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config["SESSION_SQLALCHEMY"] = db
    Session(app)

    CORS(app, 
         origins=[
             "http://localhost:3000",
             "http://127.0.0.1:3000",
             'https://fit-fam.onrender.com',
             'https://group-fitness-app.onrender.com',
             'https://fit-fam-eight.vercel.app',
             'https://fit-fam-six.vercel.app'], 
         supports_credentials=True, 
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
    Api(app)

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(workout_bp, url_prefix="/workouts")
    app.register_blueprint(progress_bp, url_prefix="/progress")
    app.register_blueprint(friends_bp, url_prefix="/friends")
    app.register_blueprint(workout_session_bp, url_prefix="/workout-sessions")

    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy", "message": "Server is running"}), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not Found"}), 404
    
    @app.route('/version')
    def version():
        return jsonify({"message": "Deployed on Sep 30 2025 at 12:00PM", "status": "new code"})


    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal Server Error"}), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
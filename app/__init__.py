from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    from .models import User

    CORS(app)

        # register blue prints
        #authentication blueprint
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    #patient blueprint
    from .patients import User_blueprint
    app.register_blueprint(User_blueprint)
    
    #doctor blueprint 
    from .doctor import Doctor_blueprint
    app.register_blueprint(Doctor_blueprint)
    return app


    


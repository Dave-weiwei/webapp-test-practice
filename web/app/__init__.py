from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # PostgreSQL 資料庫連線設定（使用 .env 或預設值）
    
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        db_url = (
            f"postgresql://{os.getenv('PG_USER', 'postgres')}:"
            f"{os.getenv('PG_PASSWORD', 'postgres')}@"
            f"{os.getenv('PG_HOST', 'localhost')}:"
            f"{os.getenv('PG_PORT', '5432')}/"
            f"{os.getenv('PG_DB', 'testdb')}"
        )
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv("SECRET_KEY", "jlbXz5pqIWztluSG6hsOKUMgTXuGny3K")
    #
    db.init_app(app)
    migrate.init_app(app, db)
    #
    from . import models
    #
    from .routes.main import main_bp
    app.register_blueprint(main_bp)
    
    #auth Blueprint
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    #member Blueprint
    from .routes.member import member_bp
    app.register_blueprint(member_bp)
    
    #calculator Blueprint
    from .routes.calculator import calculator_bp
    app.register_blueprint(calculator_bp)
    
    from .routes.product import product_bp
    app.register_blueprint(product_bp)
    
    from .routes.admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from .routes.api import api_bp
    app.register_blueprint(api_bp)

    return app
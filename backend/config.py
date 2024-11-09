import os
from dotenv import load_dotenv

load_dotenv()

def configure_app(app):
    app.secret_key = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")
    app.config["JWT_ALGORITHM"] = "HS256"
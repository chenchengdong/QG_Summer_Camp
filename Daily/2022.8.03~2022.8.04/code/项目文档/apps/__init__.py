from flask import Flask
import sys
sys.path.append("..")
from Control.Model import Model

model = Model()
from .book import book_bp
from .func import func_bp
from .user import user_bp
from .edit import edit_bp
import sys

def create_app():
    global model
    model = Model()
    app = Flask(__name__)

    app.register_blueprint(book_bp)
    app.register_blueprint(func_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(edit_bp)

    app.config["ENV"] = "development"

    return app

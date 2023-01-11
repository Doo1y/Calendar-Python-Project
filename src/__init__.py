from flask import Flask
from src import routes
import os

src = Flask(__name__)
src.config.update({'SECRET_KEY': os.environ.get('SECRET_KEY')})
src.register_blueprint(routes.bp)
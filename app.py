from flask import Flask
from flask_restful import Api

from apps.urls import register_urls
from apps.models import db


api = Api()

def create_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    
    register_urls(api)
    api.init_app(app)
    db.init_app(app)

    return app
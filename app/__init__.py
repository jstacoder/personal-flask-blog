import os
from flask import Flask, Blueprint, request, g
from dotenv import load_dotenv 
from flask_apps import FlaskApps
from flask_babel import Babel as FlaskBabel
from flask_mailgun import Mailgun
from flask_mailman import Mail
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from .api import api
from .apps.user import UserBlueprint
from .apps.comment import CommentBlueprint
from .apps.blog import BlogBlueprint
from .apps.address import EmailBlueprint
from .auth import security, user_datastore
from .models.base import session as db_session
from .views import index
from .admin import admin

load_dotenv(".flaskenv")

def create_app(*args, **kwargs):
    app = Flask(__name__)

    app.config.from_prefixed_env()
    app.add_url_rule("/api", view_func=index.IndexView.as_view("index"))
    app.add_url_rule("/hello/<name>", view_func=index.NameView.as_view("name"))
    FlaskBabel(app)
    admin.init_app(app)
    security.init_app(app, user_datastore)
    mailgun = Mailgun()
    mail = Mail()
    mail.init_app(app)
    mailgun.init_app(app)
    # app.wsgi_app = app(api)
    # frontend = Flask('app')

    app.register_blueprint(UserBlueprint, url_prefix="/user/" , name="user_bp")
    app.register_blueprint(CommentBlueprint, url_prefix="/comments/" , name="comment_bp")
    app.register_blueprint(BlogBlueprint, url_prefix="/blogs/" , name="blog_bp")
    app.register_blueprint(EmailBlueprint, url_prefix='/emails/', name="email_bp")
 #   FlaskApps(app)

    app.teardown_appcontext(lambda exc: db_session.close())
    app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}
    app.config["SECURITY_PASSWORD_SALT"] = str(os.environ.get("FLASK_SECURITY_PASSWORD_SALT"))
    return app

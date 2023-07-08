from flask import Flask, request, jsonify
from flask_babel import Babel
from app.config import LANGUAGES


def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())


app = Flask(__name__)
babel = Babel(app, locale_selector=get_locale)

app.config["BABEL_DEFAULT_LOCALE"] = "ru"


from app import views
from app.service import admin_api
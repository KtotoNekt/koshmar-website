from flask import render_template, make_response
from flask_babel import get_locale

from app.service.bot import get_user_from_token, get_user_self, get_user_profile, get_messages_from_channel, get_messages_from_user

from app.config import PROJECTS
from app import app, request, jsonify

from pprint import pprint


@app.route("/")
def home():
    locale = str(get_locale())
    if locale == "None":
        locale = "en"
    
    if locale != "en":
        filter_projects = []
        for project in PROJECTS:
            _pr = project.copy()
            if project.get("description-translations"):
                if project["description-translations"].get(locale):
                    _pr["description"] = project["description-translations"][locale]
            filter_projects.append(_pr)
    else:
        filter_projects = PROJECTS.copy()

    return render_template("index.html", user=get_user_self(), projects=filter_projects)





@app.route("/api/get/self")
def get_self_user():
    user = get_user_self()
    return jsonify(user)


@app.route("/api/get/<user_id>/card")
def get_card_profile_user(user_id):
    headers = {
        "Authorization": request.cookies.get("token")
    }

    user = get_user_profile(user_id=user_id, headers=headers)
    if user["user"] == None:
        return "Не найден пользователь с ID " + user_id

    return render_template("card-profile.html", user=user)


@app.route("/api/get/messages/<channel_id>")
def get_messages(channel_id):
    token = request.cookies.get("token")

    if request.args["referer"] == "friends":
        messages = get_messages_from_user(token, channel_id)
    else:
        messages = get_messages_from_channel(token, channel_id)

    messages.reverse()

    return render_template("chat.html", messages=messages)


@app.route("/api/get/guild")
def get_guild():
    return "Полноценный сайт для этого в разработке"


@app.route("/api/get/token", methods=["POST"])
def get_info_from_token():
    token = request.form["token"]
    user = get_user_from_token(token)

    resp = make_response(jsonify(user))

    if user.get("user") != None or user.get("bot"):
        resp.set_cookie("token", token)

    return resp
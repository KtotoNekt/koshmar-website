from dotenv import load_dotenv
from os import getenv

import json


load_dotenv()

LANGUAGES = {
    'de': 'Deutsch',
    "ru": "Russian"
}

TOKEN = getenv("TOKEN")

SELF_USER_ID = getenv("SELF_USER_ID")
LOGIN = getenv("LOGIN")
PASSWORD = getenv("PASSWORD")

with open("projects.json", "r") as fr:
    PROJECTS = json.load(fr)


URLS_API = {
    "api": "https://discord.com/api/",
    "cdn": "https://cdn.discordapp.com/",
    "channels": "https://discord.com/api/channels/",
    "users": "https://discord.com/api/users/",
    "guild_get": "https://discord.com/api/guilds/",
    "self_user": "https://discord.com/api/users/@me",
    "avatars": "https://cdn.discordapp.com/avatars/",
    "banners": "https://cdn.discordapp.com/banners/",
    "guilds": "https://discord.com/api/users/@me/guilds",
    "friends": "https://discord.com/api/users/@me/relationships",
    "dm-channels": "https://discord.com/api/users/@me/channels"
}

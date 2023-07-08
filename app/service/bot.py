import requests as req
from app.config import TOKEN, URLS_API, SELF_USER_ID
from datetime import datetime


self_headers = {
    'Authorization': TOKEN
}


def set_str_on_html_tag(string: str, tag: str, symb: str):
    list_tag = list(tag)
    list_tag.insert(1, "/")
    
    end_tag = "".join(list_tag)
    count = 0
    for i in range(string.count(symb)):
        if count == 0:
            string = string.replace(symb, tag, 1)
            count += 1
        else:
            string = string.replace(symb, end_tag, 1)
            count = 0
    
    return string
    



    
def set_string_on_html_url(string: str, index_start: int):
    index_end_1 = string.find(" ", index_start)
    index_end_2 = string.find("<", index_start)

    if index_end_1 != -1 and index_end_2 != -1:
        index_end = min(index_end_1, index_end_2)+1
    else:
        index_end = len(string)+1

    url = string[index_start:index_end-1]

    list_string = list(string)

    list_string.insert(index_start, f"<a href='{url}'>")
    list_string.insert(index_end, f"</a>")

    string = "".join(list_string)

    return string, index_end
    
    
def count_http_or_https(bio: str, start_url: str):
    count = bio.count(start_url)
    old_index_start = 0

    for i in range(count):
        index_start = bio.find(start_url, old_index_start)

        if index_start != -1:
            bio, old_index_start = set_string_on_html_url(bio, index_start)

    return bio
    
    
def edit_string_on_html_urls(bio: str):
    bio = count_http_or_https(bio, "http://")
    bio = count_http_or_https(bio, "https://")
    
    return bio
    
    
def edit_user_bio(bio: str):
    bio = bio.replace("\n", "<br>")
    bio = set_str_on_html_tag(bio, "<b>", "**")
    bio = set_str_on_html_tag(bio, "<i>", "*")
    bio = set_str_on_html_tag(bio, "<i>", "*")
    bio = set_str_on_html_tag(bio, "<span class=\"spoiler-text\" tabindex=\"0\">", "||")
    bio = edit_string_on_html_urls(bio)
    
    return bio




def get_suppl_info(data: dict):
    if data["avatar"]:
        data["avatar_url"] = f"{URLS_API['avatars']}{data['id']}/{data['avatar']}"
    else:
        if data["discriminator"] == "0":
            index = (int(data['id']) >> 22) % 6
        else:
            index = int(data["discriminator"]) % 5

        data["avatar_url"] = f"{URLS_API['cdn']}embed/avatars/{index}.png"

    if data["banner"]:
        data["banner_url"] = f"{URLS_API['banners']}{data['id']}/{data['banner']}?size=512"

    data["creation_date"] = datetime.utcfromtimestamp(((int(data["id"]) >> 22) + 1420070400000) / 1000).strftime('%b. %d, %Y')
    
    if not data["banner_color"]:
        data["banner_color"] = "black"



def get_url_badge_icon(badge_icon_hash: str):
    return f"https://cdn.discordapp.com/badge-icons/{badge_icon_hash}.png"


def get_badges(data: dict):
    badges = data.get("badges")

    if badges == None:
        data["badges"] = []
    else:
        for i in range(len(badges)):
            badges[i]["icon_url"] = get_url_badge_icon(badges[i]["icon"])

        data["badges"] = badges


def get_user_info_with_url_api(url, headers):
    resp = req.get(url, headers=headers).json()
    return resp



def get_user_profile(user_id: str, headers: dict):
    resp = req.get(URLS_API["users"] + user_id + "/profile", headers=headers)

    if resp.status_code == 200:
        data = resp.json()
        
        data["user"]["bio"] = edit_user_bio(data["user"]["bio"])
        get_suppl_info(data["user"])
        get_badges(data)

        return data

    return {"user": None}


def get_user_self():
    profile = get_user_profile(SELF_USER_ID, self_headers)
    return profile


def get_user_from_token(token: str):
    headers = {'Authorization': token}
    user = req.get(URLS_API["self_user"], headers=headers)

    if user.status_code != 200:
        headers = {'Authorization': "Bot " + token}
        user = req.get(URLS_API["self_user"], headers=headers)
        if user.status_code != 200:
            return {"user": None}
        
        data = user.json()
        get_suppl_info(data)
        get_badges(data)

        data["friends"] = []
        data["dm-channels"] = get_user_info_with_url_api(URLS_API["dm-channels"], headers)
        data["guilds"] = get_user_info_with_url_api(URLS_API["guilds"], headers)
        
        return data

    user_data = user.json()

    profile = get_user_profile(user_id=user_data["id"], headers=headers)

    profile["friends"] = get_user_info_with_url_api(URLS_API["friends"], headers)
    profile["dm-channels"] = get_user_info_with_url_api(URLS_API["dm-channels"], headers)
    profile["guilds"] = get_user_info_with_url_api(URLS_API["guilds"], headers)

    profile["email"] = user_data["email"]
    profile["phone"] = user_data["phone"]
    profile["locale"] = user_data["locale"]


    return profile


def get_messages_from_user(token, user_id):
    headers = {'Authorization': token}

    dm_channel = req.post(URLS_API['self_user']+"/channels", json={"recipient_id": user_id}, headers=headers).json()

    return get_messages_from_channel(token, dm_channel["id"])


def get_messages_from_channel(token, channel_id):
    headers = {'Authorization': token}

    messages = req.get(URLS_API["channels"]+channel_id+"/messages", headers=headers).json()
    
    return messages
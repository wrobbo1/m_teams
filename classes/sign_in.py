from bs4 import BeautifulSoup as bs
import requests
import time
import datetime
import json
import random
import utils

class Config:
    def __init__(self):
        with open('config.json', 'r') as c:
            j = json.load(c)
            self.email = j["email"]
            self.password = j["password"]
            self.message = j["message"]
            self.time = j["time"]


c = Config()
log = utils.Logger()

def login():
    s = requests.Session()
    s.headers = utils.get_headers()

    sts_page = s.get("https://sts.platform.rmunify.com/Account/SignIn/kingstongrammar")
    html = bs(sts_page.text, "html.parser")

    form = html.find('form')

    rvt = form.find('input', {"name": "__RequestVerificationToken"})["value"]
    return_url = form.find('input', {"name": "returnUrl"})["value"]

    payload = {
        "__RequestVerificationToken": rvt,
        "UserName": c.email,
        "username2TxtGloLgn": c.email,
        "Password": c.password,
        "password2TxtGloLgn": c.password,
        "returnUrl:": return_url
    }

    login_post = s.post("https://sts.platform.rmunify.com/Account/SignIn/kingstongrammar", data=payload, allow_redirects=True)

    if "signInErrorMessage" in login_post.text:
        log.error("Failed to sign in.")
    else:
        log.success("Successfully signed in.")
        teams = s.get("https://teams.microsoft.com/", allow_redirects=True)
        print(teams.text)


login()
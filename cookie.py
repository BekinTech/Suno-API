# -*- coding:utf-8 -*-

import os
import time
from http.cookies import SimpleCookie
from threading import Thread

import requests
import firebase_admin
from firebase_admin import firestore


from utils import COMMON_HEADERS


class SunoCookie:
    def __init__(self):
        self.cookie = SimpleCookie()
        self.session_id = None
        self.token = None

    def load_cookie(self, cookie_str):
        self.cookie.load(cookie_str)

    def get_cookie(self):
        return ";".join([f"{i}={self.cookie.get(i).value}" for i in self.cookie.keys()])

    def set_session_id(self, session_id):
        self.session_id = session_id

    def get_session_id(self):
        return self.session_id

    def get_token(self):
        return self.token

    def set_token(self, token: str):
        self.token = token


app = firebase_admin.initialize_app()
db = firestore.client()
doc_ref = db.collection("ifai").document("SunoAI")
doc = doc_ref.get()
doc_data = doc.to_dict()

sess=doc_data.get('SESSION_ID')
cokk=doc_data.get('COOKIE')
printf(sess)
printf(cokk)

suno_auth = SunoCookie()
suno_auth.set_session_id(sess)
suno_auth.load_cookie(cokk)


def update_token(suno_cookie: SunoCookie):
    headers = {"cookie": suno_cookie.get_cookie()}
    headers.update(COMMON_HEADERS)
    session_id = suno_cookie.get_session_id()

    resp = requests.post(
        url=f"https://clerk.suno.com/v1/client/sessions/{session_id}/tokens?_clerk_js_version=4.72.0-snapshot.vc141245",
        headers=headers,
    )

    resp_headers = dict(resp.headers)
    set_cookie = resp_headers.get("Set-Cookie")
    suno_cookie.load_cookie(set_cookie)
    token = resp.json().get("jwt")
    suno_cookie.set_token(token)
    # print(set_cookie)
    # print(f"*** token -> {token} ***")


def keep_alive(suno_cookie: SunoCookie):
    while True:
        try:
            update_token(suno_cookie)
        except Exception as e:
            print(e)
        finally:
            time.sleep(5)


def start_keep_alive(suno_cookie: SunoCookie):
    t = Thread(target=keep_alive, args=(suno_cookie,))
    t.start()


start_keep_alive(suno_auth)

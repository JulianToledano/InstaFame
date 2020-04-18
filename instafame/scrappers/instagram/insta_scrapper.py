"""Instagram users info scrapper"""
import hashlib
import string
import random
from pathlib import Path
from instagram_web_api import Client as WebClient
from instagram_private_api import Client as PrivateClient


class InstagramWebClient(WebClient):
    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = ''.join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode())


class InstagramScrapper:
    # TODO: save settings to reconnect.
    def __init__(self, username, password, login=True):
        self._web_api = InstagramWebClient(auto_patch=True,
                                           drop_incompat_keys=False)
        if login:
            self._authed_web_api = PrivateClient(auto_patch=True,
                                                 authenticate=True,
                                                 username=username,
                                                 password=password)

    def user_followers(self, user_id, max_to_retrieve=500, next_max_id=None):
        rank_token = self._authed_web_api.generate_uuid()
        followers = []
        if next_max_id is None:
            results = self._authed_web_api.user_followers(user_id, rank_token)
            followers.extend(results.get('users', []))
            next_max_id = results.get('next_max_id')
        while next_max_id:
            results = self._authed_web_api.user_followers(user_id,
                                                          rank_token,
                                                          max_id=next_max_id)
            followers.extend(results.get('users', []))
            if len(followers) >= max_to_retrieve:
                break
            next_max_id = results.get('next_max_id')
        return followers, next_max_id

    def get_user_id(self, user_name):
        user_feed_info = self._web_api.user_info2(user_name)
        return user_feed_info['id']

    def get_user_info(self, user_name):
        return self._web_api.user_info2(user_name)

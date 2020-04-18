"""Instagram users info scrapper"""
import hashlib
import string
import random
import json
import codecs
from pathlib import Path
from instagram_web_api import Client as WebClient
from instagram_private_api import Client as PrivateClient
from instagram_private_api import ClientCookieExpiredError, ClientLoginRequiredError


class InstagramWebClient(WebClient):
    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = ''.join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode())


class InstagramScrapper:
    # TODO: save settings to reconnect.
    def __init__(self,
                 username,
                 password,
                 settings_file_path=None,
                 login=True):
        self._username = username
        self._password = password
        self._web_api = InstagramWebClient(auto_patch=True,
                                           drop_incompat_keys=False)
        if login:
            if settings_file_path is None:
                self._authed_web_api = self._create_connection()
            else:
                self._settings_file_path = Path(settings_file_path)
                if self._settings_file_path.is_file():
                    # Load previous connection
                    self._authed_web_api = self._reaload_connection()
                else:
                    # Create new connection
                    print('Unable to find file: {0!s}'.format(
                        settings_file_path))
                    print('New Login')
                    self._authed_web_api = self._create_connection()

    def _create_connection(self, cached_settings=None):
        if cached_settings is not None:
            print('Loading previous uuid')
            return PrivateClient(self._username,
                                 self._password,
                                 settings=cached_settings)
        return PrivateClient(username=self._username,
                             password=self._password,
                             on_login=lambda x: self._onlogin_callback(
                                 x, 'data/instagram/connection.json'))

    def _reaload_connection(self):
        try:
            with self._settings_file_path.open('r') as file_data:
                cached_settings = json.load(file_data,
                                            object_hook=self._from_json)
                print('Reusing settings: {0!s}'.format(
                    self._settings_file_path))

                device_id = cached_settings.get('device_id')
                # reuse auth settings
                api = self._create_connection(cached_settings=cached_settings)
        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.
                  format(e))
            print('Looks like login expired...')
            # Login expired
            # Do relogin but use default ua, keys and such
            api = self._create_connection()
        return api

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

    def _from_json(self, json_object):
        if '__class__' in json_object and json_object['__class__'] == 'bytes':
            return codecs.decode(json_object['__value__'].encode(), 'base64')
        return json_object

    def _onlogin_callback(self, api, new_settings_file):
        cache_settings = api.settings
        # TODO: if file not exists an exception occurs.0
        with open(new_settings_file, 'w') as outfile:
            json.dump(cache_settings, outfile, default=self._to_json)
            print('SAVED: {0!s}'.format(new_settings_file))

    def _to_json(self, python_object):
        if isinstance(python_object, bytes):
            return {
                '__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()
            }
        raise TypeError(repr(python_object) + ' is not JSON serializable')

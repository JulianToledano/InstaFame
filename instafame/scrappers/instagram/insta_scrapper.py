"""Instagram users info scrapper"""
import instaloader
from .decoders import ProfileEncoder


# TODO: rethink whole package structure.
class InstagramScrapper:
    """Instaloader wrapper"""
    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password
        self._instaload = instaloader.Instaloader()
        if username is not None and password is not None:
            self._instaload.login(self._username, self._password)

    def get_followers(self, account_name):
        for follower in self._get_followers(account_name):
            yield ProfileEncoder().decode(follower)

    def _get_followers(self, account_name):
        profile = instaloader.Profile.from_username(self._instaload.context,
                                                    account_name)
        return profile.get_followers()

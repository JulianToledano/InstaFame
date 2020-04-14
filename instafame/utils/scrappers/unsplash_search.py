'''
This class is based on unsplah-search package.
You can install it with 'pip install unsplash-search
Check it here:
        https://pypi.org/project/unsplash-search/
'''
import requests
import random
import json
from pathlib import Path


# TODO: logs
class Unsplash(object):
    """ Retrieve metadata from unsplash.

    Args:
        access_key (str): Your access_key. You can find this in the app developer page.
        destination_path (pathlib.Path): path where metadata will be saved.
    """
    def __init__(self, access_key):

        self._access_key = access_key
        self._ses = requests.Session()
        self._ses.headers.update(
            {'Authorization': "Client-ID {}".format(access_key)})

        self._base_endpoint = "https://api.unsplash.com/"
        self._search_photos_endpoint = "/search/photos"

    def search_photos(self, query, per_page, page_number):
        """ Search for photos using a query.

        Args:
            query (str): The query you want to use to retrieve the photos
            per_page (str): number of results per page.
            page_number (str): pagination page number.

        Returns:
            img (dict): dict with all the metadata.

        """

        params = {'query': query, 'per_page': per_page, 'page': page_number}
        try:
            resp = self._ses.get(self._base_endpoint +
                                 self._search_photos_endpoint,
                                 params=params)
            print(self._base_endpoint + self._search_photos_endpoint, params)
        except requests.RequestException as ex:
            print(('STATUS: {}  TEXT: {}'.format(ex.response.status_code,
                                                 ex.response)))
        else:
            data = resp.json()
            return data['results']

    def download_photo(self, metadata_file, destination_dir):
        """ Downloads a photo given a unsplash metadata file.
        """
        with metadata_file.open() as f:
            metadata = json.load(f)
        file_name = metadata['id'] + '.jpg'
        destination_file = destination_dir / file_name
        url = metadata['urls']['full']
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with destination_file.open('wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)

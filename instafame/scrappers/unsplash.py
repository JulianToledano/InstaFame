'''
This class is based on unsplah-search package.
You can install it with 'pip install unsplash-search
Check it here:
        https://pypi.org/project/unsplash-search/
'''
import requests
import random
import json
import logging
from pathlib import Path


# TODO: save results in a directory with structure:
#   -- unsplash
#       |-- metadata
#       |-- photos
# TODO: logs are pretty bad.
class Unsplash(object):
    """ Retrieve metadata from unsplash.

    Args:
        access_key (str): Your access_key. You can find this in the app developer page.
        destination_path (pathlib.Path): path where metadata will be saved.
    """
    def __init__(self, access_key):
        logging.basicConfig(level=logging.INFO)
        self._logger = logging.getLogger(__name__)
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
            # print(self._base_endpoint + self._search_photos_endpoint, params)
            self._logger.info(
                self._base_endpoint + self._search_photos_endpoint, params)
        except requests.RequestException as ex:
            # print(('STATUS: {}  TEXT: {}'.format(ex.response.status_code,
            #                                      ex.response)))
            self._logger.ERROR(
                ('STATUS: {}  TEXT: {}'.format(ex.response.status_code,
                                               ex.response)))
        else:
            data = resp.json()
            return data['results']

    def download_photo(self, size, metadata_file, destination_dir):
        """ Downloads a photo given a unsplash metadata file.
        """
        self._logger.info('Loading metadata from {}'.format(metadata_file))
        with metadata_file.open() as f:
            metadata = json.load(f)
        self._logger.info('Metadata loaded.')
        file_name = metadata['id'] + '.jpg'
        destination_file = destination_dir / file_name
        url = metadata['urls'][size]
        self._logger.info('Sending request to {}'.format(url))
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            self._logger.info('Request accepted status={}'.format(
                r.status_code))
            with destination_file.open('wb') as f:
                self._logger.debug('Downloading chunk...')
                for chunk in r.iter_content(1024):
                    f.write(chunk)
                self._logger.info('Picture downloaded.')
            self._logger.error('Error in request. Status={}'.format(
                r.status_code))

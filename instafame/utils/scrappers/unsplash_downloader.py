import requests
import random
import json
from pathlib import Path


class UnsplashDownloader:
    def __init__(self, source_path, destination_path):
        self._source_path = Path(source_path)
        self._destination_path = Path(destination_path)

    def download_image(self, metadata_file):
        source_file = self._source_path / metadata_file
        with source_file.open() as f:
            metadata = json.load(f)
        file_name = metadata['id'] + '.jpg'
        destination_file = self._destination_path / file_name
        url = metadata['urls']['full']
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with destination_file.open('wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
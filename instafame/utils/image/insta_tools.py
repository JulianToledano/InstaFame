from PIL import Image
from pathlib import Path


class InstaPicTool:
    insta_ratios = {
        'square': {
            'ratio': 1,
            'width': 1080,
            'height': 1080
        },
        'vertical': {
            'ratio': 0.8,
            'width': 1080,
            'height': 1350
        },
        'horizontal': {
            'ratio': 1.9424460431654675,
            'width': 1080,
            'height': 556
        }
    }

    def __init__(self, pic_path, destination_path):
        self._pic_path = Path(pic_path)
        self._dest_path = Path(destination_path)
        self._picture = Image.open(self._pic_path, 'r')
        self._pic_width = self._picture.size[0]
        self._pic_height = self._picture.size[1]
        self._pic_ratio = self._pic_width / self._pic_height
        self._pic_type = self.check_type()

    def check_type(self):
        if self._pic_ratio == 1:
            return 'square'
        elif self._pic_ratio < 1:
            return 'vertical'
        elif self._pic_ratio > 1:
            return 'horizontal'

    def _get_new_image_size(self):
        if self._pic_type == 'vertical':
            if self._pic_ratio < self.insta_ratios[self._pic_type]['ratio']:
                new_width = round((self._pic_height * 4) / 5)
                return (new_width, self._pic_height)
        if self._pic_type == 'horizontal':
            if self._pic_ratio > self.insta_ratios[self._pic_type]['ratio']:
                new_heigth = round((self._pic_width * 9) / 16)
                return (self._pic_width, new_heigth)
        return self._get_square_size()

    def _get_square_size(self):
        if self._pic_type == 'vertical':
            return (self._pic_height, self._pic_height)
        if self._pic_type == 'horizontal':
            return (self._pic_width, self._pic_width)

    def _resize(self):
        new_size = self._get_new_image_size()
        background = Image.new('RGB', (new_size[0], new_size[1]),
                               (255, 255, 255, 255))
        offset = ((new_size[0] - self._pic_width) // 2,
                  (new_size[1] - self._pic_height) // 2)
        background.paste(self._picture, offset)
        background.save(self._dest_path /
                        ('pic_to_post_' + self._pic_path.name))
        print("Image has been resized !")

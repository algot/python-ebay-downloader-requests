import re

import requests


class ItemPage:
    def __init__(self, item_url):
        self.item_url = item_url
        self.page_content = ''

    def get_image_urls(self):
        self._get_page_content()

        regex = re.compile('https://i\.ebayimg\.com/images/g/\S{16}/s-l1600.jpg')
        images_urls_all = regex.findall(self.page_content)
        print(f'Number of images found on item page: {len(images_urls_all)}')
        return images_urls_all

    def _get_page_content(self):
        with requests.get(url=self.item_url) as r:
            self.page_content = r.text

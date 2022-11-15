import re
from time import sleep

import requests


class ItemPage:
    def __init__(self, item_url):
        self.item_url = item_url
        self.item_id = self._get_item_id()
        self.page_content = self._get_page_content()
        self.item_title = self._get_item_title()
        self.images_urls = []
        self.item_images = {self.item_id: []}

    def get_image_urls(self):
        regex = re.compile('https://i\.ebayimg\.com/images/g/\S{16}/s-l1600.jpg')
        self.images_urls = regex.findall(self.page_content)

        if len(self.images_urls) == 0:
            self.images_urls = self._get_images_case_with_one_active_photo()

        if len(self.images_urls) == 0:
            self.images_urls = self._get_images_for_ended_items()

        print(f'Number of images on {self.item_id} = {len(self.images_urls)}')

        for i, url in enumerate(self.images_urls):
            image_filename = f'{self.item_id}_{self.item_title}_{i + 1}.jpg'
            self.item_images[self.item_id].append((image_filename, url))

        return self.item_images

    def _get_item_id(self) -> str:
        return self.item_url.split('/')[-1]

    def _get_page_content(self):
        print(f'Loading item {self.item_id}')
        sleep(2)

        try:
            with requests.get(self.item_url) as r:
                return r.text
        except Exception as err:
            print(err)

    def _get_item_title(self):
        title = re.search('<title>(.*)</title>', self.page_content).group(1)
        s = title.replace(' | eBay', '').strip()
        s = s.replace(' ', '_')
        s = re.sub(r'(?u)[^-\w.]', '', s)
        s = s.replace('__', '_')
        return s.lower()

    def _get_images_case_with_one_active_photo(self):
        result = []
        split_lines = self.page_content.splitlines()
        line_with_images = [x for x in split_lines if 'mainImgHldr' in x]
        if len(line_with_images) > 0:
            preview_regex = re.compile('https://i\.ebayimg\.com/images/g/\S{16}/s-l\S*')
            image_preview_urls = preview_regex.findall(line_with_images[0])
            if len(image_preview_urls) > 0:
                result = [re.sub('(-l.*).(jpg|png)', '-l1600.jpg', x) for x in image_preview_urls]

        return result

    def _get_images_for_ended_items(self):
        result = []
        split_lines = self.page_content.splitlines()
        line_with_images = [x for x in split_lines if '<img id="icImg"' in x and '<noscript>' not in x]
        if len(line_with_images) > 0:
            preview_regex = re.compile('https://i\.ebayimg\.com/images/g/\S{16}/s-l\S*')
            image_preview_urls = preview_regex.findall(line_with_images[0])
            if len(image_preview_urls) > 0:
                result = [re.sub('(-l.*).(jpg|png)', '-l1600.jpg', x) for x in image_preview_urls]

        return result

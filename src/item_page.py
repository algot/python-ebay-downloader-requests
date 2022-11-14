import re

import requests


class ItemPage:
    def __init__(self, item_url):
        self.item_url = item_url
        self.page_content = self._get_page_content()
        self.item_id = self._get_item_id()
        self.item_title = self._get_item_title()
        self.images_urls = []
        self.item_images = {self.item_id: []}

    def get_image_urls(self):
        regex = re.compile('https://i\.ebayimg\.com/images/g/\S{16}/s-l1600.jpg')
        self.images_urls = regex.findall(self.page_content)

        if len(self.images_urls) == 0:
            self.images_urls = self._get_images_for_porsche_case()

        print(f'Number of images on {self.item_id} = {len(self.images_urls)}')

        for i, url in enumerate(self.images_urls):
            image_filename = f'{self.item_id}_{self.item_title}_{i + 1}.jpg'
            self.item_images[self.item_id].append((image_filename, url))

        return self.item_images

    def _get_item_id(self) -> str:
        return self.item_url.split('/')[-1]

    def _get_page_content(self):
        with requests.get(url=self.item_url) as r:
            return r.text

    def _get_images_for_porsche_case(self):
        split_lines = self.page_content.splitlines()
        line_with_images = [x for x in split_lines if 'mainImgHldr' in x]
        preview_regex = re.compile('https://i\.ebayimg\.com/images/g/\S{16}/s-l\S*')
        image_preview_urls = preview_regex.findall(line_with_images[0])

        return [re.sub('(-l.*).(jpg|png)', '-l1600.jpg', x) for x in image_preview_urls]

    def _get_item_title(self):
        title = re.search('<title>(.*)</title>', self.page_content).group(1)
        s = title.replace(' | eBay', '').strip()
        s = s.replace(' ', '_')
        s = re.sub(r'(?u)[^-\w.]', '', s)
        s = s.replace('__', '_')
        return s.lower()

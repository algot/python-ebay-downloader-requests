import contextlib
import json
import re
from time import sleep

import requests

from special_chars_parser import parse_string


class ItemPage:
    def __init__(self, item_url):
        self.item_url = item_url
        self.item_id = self._get_item_id()
        self.page_content = self._get_page_content()
        self.item_title = self._get_item_title()
        self.images_urls = []
        self.item_images = {self.item_id: []}

    def get_image_urls(self, count):
        self._getimages_default_approach()
        self._get_image_case_with_one_active_photo()
        self._get_images_for_ended_items_multiple_photo()
        self._get_image_for_ended_items_single_photo()

        print(f'Number of images on {self.item_id} = {len(self.images_urls)}')

        for index, url in enumerate(self.images_urls):
            image_filename = self._get_image_filename(count, index)
            self.item_images[self.item_id].append((image_filename, url))

        return self.item_images

    def _get_item_id(self):
        return self.item_url.split('/')[-1]

    def _get_page_content(self):
        print(f'Loading item {self.item_id}')
        sleep(1)

        try:
            with requests.get(self.item_url, params={'_ul': 'EN'}) as r:
                return r.text
        except Exception as err:
            print(err)

    def _get_item_title(self):
        title = re.search(r'<title>(.*)</title>', self.page_content).group(1)
        s = title.replace(' | eBay', '').strip()
        s = s.replace(' ', '-')
        s = re.sub(r'(?u)[^-\w.]', '', s)
        s = s.replace('__', '_')
        s = parse_string(s)
        return s.lower()

    def _getimages_default_approach(self):
        regex = re.compile(r'https://i\.ebayimg\.com/images/g/\S{16}/s-l1600.jpg')
        result = regex.findall(self.page_content)

        if len(result) > len(self.images_urls):
            self.images_urls = result

    def _get_image_case_with_one_active_photo(self):
        result = []
        split_lines = self.page_content.splitlines()
        line_with_images = [x for x in split_lines if 'mainImgHldr' in x]
        if len(line_with_images) > 0:
            preview_regex = re.compile(r'https://i\.ebayimg\.com/images/g/\S{16}/s-l\S+\.[a-zA-Z]+')
            image_preview_urls = preview_regex.findall(line_with_images[0])
            if image_preview_urls:
                result = [re.sub('(-l.*).(jpg|png)', '-l1600.jpg', x) for x in image_preview_urls]
                result = list(dict.fromkeys(result))  # remove duplicates preserving orders

        if len(result) > len(self.images_urls):
            self.images_urls = result

    def _get_images_for_ended_items_multiple_photo(self):
        split_lines = self.page_content.splitlines()
        line_with_images = [x for x in split_lines if '$vim_C' in x][0]
        if line_with_images:
            self._get_images_from_line_with_images_of_ended_item(line_with_images)

    def _get_image_for_ended_items_single_photo(self):
        split_lines = self.page_content.splitlines()
        line_with_image_raw = [x for x in split_lines if '$vim_C' in x][0]
        line_with_image_split = line_with_image_raw.split('<script>')  # "p": "PICTURE"
        line_with_image = [x for x in line_with_image_split if '"p":"PICTURE"' in x][0]
        if line_with_image:
            self._get_images_from_line_with_images_of_ended_item(line_with_image)

    def _get_images_from_line_with_images_of_ended_item(self, line_with_images):
        json_regex = re.compile(r'.concat\((.*?)\)</script>')
        str_json_result = json_regex.search(line_with_images)
        if str_json_result.groups():
            json_object = json.loads(str_json_result.group(1))
            with contextlib.suppress(KeyError):
                media_list = json_object['w'][0][2]['model']['mediaList']
                image_ids = [x['image']['originalImg']['imageId'] for x in media_list]
                result = [f'https://i.ebayimg.com/images/g/{x}/s-l1600.jpg' for x in image_ids]

                if len(result) > len(self.images_urls):
                    self.images_urls = result

    def _get_image_filename(self, count, index):
        return f'{count + 1}_{self.item_id}_{self.item_title}_{index + 1}.jpg'

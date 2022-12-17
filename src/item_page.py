import json
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

    def get_image_urls(self, count):
        self._getimages_default_approach()
        self._get_image_case_with_one_active_photo()
        self._get_images_for_ended_items_multiple_photo()
        self._get_image_for_ended_items_single_photo()

        print(f'Number of images on {self.item_id} = {len(self.images_urls)}')

        for i, url in enumerate(self.images_urls):
            image_filename = f'{count + 1}_{self.item_id}_{self.item_title}_{i + 1}.jpg'
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
        s = s.replace(' ', '_')
        s = re.sub(r'(?u)[^-\w.]', '', s)
        s = s.replace('__', '_')
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
            preview_regex = re.compile(r'https://i\.ebayimg\.com/images/g/\S{16}/s-l\S*')
            image_preview_urls = preview_regex.findall(line_with_images[0])
            if image_preview_urls:
                result = [re.sub('(-l.*).(jpg|png)', '-l1600.jpg', x) for x in image_preview_urls]

        if len(result) > len(self.images_urls):
            self.images_urls = result

    def _get_images_for_ended_items_multiple_photo(self):
        result = []
        split_lines = self.page_content.splitlines()
        line_with_images = [x for x in split_lines if '$vim_C' in x][0]
        if line_with_images:
            json_regex = re.compile(r'.concat\((.*?)\)</script>')
            str_json_result = json_regex.search(line_with_images)
            if len(str_json_result.groups()) > 0:
                json_object = json.loads(str_json_result.group(1))
                intermediate_node = json_object['w'][0][2]
                if 'model' in intermediate_node:
                    model_node = intermediate_node['model']
                    if 'mediaList' in model_node:
                        media_list = model_node['mediaList']
                        image_ids = [x['image']['originalImg']['imageId'] for x in media_list]
                        result = [f'https://i.ebayimg.com/images/g/{x}/s-l1600.jpg' for x in image_ids]

        if len(result) > len(self.images_urls):
            self.images_urls = result

    def _get_image_for_ended_items_single_photo(self):
        result = []
        split_lines = self.page_content.splitlines()
        line_with_image_raw = [x for x in split_lines if '$vim_C' in x][0]
        line_with_image_split = line_with_image_raw.split('<script>')  # "p": "PICTURE"
        line_with_image = [x for x in line_with_image_split if '"p":"PICTURE"' in x][0]
        if line_with_image:
            json_regex = re.compile(r'.concat\((.*?)\)</script>')
            str_json_result = json_regex.search(line_with_image)
            if len(str_json_result.groups()) > 0:
                json_object = json.loads(str_json_result.group(1))
                model_node = json_object['w'][0][2]['model']
                if 'mediaList' in model_node:
                    media_list = model_node['mediaList']
                    image_ids = [x['image']['originalImg']['imageId'] for x in media_list]
                    result = [f'https://i.ebayimg.com/images/g/{x}/s-l1600.jpg' for x in image_ids]

        if len(result) > len(self.images_urls):
            self.images_urls = result

import re

from pathlib import Path


class IndexPage:
    def __init__(self, filename):
        self.parent_dir = Path(__file__).parent.parent
        self.resource_dir = self.parent_dir.joinpath('resources')
        self.index_page_file_path = f'{self.resource_dir.joinpath(filename)}'
        self.page_content = ''

    def _read_file(self):
        with open(self.index_page_file_path, mode='r', encoding='utf-8') as f:
            self.page_content = f.read()

    def get_list_of_item_urls_from_index_page(self):
        self._read_file()

        regex = re.compile(r'https://\S*/itm/\S{12}')

        item_urls = list(dict.fromkeys(regex.findall(self.page_content)))  # remove duplicates preserving orders
        items_urls_cleaned = [i for i in item_urls if '12345' not in i]

        print(f'Numbers of items found: {len(items_urls_cleaned)}')

        return items_urls_cleaned

import sys

from index_page import IndexPage
from item_page import ItemPage


def main(input_filename):
    index_page = IndexPage(input_filename)
    items_urls = index_page.get_list_of_item_urls_from_index_page()

    urls_to_download = []

    for url in items_urls:
        item_page = ItemPage(url)
        urls_to_download.append(item_page.get_image_urls())
    print(urls_to_download)
    pass


if __name__ == '__main__':
    # filename = (sys.argv[1])

    # filename = '2022.09.24-5452graham-003.html'  # 3
    filename = '2022.11.05-aherl-1-240.html'  # 240
    # filename = '2022.11.05-xroads13-01-240.html'  # 60
    # filename = '2022.11.12-carbooks0947-008.html'  # 8

    main(filename)

import sys

from index_page import IndexPage
from item_page import ItemPage
from downloader import download


def main(input_filename):
    items_urls = IndexPage(input_filename).get_list_of_item_urls_from_index_page()
    files_to_download = [ItemPage(url).get_image_urls() for url in items_urls]
    download(input_filename, files_to_download)


if __name__ == '__main__':
    filename = (sys.argv[1])

    main(filename)

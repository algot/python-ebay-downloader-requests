import sys

from alive_progress import alive_bar

from index_page import IndexPage
from item_page import ItemPage
from downloader import download


def main(input_filename):
    items_urls = IndexPage(input_filename).get_list_of_item_urls_from_index_page()

    files_to_download = []
    with alive_bar(len(items_urls), title='Get image urls', spinner='dots') as bar:
        for count, url in enumerate(items_urls):
            item_page = ItemPage(url)
            files_to_download.append(item_page.get_image_urls(count))
            bar()

    download(input_filename, files_to_download)


if __name__ == '__main__':
    filename = (sys.argv[1])

    main(filename)

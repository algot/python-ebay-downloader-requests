import sys
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

import downloader
from index_page import IndexPage
from item_page import ItemPage


def main(input_filename):
    items_urls = get_list_of_item_urls_from_index_page(input_filename)
    files_to_download = get_list_of_files_to_download_parallel(items_urls)
    downloader.download(input_filename, files_to_download)


def get_list_of_item_urls_from_index_page(input_filename):
    index_page = IndexPage(input_filename)
    return index_page.get_list_of_item_urls_from_index_page()


def get_image_urls_from_item_page(url):
    item_page = ItemPage(url)
    image_urls = item_page.get_image_urls()
    return image_urls


def get_list_of_files_to_download(url):
    return get_image_urls_from_item_page(url)


def get_list_of_files_to_download_parallel(args):
    cpus = cpu_count()
    results = ThreadPool(cpus - 1).imap(get_list_of_files_to_download, args)
    return list(results)


if __name__ == '__main__':
    try:
        filename = (sys.argv[1])
    except IndexError:
        print('You forgot to specify filename to process! Please try again.')
        sys.exit(1)

    main(filename)

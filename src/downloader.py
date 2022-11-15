import os
from pathlib import Path
from time import sleep

import requests


def download(input_filename, files_to_download):
    directory = _get_download_dir(input_filename)

    if not os.path.isdir(directory):
        os.makedirs(directory)

    for item in files_to_download:
        current_item_id = ", ".join(item)
        print(f'Downloading item: {current_item_id}')
        for file in item[current_item_id]:
            filename = file[0]
            print(f'Downloading file: {filename}')

            url_to_download = file[1]

            sleep(1)
            try:
                with requests.get(url_to_download) as r:
                    content = r.content

                    try:
                        with open(directory.joinpath(filename), 'wb') as w:
                            w.write(content)
                    except Exception as err:
                        print(err)

            except Exception as err:
                print(err)


def _get_download_dir(input_filename):
    parent_dir = Path(__file__).parent.parent
    return parent_dir.joinpath('resources').joinpath(input_filename.replace('.html', ''))

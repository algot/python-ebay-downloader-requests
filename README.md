# Prerequisites
* Python 3.6 is installed
* git is installed

# Installation (Windows)
* Open cmd
* Navigate to place where it should be installed
* Run following commands:
  * `git clone https://github.com/algot/python-ebay-downloader-requests`
  * `cd python-ebay-downloader-requests`
  * `python -m venv .venv`
  * `.venv\Scripts\activate.bat`
  * `pip install -r requirements.txt`

# Usage
Place html file into **resources** directory

In **python-ebay-downloader-requests** directory open **cmd** and run following command:

`python src\main.py <filename>`

e.g.

`python src\main.py 2022.11.12-cootsimagery-deluxe-010.html`

Results will be downloaded to **resources** directory
import click
import datetime
import os
import re
import tarfile
import urllib.request

from bs4 import BeautifulSoup

def _get_timestamp():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d")
    return timestamp

def _create_dir(dir_name):
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        print(f"Directory {dir_name} already exists")

def _get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def _get_title(soup_obj):
    title = soup_obj.title.text
    title = re.sub('[^0-9a-zA-Z]+', '_', title)
    return title

def download_all_images_from_page(url):
    timestamp = _get_timestamp()
    html = _get_html(url)
    base_url = os.path.split(url)[0]

    soup = BeautifulSoup(html, 'html.parser')
    title = _get_title(soup)
    dest_dir = timestamp + '_' + title
    _create_dir(dest_dir)
    for image in soup.find_all('img'):
        image_src = image.get('src')
        image_url = base_url + '/' + image_src
        image_path = os.path.split(image_src)
        dest_image_name = dest_dir + '/' + image_path[len(image_path)-1]

        try:
            print(image_url)
            urllib.request.urlretrieve(image_url, dest_image_name)
        except urllib.error.HTTPError:
            print(f"image not found: {image_url}")

    _create_tarfile(dest_dir)

def _create_tarfile(img_dir):
    tar = tarfile.open(f"{img_dir}.tar", "w")
    tar.add(img_dir)
    tar.close()

@click.command()
def main():
    url = 'http://www.cs.uah.edu/~rcoleman/CS221/Temp/SIP3Hints.html'
    download_all_images_from_page(url)

if __name__ == '__main__':
    main()

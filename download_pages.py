import io
import re

import requests
from PIL import Image


def main():
    visited_pages = set()
    pages = list(set(re.findall(r'\w+\.htm', str(requests.get(f'https://www.datingariane.com').content))))
    while pages:
        print(f'{len(pages)} remaining')
        page = pages.pop()
        if page not in visited_pages:
            visited_pages.add(page)
            print(f'Downloading {page}')
            response = str(requests.get(f'https://www.datingariane.com/{page}').content)
            pages += list(set(re.findall(r'\w+\.htm', response)))
            images = set(re.findall(r'images/\w+\.jpg', response))
            print(f'{len(images)} images found')
            for image in images:
                try:
                    response = requests.get(f'https://www.datingariane.com/{image}')
                    response.raise_for_status()
                    with io.BytesIO(response.content) as f:
                        with Image.open(f) as img:
                            print(f'Saving image {image}')
                            img.save(f'{image}')
                except Exception:
                    pass


if __name__ == '__main__':
    main()

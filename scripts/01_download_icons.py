import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# URL da página de nós AWS
BASE_URL = 'https://diagrams.mingrammer.com/docs/nodes/aws'

# Diretório de saída
OUTPUT_DIR = 'data/raw/icons'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_page(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def parse_icon_urls(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if not src:
            continue
        if 'img/resources/aws' not in src:
            continue
        full_url = urljoin(base_url, src)
        urls.append(full_url)
    return list(set(urls))

def download_image(url, output_dir):
    filename = os.path.basename(url.split('?')[0])
    path = os.path.join(output_dir, filename)
    if os.path.exists(path):
        print(f'[SKIP] {filename} já existe')
        return
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f'[DOWNLOADED] {filename}')

def main():
    html = fetch_page(BASE_URL)
    icon_urls = parse_icon_urls(html, BASE_URL)
    print(f'Encontrei {len(icon_urls)} ícones. Iniciando download...')
    for url in icon_urls:
        download_image(url, OUTPUT_DIR)
    print('Download finalizado.')

if __name__ == '__main__':
    main()
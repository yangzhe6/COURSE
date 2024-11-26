import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import threading
url = "http://nsdb.imcce.fr/obspos/OBS_COLL/S/"
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')
if not os.path.exists('downloads'):
    os.makedirs('downloads')
def download_file(link, progress, lock):
    name = link.get('href')
    if name and not name.startswith("../") and not name.startswith(".") and (name.endswith('.html') or name.endswith('.txt')):
        file_url = url + name
        file_response = requests.get(file_url, stream=True)
        file_response.raise_for_status()
        file_path = os.path.join('downloads', name)
        with open(file_path, 'wb') as file:
            for data in file_response.iter_content(chunk_size=1024):
                file.write(data)
        with lock:
            progress.update(1)
        return name
filtered_links = [link for link in links if link.get('href') and link.get('href').endswith(('.html', '.txt'))]
progress = tqdm(total=len(filtered_links), desc='Downloading files')
lock = threading.Lock()
downloaded_files = []
with ThreadPoolExecutor(max_workers=20) as executor:
    downloaded_files = list(executor.map(lambda link: download_file(link, progress, lock), filtered_links))
progress.close()
if len(downloaded_files) == progress.n:
    print("所有文件下载完成。")
else:
    print("部分文件下载失败。")
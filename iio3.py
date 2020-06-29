import os

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tinydb import TinyDB, Query


sub_urls = []

BASEPATH = os.getcwd()
DATAPATH = os.path.join(BASEPATH, 'sensors.json')
DRIVERS = os.path.join(BASEPATH, 'drivers')
db = TinyDB(DATAPATH)


def create_schema(base_dir, base_obj):
    
    tables = db_tables()
    
    if not base_dir in tables:
        table = db.table(base_dir)
        table.insert(base_obj)

    
def db_tables():
    return db.tables()
    

def insert_files_dirs(base_url, kernel):
    full_url = f'{base_url}?h=v{kernel}'
    
    parsed_uri = urlparse(full_url)
    base_uri = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    
    base_dir = base_url.split('/')[-1]
    
    rqst_obj = Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})

    web_page = urlopen(rqst_obj)
    _content = web_page.read()
    web_page.close()

    new_html = BeautifulSoup(_content, 'lxml')
    
    files = new_html.select('a[class*=ls-blob]')
    dirs = new_html.select('a[class*=ls-dir]')
    
    files = [file.text for file in files]
    dirs = [dir.text for dir in dirs]
    
    create_schema(base_dir, {'href': base_url})
    create_schema(base_dir, {'ls-blob': files})
    create_schema(base_dir, {'ls-dir': dirs})
    
    for dir in dirs:
        if not dir in sub_urls:
            sub_urls.append(base_url+'/'+dir)
    

def download_file(href, filename, kernel):
    # remote
    full_url = f'{href}/{filename}?h=v{kernel}'
    
    print('DOWNLOADING ... ', full_url)
    
    #'''
    rqst_obj = Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})

    web_page = urlopen(rqst_obj)
    _content = web_page.read()
    web_page.close()

    new_html = BeautifulSoup(_content, 'lxml')

    file_content = new_html.select('div[class*=highlight]')[0].pre.text
    
    # local
    sub_dirs = href.split('/drivers/')[1].split('/')
    
    file_path = DRIVERS
    for s_d in sub_dirs:
        file_path = os.path.join(file_path, s_d)
    
    try:
        os.makedirs(file_path)
    except:
        pass
    
    file_path = os.path.join(file_path, filename)    
    
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(file_content)
    #'''


def download_files(kernel):
    tables = db_tables()
    
    #print('------------------', 'download_files', '------------------')
    for table in tables:
        href = db.table(table).all()[0]['href']
        blobs = db.table(table).all()[1]['ls-blob']
        
        for blob in blobs:
            #print(href, blob)
            download_file(href, blob, kernel)
    
    

if __name__ == '__main__':
    base_url = 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/drivers/iio'
    kernel = '4.19.97'
    
    insert_files_dirs(base_url, kernel)
    
    for s_u in sub_urls:
        #print(s_u)
        base_url = s_u
        insert_files_dirs(base_url, kernel)
        #sub_urls.remove(s_u)
    
    download_files(kernel)
    
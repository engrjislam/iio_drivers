import os

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tinydb import TinyDB, Query



def create_schema(_dir, _obj):
    BASEPATH = os.getcwd()
    DATAPATH = os.path.join(BASEPATH, 'sensors.json')
    db = TinyDB(DATAPATH)
    table = db.table(_dir)
    table.insert(_obj)
    

def extract_files_dirs(full_url):
    rqst_obj = Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})

    web_page = urlopen(rqst_obj)
    _content = web_page.read()
    web_page.close()

    new_html = BeautifulSoup(_content, 'lxml')
    
    files = new_html.select('a[class*=ls-blob]')
    dirs = new_html.select('a[class*=ls-dir]')
    
    return files, dirs


def extract_dir(dirs, full_url):
    parsed_uri = urlparse(full_url)
    base_uri = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

    print("-------------------------------------")
    for dir in dirs:
        print('directory: ', dir.text)
        print('url link:  ', base_uri + dir['href'])
        print("-------------------------------------")
    



if __name__ == '__main__':
    base_url = 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/drivers/iio'
    _version = '?h=v4.19.97'
    full_url = base_url + _version
    
    files, dirs = extract_files_dirs(full_url)
    
    '''
    for file in files:
        #print(file.text)
        create_schema('iio', {'ls-blob': file.text})
    '''
    
    '''
    files = [str(file.text) for file in files]
    create_schema('iio', {'ls-blob': files})
    '''
        
    parsed_uri = urlparse(full_url)
    base_uri = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    
    '''    
    for dir in dirs:
        #print('dir name:', dir.text)
        #print('dir link:', base_uri+dir['href'])
        create_schema('iio', {'ls-dir': dir.text, 'ls-lnk': base_uri+dir['href']})
    '''
    
    
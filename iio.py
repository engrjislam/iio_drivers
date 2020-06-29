

import xlsxwriter




def extract_dirs(full_url):
    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup
    
    rqst_obj = Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})

    web_page = urlopen(rqst_obj)
    _content = web_page.read()
    web_page.close()

    new_html = BeautifulSoup(_content, 'lxml')
    dirs = new_html.select('a[class*=ls-dir]')
    
    return dirs


'''
with open('iio.txt', 'w') as file:
    file.write(str(sensors))
'''


def extract_dir(dirs, full_url):
    from urllib.parse import urlparse

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
    
    dirs = extract_dirs(full_url)
    extract_dir(dirs, full_url)


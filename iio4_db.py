from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


base_url = 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/drivers/iio/Makefile'
kernel = '4.19.97'

full_url = f'{base_url}?h=v{kernel}'

rqst_obj = Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})

web_page = urlopen(rqst_obj)
_content = web_page.read()
web_page.close()

new_html = BeautifulSoup(_content, 'lxml')

file_content = new_html.select('div[class*=highlight]')[0].pre.text

with open('Makefile', 'w') as file:
    file.write(spans)
    




import os

from tinydb import TinyDB, Query

BASEPATH = os.getcwd()
DATAPATH = os.path.join(BASEPATH, 'sensors.json')
db = TinyDB(DATAPATH)
db.tables()

db.table('accel')
db.table('accel').all()
db.table('accel').all()[0]
db.table('accel').all()[0]['href']
sub_dir = db.table('accel').all()[0]['href'].split('drivers')

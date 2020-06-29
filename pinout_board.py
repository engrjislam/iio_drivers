pip install bs4
pip install beautifulsoup4

pip install lxml
pip install xlsxwriter



from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

pinout_url = 'https://pinout.xyz/boards'

pinout_req = Request(pinout_url, headers={'User-Agent': 'Mozilla/5.0'})

pinout_web = urlopen(pinout_req)
pinout_page = pinout_web.read()
pinout_web.close()

pinout_html = BeautifulSoup(pinout_page, 'lxml')

#boards = pinout_html.findAll('li', {'class':'board'})

hats = pinout_html.findAll('li', {'data-form-factor':'HAT'})


print("-------------------------------------")
for hat in hats:
    manufacturer = hat['data-manufacturer']
    type = hat['data-type']
    url = hat.a['href']
    img_src = hat.a.img['src']
    name = hat.a.strong.text
    
    print('name: ', name)
    print('manufacturer: ', manufacturer)
    print('type: ', type)
    print('url: ', url)
    print('img_src: ', img_src)
    
    print("-------------------------------------")
    
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

import xlsxwriter

pinout_url = 'https://pinout.xyz/boards'

pinout_req = Request(pinout_url, headers={'User-Agent': 'Mozilla/5.0'})

pinout_web = urlopen(pinout_req)
pinout_page = pinout_web.read()
pinout_web.close()

pinout_html = BeautifulSoup(pinout_page, 'lxml')

#boards = pinout_html.findAll('li', {'class':'board'})

hats = pinout_html.findAll('li', {'data-form-factor':'HAT'})




filename, headers = 'hats.xlsx', ["product_name", "manufacturer", "product_type", "product_url", "product_image"]

row, col = 0, 0

workbook = xlsxwriter.Workbook(filename) 
worksheet = workbook.add_worksheet("hats")

for header in headers:
    worksheet.write(row, col, header)
    col += 1
    
row, col = 1, 0


#print("-------------------------------------")
for hat in hats:
    manufacturer = hat['data-manufacturer'] #.replace(',', '|')
    type = hat['data-type'] #.replace(',', '|')
    url = hat.a['href'] #.replace(',', '|')
    img_src = hat.a.img['src'] #.replace(',', '|')
    name = hat.a.strong.text #.replace(',', '|')
    
    #print('name:', name)
    #print('manufacturer:', manufacturer)
    #print('type:', type)
    #print('url:', url)
    #print('img_src:', img_src)
    
    worksheet.write(row, col, name)
    worksheet.write(row, col+1, manufacturer)
    worksheet.write(row, col+2, type)
    worksheet.write(row, col+3, url)
    worksheet.write(row, col+4, img_src)
    
    row += 1
    
    #print("-------------------------------------")
    
workbook.close()
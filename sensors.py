from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

import xlsxwriter

pinout_url = 'https://pinout.xyz'
pinout_boards = pinout_url + '/boards'

pinout_req = Request(pinout_boards, headers={'User-Agent': 'Mozilla/5.0'})

pinout_web = urlopen(pinout_req)
pinout_page = pinout_web.read()
pinout_web.close()

pinout_html = BeautifulSoup(pinout_page, 'lxml')

#boards = pinout_html.findAll('li', {'class':'board'})
#hats = pinout_html.findAll('li', {'data-form-factor':'HAT'})

sensors = pinout_html.select('li[data-type*=Sensor]')



filename, headers = 'sensors.xlsx', ["name", "manufacturer", "form_factor", "url", "image"]

row, col = 0, 0

workbook = xlsxwriter.Workbook(filename) 
worksheet = workbook.add_worksheet("sensors")

for header in headers:
    worksheet.write(row, col, header)
    col += 1
    
row, col = 1, 0


#print("-------------------------------------")
for sensor in sensors:
    manufacturer = sensor['data-manufacturer'] 
    form_factor = sensor['data-form-factor'] 
    url = pinout_url + sensor.a['href'] 
    image = pinout_url + sensor.a.img['src'] 
    name = sensor.a.strong.text 
    
    worksheet.write(row, col, name)
    worksheet.write(row, col+1, manufacturer)
    worksheet.write(row, col+2, form_factor)
    worksheet.write(row, col+3, url)
    worksheet.write(row, col+4, image)
    
    row += 1
    
    #print("-------------------------------------")
    

workbook.close()
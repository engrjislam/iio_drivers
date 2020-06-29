#pip install xlrd

import xlrd
import requests

url = 'http://localhost:5000/api/sensors'

loc = ("sensors.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_name('sensors')

nrows = sheet.nrows


headers = sheet.row_values(0)
# ['name', 'manufacturer', 'form_factor', 'url', 'image']

for index in range(1, nrows):
    row = sheet.row_values(index)
    json_obj = {}
    for col in range(len(row)):
        json_obj[headers[col]] = row[col]
        
    #print(json_obj)
    r = requests.post(url, json=json_obj)
    print(r.status_code)
    

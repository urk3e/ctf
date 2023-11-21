import requests as req
import json

firstPage = req.get('http://10.10.169.100:3000/')
isiPage = firstPage.text
jsonFormat = json.loads(isiPage)

nextPage = jsonFormat['next']
firstVal = jsonFormat['value']

all_val = [firstVal]

while(nextPage != 'end'):
        pageReq = req.get('http://10.10.169.100:3000/' + nextPage)
        isi = pageReq.text
        jsonF = json.loads(isi)

        nextPage = jsonF['next']
        val = jsonF['value']

        if val != 'end':
                all_val.append(val)

print(*all_val, sep='')

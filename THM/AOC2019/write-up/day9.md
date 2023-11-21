akses IP yang sudah disediakan beserta dengan portnya, yaitu `http://10.10.169.100:3000/`

hasilnya nanti adalah
```
{"value":"s", "next":"f"}
```
Q1:What is the value of the flag?


A1:
hasil dari itu adalah JSON objek. kita perlu pergi ke `next` yang berarti next page, 
yang mana ada di `http://10.10.169.100:300/f`. kita perlu menyimpan hasil dari tiap 
`value` pada tiap page hingga mencapai `end` pada value dari `value` dan `next`. untuk 
melakukan request ke tiap page yang akan dikunjungi, daripada kita harus menuliskannya 
satu per satu, kita dapat mengotomatisasi hal tersebut dengan python scripting. 
sebelumnya, kita buat file python dengan format `.py`, disini saya menggunakan editor 
`nano`, jadi langsung saja buat file `nano loop_req.py`. jika sudah membuatnya, 
tuliskan script python berikut
```
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
```

2 line pertama pada script tersebut adalah importing 
library dari python yg diperlukan. `firstPage` merupakan variabel yang berisi request 
pada halaman pertama dari web. selanjutnya variabel `isiPage` merupakan isi atau hasil 
request pada halaman pertama. lalu `jsonFormat` adalah variabel yang merupa hasil 
request menjadi format JSON, yang mana format JSON ini sama seperti format dictionary 
pada python. variabel `nextPage` dan `firstVal` merupakan pemanggilan value dari 
dictionary dengan menggunakan key. selanjutnya kita buat list `all_val` yang berisi 
`firstVal`, list ini nantinya akan terisi secara otomatis oleh value dari `value` pada 
setiap page. while loop disini adalah melakukan hal seperti sebelumnya namun secara 
otomatis dan berulang, hingga value dari `value` dan `next` mencapai `end`, selain itu
terdapat pengkodisian if juga dimana jika value dari `value` bukan merupakan `end` maka
value dari `value` tersebut akan ditambahkan ke list `all_val`. terakhir, nantinya
list `all_val` di print semua value didalamnya tanpa ada separator atau tanda pemisah
apapun, sehingga nantinya semua value tersebut ketika digabungkan akan menjadi flag yang
dapat disubmit pada soal


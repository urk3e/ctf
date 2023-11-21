spawn mesin di THM, tunggu hingga 5menit agar mesin benar-benar siap.

Q1:What is the path of the hidden page?
Q2:What is the password you found?
Q3:What do you have to take to the 'partay'

A1:
kita perlu melakukan brute-forcing untuk menemukan hidden dir yang diminta,
tools yang dapat digunakan diantaranya `dirb` dan `gobuster`.
jika menggunakan `dirb` kita dapat langsung melakukannya dengan cara:
```
dirb http://<ip machine>:3000
```
dan dirb akan otomatis menggunakan wordlist yang ada di `/usr/share/dirb/wordlists/common.txt`

sedangkan jika kita ingin menggunakan gobuster, kita dapat melakukannya dengan cara:
```
gobuster dir -u http://<ip machine>:3000 -w /usr/share/dirb/wordlists/common.txt
```
sebenarnya untuk wordlist bebas menggunakan apa saja, namun untuk mempermudah, disini saya
menggunakan wordlists yang sudah disediakan oleh Kali Linux saja.

selanjutnya jika proses sudah berjalan nantinya kita akan mendapatkan hasil dir yang telah
didapat setelah brute-forcing. ada 2 path yang menarik perhatian, dan itulah jawabannya.

A2:
setelah didapat path dari hidden page ini, selanjutnya kita buka dengan menambahkan pathnya
dibelakang url ```http://<ip machine>:3000/path```
selanjutnya kita coba untuk lihat source code dari page dari hidden path tersebut. ternyata
hidden page tersebut dibuat oleh `arctic digital design` dan ada page githubnya. lalu kita
ke repo dari `arctic digital design` itu, dan lihat isinya, ditemukanlah password dan
username untuk login ke hidden page tersebut.

A3:
Jawaban pertanyaan ketiga didapat setelah login dengan username dan password dari github :D

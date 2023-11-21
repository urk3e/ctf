download data yang dibutuhkan untuk menyelesaikan task.

Q1:What data was exfiltrated via DNS?
Q2:What did Little Timmy want to be for Christmas?
Q3:What was hidden within the file?

A1:
buka file .pcap yang telah didownload menggunakan wireshark dengan command
```
wireshark file.pcap
```
selanjutnya, pada bagian filter masukkan dns. lalu akan terlihat pada tab source dan 
destination bahwa IP 1.1.1.1 mengirimkan data ke IP 192.168.1.107, ketika di follow,
data tersebut berupa `<hex>.holidaythief.com`, karena informasi tersebut ter-encrypt
menggunakan hex, maka kita dapat melakukan decrypt hex tersebut, disini saya menggunakan
tools [cyberchef](cyberchef.org). pada bagian recipe masukkan HEX, dan pada bagian input
masukkan encrypted data tersebut, maka akan keluar hasil decrypted data berupa kalimat.

A2:
selanjutnya kita dapat extract object yang ada pada file .pcap ini. dengan cara
`File>Export Object>HTTP` akan ada 2 file menarik yang ter ekstrak. yaitu 
`christmaslist.zip` dan `TryHackMe.jpg`. ternyata file `christmaslist.zip` membutuhkan
password untuk ekstrak. kita dapat menggunakan tool `zip2john` untuk mengambil informasi
hash, dengan command
```
zip2john christmaslist.zip > hash
```
lalu cek file hash dengan `cat` apakah sudah berisi informasi hash. jika sudah, kita dapat
langsung bruteforce passwordnya dengan menggunakan tools `john` atau john the ripper,
dengan command
```
john hash
```
kita dapatkan password untuk zip tersebut. kita dapat gunakan `unzip` untuk extrak isinya
```
unzip christmaslist.zip
	password: Dec...
```
selanjutnya, karena pertanyaannya adalah apa harapan Timmy, maka kita `cat` file Timmy
```
cat christmaslisttimmy.txt
```

A3:
untuk melihat informasi tersembunyi dari file `TryHackMe.jpg` kita dapat menggunakan
tool `steghide`. dengan cara
```
steghide extract -sf ./TryHackMe.jpg
```
tanpa passphrase.

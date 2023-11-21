download file .pcap yang ada.

Q1:What is the destination IP on packet number 998?
Q2:What item is on the Christmas list?
Q3:Crack buddy's password!

A1:
dalam task ini, kita akan menggunakan Wireshark. Buka file .pcap yang telah didownload
menggunakan Wireshark. lalu karena pertanyaan adalah paket nomor 998, kita bisa langsung
menuju ke paket nomer 998. destination ada diantara tab `Source` dan `Protocol`.

A2:
untuk melihat isi dari paket nomer 998, kita klik kanan, lalu pilih follow,
dan pilih TCP Stream. jawaban ada di teks berwarna merah

A3:
untuk crack password milik user buddy, kita dapat menggunakan `hashcat`. berikut 
adalah hash dari user `buddy`, terletak di paling bawah dari urutan teks yang berwarna 
merah ```buddy:$6$...:18233:0:99999:7:::```
kita dapat mengetahui algoritma hash yang digunakan dari `$6$` di [algoritma hash](https://hashcat.net/wiki/doku.php?id=example_hashes).
sebelum melakukan cracking, kita perlu storing informasi hash ke dalam file, informasi yang
diperlukan adalah dari awal `$6$` sampai sebelum `:` pertama
```
echo "$6$..." >> hash
```
setelahnya kita dapat mulai crack, untuk menggunakan `hashcat`, kita dapat menggunakan command
```
hashcat -m 1800 hash /usr/share/wordlists/rockyou.txt --force
```
atau
```
hashcat -a 0 -m 1800 hash /usr/share/wordlists/rockyou.txt --force
```

nantinya proses cracking akan berjalan, lamanya tergantung performa device yang digunakan.
jika sudah berhasil, nantinya akan keluar output seperti berikut
```
...
* Runtime...: 1 sec

$6$...:<hasil crack>
                                                          
Session..........: hashcat
Status...........: Cracked
...
```

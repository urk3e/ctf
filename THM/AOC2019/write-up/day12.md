download file yang diperlukan untuk menyelesaikan task

<br>Q1:What is the md5 hashsum of the encrypted note1 file?
<br>Q2:Where was elf Bob told to meet Alice?
<br>Q3:Decrypt note2 and obtain the flag!


<br>A1:
<br>untuk mendapatkan md5 hashsum dari note1, kita dapat menggunakan command
```shell
md5sum note1.txt.gpg
```

<br>A2:
<br>dari Hint yang diberikan, gpg key untuk note1 merupakan `25daysofchristmas`, jadi kita
bisa langsung decrypt file tersebut dengan cara
```shell
gpg -d note1.txt.gpg
passphrase:25daysofchristmas
```
nantinya akan keluar jawaban dimana Bob diberitahu untuk bertemu Alice.

<br>A3:
<br>selanjutnya, untuk hint dari Q3 merupakan private password yaitu `hello`, jadi untuk
decrypt note2, kita dapat menggunakan command
```shell
openssl rsautl -decrypt -inkey private.key in note2_encrypted.txt -out note2_dec.txt

passphrase -> hello
```
selanjutnya nanti akan otomatis dibuat file baru bernama `note2_dec.txt`, untuk dapat
melihat isinya, kita dapat gunakan `cat note2_dec.txt`

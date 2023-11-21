target host : 10.10.77.216

nmap scan result:
```shell
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 bc:fe:3a:d4:39:ef:6b:34:2a:70:7f:87:17:b2:91:aa (RSA)
|   256 ee:94:86:78:93:92:e7:e3:94:10:61:0b:07:81:ac:e4 (ECDSA)
|_  256 fc:b6:b8:41:c1:cc:1a:50:58:14:e5:81:c6:bb:df:44 (ED25519)
80/tcp   open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Bastion Hosting
9999/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Index of /
|_http-server-header: nginx/1.18.0 (Ubuntu)
| http-ls: Volume /
| SIZE  TIME               FILENAME
| -     20-Aug-2021 14:10  Credentials/
| 3505  16-Aug-2021 15:17  Credentials/BastionHostingCreds.zip
| 3645  16-Aug-2021 15:15  Credentials/combined.txt
| 2798  09-Aug-2021 23:32  Credentials/emails.txt
| 847   15-Aug-2021 21:47  Credentials/passwords.txt
| 898   14-Aug-2021 03:08  Credentials/usernames.txt
| 9162  07-Aug-2021 18:44  AlteredKeys.zip
|_
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

buka Burp, lalu ke Proxy dan Intercept On. Pada browser lokal (Firefox) gunakan FoxyProxy dan buat setting proxy baru dengan domain `127.0.0.1` dan port `8080` untuk dapat diteruskan request ke BurpSuite, dan aktifkan FoxyProxy. Selanjutnya buka `http://<IP target>`. klik kanan pada tab isi dari tab raw, lalu pilih `Do intercept -> Response to this request`.

langkah-langkah custom requests untuk bypass whitelisting:
- ke page yang ingin di XSS, dalam hal ini `http://<IP target>/ticket`
- pastikan `intercept on` pada burp
- isi email dan content dengan random, misal `a@mail.com` and `hi` for the content. lalu kirim.
- pindah ke burp. pada bagian bawah saat ter-intercept, kita dapat modify request pada bagian `email=a%email.com&content=hi` ganti email dengan `<script>alert('XSS content!')</script>`
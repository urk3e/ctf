use nmap to scan port
> nmap -sV -sC -p 1-2000 IP__

which tcp port is hosting databases
1433

what is the name of the non-administrative share availabele on SMB
> smbclient -L -N IP__
backups

what is the passd that we found on smbclient
connect to smbclient first
> smbclient \\\\IP__\\backups
> get file
M3g4c0rp123

user flag
3e7b102e78218e935bf3f4951fec21a3

root flag
b91ccec3305e98240082d4474b848528


# Ports
There are total 65535 ports that can be used in a device. Ports 0 through 1023 are defined as well-known ports. 
Registered ports are from 1024 to 49151. The remainder of the ports from 49152 to 65535 can be used dynamically 
by applications.

# Nmap
```bash
-sS #for Syn Scan
-sU #for UDP scan
-sT #for TCP scan
-O #for OS det
-sV #for Service det
-v #for Verbosity (could be more, -vv [lv 2 is recommended] ...)
-oA #for saving in all formats avail
-oN #for saving in "normal" format
-oG #for saving in "grepable" format
-A #for Aggresive mode (would do -sV, -O, tracerout, and common script scanning)
-t5 #for fastest timing, default is 3. Be careful with the higher speed, it could be much noise and can incur errors.
-p <port> #for specific port
-p <port>-<port> #for ports in range
-p- #for all ports
--script #for activating script from nmap scripting library
--script=vuln #for activating all scripts in "vuln" category
```

When port scanning with Nmap, there are three basic scan types. These are:
```
-sT # TCP Connect Scans 
-sS # SYN "Half-open" Scans
-sU # UDP Scans
```
Additionally there are several less common port scan types, some of which 
we will also cover (albeit in less detail). These are:
```
-sN # TCP Null Scans 
-sF # TCP FIN Scans 
-sX # TCP Xmas Scans
```

Due to the difficulty in identifying whether a UDP port is actually open, UDP scans tend to be 
slower than TCP (in the refion of 20 min scan the first 1k ports, with good connection). For this,
usually good to run Nmap with `--top-ports <number>` enabled as arguments. (i.e `nmap -sU --top-ports 20 <target>`, which will scan top 20 most commonly used UDP ports.)

## ICMP Network Scanning
or we could call it ping sweep, we can use `-sn` with IP ranges which can be specified using `-` or
CIDR notation. i.e. we want to ping sweep `192.168.0.x` in the network:
- `nmap -sn 192.168.0.1-254`
- `nmap -sn 192.168.0.0/24`
need to run it as root.

## Using Nmap Script
can be done by `--script=<category>`. i.e. `--script=vuln` or `--script=safe`

## Firewall Evasion
other than stealth scan, along with NULL, FIN, and Xmas scans, there is another way to do Firewall 
Evasion. we can use `-Pn`, which tell nmap to treat target host as being alive, effectively bypassing 
the ICMP block; however it comes at the price of potentially taking a very ling time to complete the 
scan, because if the host is really dead then nmap will still be checking and double checking every 
specified port. there is also a lot of other method that we could use for firewall/IDS Evasion we can 
find it in [here](https://nmap.org/book/man-bypass-firewalls-ids.html). some of them are:
- `-f` : to fragment the packets (i.e. split into smaller pieces)
- `--mtu <number>` : alternative to `-f` but we can control over the size of the packets, must
be multiple of 8
- `--scan-delay <time>ms` : add delay between packets sent. useful for evading any time-based IDS
and unstable network
- `--badsum` : used to generate invalid checksum for packets. any real TCP/IP stack would drop this
packets, however firewalls may potentially respond automatically without bothering to check the checksum
of the packet.



# Practical
Does target respond to ICMP req?
- N
Perform Xmas on first 999 ports, how many are shown to be filtered?
- `sudo nmap <IP target> -p1-999 -sX -vv -Pn`
- 999
Reason of the previous question?
- use `--vv`
- no response
Perform TCP SYN scan on first 5000 ports, how many are shown to be open?
- `sudo nmap <IP target> -p1-5000 -sS -Pn`
- 5
- `21/tcp ftp, 53/tcp domain, 80/tcp http, 135/tcp msrpc, 3389/tcp ms-wbt-server`




























# Level 1

1. 48bb6e862e54f2a795ffc4e541caed4d --Hint=md5

```shell
echo "48bb6e862e54f2a795ffc4e541caed4d" > hash1

hashcat -a 0 -m 0 hash1 /usr/share/wordlists/rockyou.txt
```

hasil

```shell
48bb6e862e54f2a795ffc4e541caed4d:easy
```

2. CBFDAC6008F9CAB4083784CBD1874F76618D2A97 --Hint=Sha.. but which version

```shell
echo "CBFDAC6008F9CAB4083784CBD1874F76618D2A97" > hash2

hashcat -a 0 -m 100 hash2 /usr/share/wordlists/rockyou.txt
```

hasil

```shell
cbfdac6008f9cab4083784cbd1874f76618d2a97:password123
```

3. 1C8BFE8F801D79745C4631D09FFF36C82AA37FC4CCE4FC946683D7B336B63032--Hint=Sha...

```shell
echo "1C8BFE8F801D79745C4631D09FFF36C82AA37FC4CCE4FC946683D7B336B63032" > hash3


hashcat -a 0 -m 1400 hash3 /usr/share/wordlists/rockyou.txt
```


```shell
1c8bfe8f801d79745c4631d09fff36c82aa37fc4cce4fc946683d7b336b63032:letmein
```

4. $2y$12$Dwt1BZj6pcyc3Dy1FWZ5ieeUznr71EeNkJkUlypTsgbX1H68wsRom --Hint=Search the hashcat examples page (https://hashcat.net/wiki/doku.php?id=example_hashes) for $2y$. This type of hash can take a very long time to crack, so either filter rockyou for four character words, or use a mask for four lower case alphabetical characters.

```shell
echo "\$2y\$12\$Dwt1BZj6pcyc3Dy1FWZ5ieeUznr71EeNkJkUlypTsgbX1H68wsRom" > hash4

grep -E "^[a-z]{4}$" /usr/share/wordlists/rockyou.txt > wordlists4char.txt

hashcat -a 0 -m 3200 hash4 wordlists4char.txt
```

```
$2y$12$Dwt1BZj6pcyc3Dy1FWZ5ieeUznr71EeNkJkUlypTsgbX1H68wsRom:bleh
```

5. 279412f945939ba78ce0758d3fd83daa --Hint=md4

```shell
echo "279412f945939ba78ce0758d3fd83daa" > hash5

hashcat -a 0 -m 900 hash5
```

```
279412f945939ba78ce0758d3fd83daa:Eternity22
```



# Task 2

1. F09EDCB1FCEFC6DFB23DC3505A882655FF77375ED8AA2D1C13F640FCCC2D0C85

```shell
echo "F09EDCB1FCEFC6DFB23DC3505A882655FF77375ED8AA2D1C13F640FCCC2D0C85" > hash6

hashcat -a 0 -m 1400 hash6
```

```shell
f09edcb1fcefc6dfb23dc3505a882655ff77375ed8aa2d1c13f640fccc2d0c85:paule
```

2. 1DFECA0C002AE40B8619ECF94819CC1B --Hint=NTLM


```shell
echo "1DFECA0C002AE40B8619ECF94819CC1B" > hash7

hashcat -a 0 -m 1000 hash7 /usr/share/wordlists/rockyou.txt
```


```shell
1dfeca0c002ae40b8619ecf94819cc1b:n63umy8lkf4i
```

3. Hash: $6$aReallyHardSalt$6WKUTqzq.UQQmrm0p/T7MPpMbGNnzXPMAXi4bJMl9be.cfi3/qxIf.hsGpS41BqMhSrHVXgMpdjS6xeKZAs02. Salt: aReallyHardSalt

```shell
echo "\$6\$aReallyHardSalt\$6WKUTqzq.UQQmrm0p/T7MPpMbGNnzXPMAXi4bJMl9be.cfi3/qxIf.hsGpS41BqMhSrHVXgMpdjS6xeKZAs02."  > hash8

awk 'length($0) <= 6' /usr/share/wordlists/rockyou.txt > wordlists6char.txt

hashcat -a 0 -m 1800 hash8 wordlists6char.txt
```

```
$6$aReallyHardSalt$6WKUTqzq.UQQmrm0p/T7MPpMbGNnzXPMAXi4bJMl9be.cfi3/qxIf.hsGpS41BqMhSrHVXgMpdjS6xeKZAs02.:waka99
```

4. Hash:e5d8870e5bdd26602cab8dbe07a942c8669e56d6 Salt:tryhackme --Hint=HMAC-SHA1

```shell
echo "e5d8870e5bdd26602cab8dbe07a942c8669e56d6:tryhackme" > hash9

hashcat -a 0 -m 160 hash9 /usr/share/wordlists/rockyou.txt
```

```
e5d8870e5bdd26602cab8dbe07a942c8669e56d6:tryhackme:481616481616
```

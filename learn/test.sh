read -p "input username:" name
read -p "input password" -s Passwd
echo
mysql -u $name -p$Passwd <<eof
show databases;
use learnsql;
show tables;
select * from customer;
exit
eof
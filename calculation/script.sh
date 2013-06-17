#!/bin/bash
statid=$(php /home/martijn/mysqltest/scriptstart.php)
/home/martijn/mysqltest/test2.py >/home/martijn/mysqltest/test2.log
/home/martijn/mysqltest/testmb2.py >/home/martijn/mysqltest/testmb2.log
php /home/martijn/mysqltest/getdataprep.php >/home/martijn/mysqltest/getdataprep.log
php /home/martijn/mysqltest/scriptend.php -- $statid > /home/martijn/mysqltest/end.log


<?php
mysql_connect('localhost', 'python', 'python');
mysql_select_db('test');

$query = "INSERT INTO scriptstats (begin) VALUES (NOW())";
$result = mysql_query($query);
echo mysql_insert_id();

?>

<?php
mysql_connect('localhost', 'python', 'python');
mysql_select_db('test');

if ($argc > 1) {
	$id = $argv[2];

	if (is_numeric($id)) {
		$query = "UPDATE scriptstats SET eind=NOW() WHERE id=$id";
		$result = mysql_query($query);
	}
}
?>

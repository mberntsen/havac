<?php
 
$starttime = microtime(true);
echo "start at " . date('l jS \of F Y h:i:s A') . "\n";

mysql_connect('localhost', 'python', 'python');
mysql_select_db('test');

$query = "SELECT graph_id FROM graphs ORDER BY generationtime ASC LIMIT 0,1";
$result = mysql_query($query);
$row = mysql_fetch_row($result);
$graphid = $row[0];

$t = floor(time() / 60);
$rows = 30*24*60;
$lasttimestamp = $t - $rows;

function getdata($sensorid, $last, $current){
	$query = "SELECT tijd3, waarde FROM metingen WHERE tijd3 > $last AND sensorid=$sensorid";
	$result = mysql_query($query);
	$data = array_fill(0,$current - $last,null);
	while ($row = mysql_fetch_row($result)) {
		$i = $row[0] - $last - 1;
		$data[$i] = (float)($row[1]);
	}
	return $data;
}

function adddatatodb($dataid, $jsondata) {
	$query = "SELECT COUNT(*) FROM content WHERE id=$dataid";
	$result = mysql_query($query);
	$row = mysql_fetch_row($result);
	if ($row[0] == 0) {
		echo "inserting plain content in database (id=$dataid) ";
		$query = "INSERT INTO content (id, datetime, data) VALUES ($dataid,NOW(),\"$jsondata\")";
		if (mysql_query($query))
			echo "success\n";
		else
			echo "failed\n";
	} else {
		echo "updating plain content in database (id=$dataid) ";
		$query = "UPDATE content SET datetime=NOW(), data=\"$jsondata\" WHERE id=$dataid";
		if (mysql_query($query))
			echo " success\n";
		else
			echo " failed\n" ;
	}
}

$databasic = array();
for ($i = 0; $i < $rows; $i++) {
	$databasic[$i] = array($lasttimestamp + $i + 1);
}

$query = "SELECT sensor_id FROM graphs_sensors WHERE graph_id = $graphid ORDER BY sortorder ASC";
$result = mysql_query($query);
while ($row = mysql_fetch_row($result)) {
	$sensorid = $row[0];
	$data = getdata($sensorid, $lasttimestamp, $t);
	for ($i = 0; $i < $rows; $i++) {
		$databasic[$i][] = $data[$i];
	}
}

$outputdata = array(1,$databasic);
$jsondata = json_encode($outputdata);
$jsondatagzip = addslashes(gzencode( trim( preg_replace( '/\s+/', ' ', $jsondata ) ), 9));

adddatatodb($graphid, $jsondata);
adddatatodb($graphid+1000, $jsondatagzip);

$query = "UPDATE graphs SET generationtime = NOW() WHERE graph_id = $graphid";
$result = mysql_query($query);

$endtime = microtime(true);
echo "graph ($graphid) finished in " . number_format($endtime - $starttime, 3, '.', '') . " seconds\n";

?>

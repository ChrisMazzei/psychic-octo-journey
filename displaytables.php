<?php

#`hostname -I` in terminal for apache webpage
$servername = "localhost";
$username = "root";
$password = "root";
$mydb = "dbtest1";

$dbconnect = mysqli_connect($servername, $username, $password, $mydb);

if(!mysqli_select_db){
	echo "database not found";
	echo mysqli_error();
	exit();
}
else{
	$query = "SELECT * FROM stocks";
	$result = mysqli_query($dbconnect, $query);

	echo "<table>";
	while($record = mysqli_fetch_array($result))
		echo "<tr><td>" . $record['Symbol'] . "</td><td>" . $record['Name'] . 
		"</td><td>" . $record['Price'] . "</td><td>" . $record['Change'] . 
		"</td><td>" . $record['percentChange'] . "</td><td>" . $record['Volumn'] . 
		"</td><td>" . $record['AvgVolumn'] . "</td><td>" . $record['MarketCap'] .
	       	"</td><td>" . $record['peRatio'] . "</td></tr>";


	echo "</table>";
	mysqli_close();
}
?>

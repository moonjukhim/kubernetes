<html>
<head><title>Welcome Web Page</title></head>
<body>
<h1>Welcome Web Page</h1>
<?
    $hostname = $_SERVER["HTTP_HOST"]
    echo "Hostname : "; 
    echo $hostname."<br>";
?>
<?php
    $dbserver = "CLOUDSQLIP";
    $dbuser = "blogdbuser";
    $dbpassword = "DBPASSWORD";
    
    $conn = new mysqli($dbserver, $dbuser, $dbpassword);

    if (mysqli_connect_error()) {
            echo ("Database connection failed: " . mysqli_connect_error());
    } else {
            echo ("Database connection succeeded.");
    }
?>
</body></html>
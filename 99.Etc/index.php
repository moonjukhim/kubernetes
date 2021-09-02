<html>
<head><title>Welcome Web Page</title></head>
<body>
<h1>Welcome Web Page</h1>
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
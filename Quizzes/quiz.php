<html>

<head>
    <!-- Bootstrap core CSS -->
    <link href="../libs/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap theme -->
    <link href="../libs/css/bootstrap-theme.min.css" rel="stylesheet">
    <!-- Custom styles for this template -->
    <link href="../libs/css/theme.css" rel="stylesheet">

    <meta http-equiv=Content-Type content="text/html; charset=us-ascii">
    <title>CS 235 - Data Structures</title>
</head>

<body lang=EN-US link=blue vlink=purple>
    <?php include("../navbar.php") ?>
    
    <div class="container theme-showcase" role="main">

<?php
    include('db.php');

    $db = new MyDB();

    if(!$db) {
        echo $db->lastErrorMsg();
    }
    else {

        $db->close();   
    }
?>
</div>
    <!-- Bootstrap core JavaScript
        ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="../libs/jquery-ui-1.10.4.custom/js/jquery-1.11.1.min.js"></script>
    <script src="../libs/js/bootstrap.min.js"></script>
    <script src="../libs/js/docs.min.js"></script>
</body>

</html>
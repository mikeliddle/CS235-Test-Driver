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
    <?php include("config.php") ?>

    <div class="container theme-showcase" role="main">
        
        <form name="quizForm" action="view_quizzes.php" method="post" enctype="multipart/form-data">
            <p>
            <label for="netid">Net ID: </label>
            <input id="txt_NetID" name="netid" type="text" />
            </p>
            <p>
            <label for="emailAddress">Email Address: </label>
            <input id="txt_emailAddress" name="emailAddress" type="text" />
            </p>
            <input type="submit" value="Submit" class="submit" />
        </form>
    </div>
    <!-- Bootstrap core JavaScript
        ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="../libs/jquery-ui-1.10.4.custom/js/jquery-1.11.1.min.js"></script>
    <script src="../libs/js/bootstrap.min.js"></script>
    <script src="../libs/js/docs.min.js"></script>
</body>

</html>
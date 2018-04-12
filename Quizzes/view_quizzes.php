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

        $student_netid = $_POST['netid'];
        $student_email = $_POST['emailAddress'];

        $db = new MyDB();

        if(!$db) {
            echo $db->lastErrorMsg();
        } else {
            $quizzes = $db->get_active_quizzes();

            $db->close();

            echo "<table class=\"table table-striped\">";
            echo "<tr><th>Name</th><th>Date</th><th>Action</th></tr>";
            
            foreach ($quizzes as $quiz) {
                echo "<tr>" . "<td>" . $quiz['NAME'] . "</td>";
                echo "<td>" . $quiz['DATE'] . "</td>";
                echo "<td><form name=\"takeQuiz" . $quiz['ID'] . "\" action=\"quiz.php\" method=\"post\" enctype=\"multipart/form-data\">";
                echo "<input style=\"display: none;\" type=\"hidden\" name=\"quizid\" value=\"" . $quiz['ID'] . "\">";
                echo "<input style=\"display: none;\" type=\"hidden\" name=\"netid\" value=\"" . $student_netid . "\">";
                echo "<input style=\"display: none;\" type=\"hidden\" name=\"emailAddress\" value=\"" . $student_email . "\">";
                echo "<input type=\"submit\" value=\"Take Quiz!\" class=\"submit\">";
                echo "</form></td>" . "</tr>";
            }

            echo "</table>";
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
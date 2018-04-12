<html>

<head>
    <!-- Bootstrap core CSS -->
    <link href="../libs/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap theme -->
    <link href="../libs/css/bootstrap-theme.min.css" rel="stylesheet">
    <!-- Custom styles for this template -->
    <link href="../libs/css/theme.css" rel="stylesheet">

    <meta http-equiv=Content-Type content="text/html; charset=us-ascii">
    <title>Result | CS 235</title>
</head>

<body lang=EN-US link=blue vlink=purple>
    <?php include("../navbar.php") ?>
    
    <div class="container theme-showcase" role="main">
        <div class="container">
    <?php
        include('db.php');

        $student_netid = $_POST['netid'];
        $student_emailAddress = $_POST['emailAddress'];
        $quiz_id = $_POST['quizid'];

        $db = new MyDB();

        if(!$db) {
            echo $db->lastErrorMsg();
        }
        else {
            $quiz_data = $db->get_quiz($quiz_id);

            if(count($quiz_data) > 0 && $quiz_data['ACTIVE'])
            {
                $questions = $db->get_quiz_questions($quiz_id);
                echo "<h1>Quiz: " . $quiz_data['NAME'] . "</h1>";
                echo "<h4>For Date: " . $quiz_data['DATE'] . "</h4>";
                echo "<form name=\"quiz\" action=\"submit_quiz.php\" method=\"post\" enctype=\"multipart/form-data\" >";
                
                // print out each question and its answers.
                foreach ($questions as $question) {
                    echo "<div><p>";
                    echo "<em>" . $question['Q_VALUE'] . "</em>";
                    echo "</p>";
                    if ($question['ANSWER1'])
                    {
                        echo "<p>";
                        echo "<input type=\"radio\" />" . $question['ANSWER1'];
                        echo "</p>";
                    }
                    if ($question['ANSWER2'])
                    {
                        echo "<p>";
                        echo "<input type=\"radio\" />" . $question['ANSWER2'];
                        echo "</p>";
                    }
                    if ($question['ANSWER3'])
                    {
                        echo "<p>";
                        echo "<input type=\"radio\" />" . $question['ANSWER3'];
                        echo "</p>";
                    }
                    if ($question['ANSWER4'])
                    {
                        echo "<p>";
                        echo "<input type=\"radio\" />" . $question['ANSWER4'];
                        echo "</p>";
                    }
                    echo "</div>";
                }

                echo "<input type=\"submit\" value=\"Submit!\" class=\"submit\" />";
                echo "</form>";
            }
            else {
                echo "<h1>Quiz has closed!</h1>";
            }
            
            $db->close();
        }
    ?>
        </div>
    </div>

    <!-- Bootstrap core JavaScript
        ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="../libs/jquery-ui-1.10.4.custom/js/jquery-1.11.1.min.js"></script>
    <script src="../libs/js/bootstrap.min.js"></script>
    <script src="../libs/js/docs.min.js"></script>
</body>

</html>
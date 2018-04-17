<html>

<head>
    <!-- Bootstrap core CSS -->
    <link href="../libs/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap theme -->
    <link href="../libs/css/bootstrap-theme.min.css" rel="stylesheet">
    <!-- Custom styles for this template -->
    <link href="../libs/css/theme.css" rel="stylesheet">

    <meta http-equiv=Content-Type content="text/html; charset=us-ascii">
    <title>Quiz Admin |CS 235</title>
</head>

<body lang=EN-US link=blue vlink=purple>
    <?php include("../navbar.php") ?>

    <div class="container theme-showcase" role="main">
        <div class="container">
            <?php
            include('db.php');

            $db = new MyDB();

            if(!$db) {
                echo $db->lastErrorMsg();
            }
            else {
                $quizzes = $db->get_all_quizzes();

                echo "<table class=\"table table-hover table-responsive\">\n";
                echo "<thead>\n<tr><th>ID</th>";
                echo "<th>Name</th>";
                echo "<th>Date</th>";
                echo "<th>Active</th>";
                echo "</tr></thead>\n";
                echo "<tbody>\n";

                foreach ($quizzes as $quiz) {
                    echo "<tr id=\"quiz" . $quiz['ID'] . "\" onclick=\"view_quiz_form(" . $quiz['ID'] . ")\">";
                    echo "<td>" . $quiz['ID'] . "</td>";
                    echo "<td>" . $quiz['NAME'] . "</td>";
                    echo "<td>" . $quiz['DATE'] . "</td>";
                    echo "<td>" . $quiz['ACTIVE'] . "</td>";
                    echo "</tr>";
                    echo "\n";
                }

                echo "</tbody>";
                echo "</table>\n";

                $db->close();
            }
            ?>
            <div class="panel">
                <div class="panel-body" id="quiz_form">

                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap core JavaScript
        ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="../libs/jquery-ui-1.10.4.custom/js/jquery-1.11.1.min.js"></script>
    <script src="../libs/js/bootstrap.min.js"></script>
    <script src="../libs/js/docs.min.js"></script>
    <script>
        function view_quiz_form(id) {
            $.post("quiz_form.php", {quiz_id: id}, function(data, status) {
                console.log("Status: " + status);
                if (status == "success") {
                    $('#quiz_form').html(data);
                }
            });
        }
    </script>
</body>

</html>
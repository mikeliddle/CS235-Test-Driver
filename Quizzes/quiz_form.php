<div class="container">
    <script>
        var question_number = 0;
        var questionsToAnswers = {};

        function add_question() {
            console.log(question_number);
            
            questionsToAnswers[question_number] = 0;

            var question = document.createElement("div");
            question.setAttribute("id", "question" + question_number);
            question.classList.add("form-group");
            
            var columnOne = document.createElement("label");
            columnOne.classList.add("control-label") 
            columnOne.classList.add("col-sm-4");
            columnOne.setAttribute("for", "txt_question" + question_number);
            columnOne.textContent = "Question: ";
            
            var columnTwo = document.createElement("input");
            columnTwo.classList.add("col-sm-8");
            columnTwo.setAttribute("id", "txt_question" + question_number);
            columnTwo.setAttribute("name", "txt_question" + question_number);
            columnTwo.setAttribute("type", "text");

            var addAnswerButton = document.createElement("button");
            addAnswerButton.classList.add("btn");
            addAnswerButton.classList.add("btn-primary");
            addAnswerButton.setAttribute("type", "button");
            addAnswerButton.setAttribute("onclick", "addAnswer(" + question_number + ")");
            addAnswerButton.innerHTML = "Add Answer";
            
            question.appendChild(columnOne);
            question.appendChild(columnTwo);
            question.appendChild(addAnswerButton);

            document.getElementById("questions").appendChild(question);

            question_number++;
        }

        function addAnswer(qNumber) {
            if(questionsToAnswers[qNumber] < 4) {
                var question = document.getElementById("question" + qNumber);
                var div_container = document.createElement("div");
                var answerOne = document.createElement("label");
                answerOne.classList.add("control-label") 
                answerOne.classList.add("col-sm-4");
                answerOne.setAttribute("for", "answer" + question_number);
                answerOne.textContent = "Answer: ";
                
                var answerTwo = document.createElement("input");
                answerTwo.classList.add("col-sm-6");
                answerTwo.setAttribute("id", "answer" + question_number);
                answerTwo.setAttribute("name", "answer" + question_number);
                answerTwo.setAttribute("type", "text");

                var isCorrect = document.createElement("input");
                isCorrect.classList.add("col-sm-2");
                isCorrect.setAttribute("type", "checkbox");
                isCorrect.setAttribute("name", "isAnswer" + questionsToAnswers[qNumber] + "correct");
                isCorrect.innerHTML = "Is this answer the right answer?";
                div_container.appendChild(answerOne);
                div_container.appendChild(answerTwo);
                div_container.appendChild(isCorrect);
                question.appendChild(div_container);

                questionsToAnswers[qNumber] += 1;
            }
        }
    </script>
    <?php
        include('db.php');
        $quiz_id = $_POST['quiz_id'];

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
                echo "<form name=\"quiz\" width=\"100%\" class=\"form-horizontal\" action=\"submit_quiz.php\" method=\"post\" enctype=\"multipart/form-data\" >
        <div class=\"form-group\">
                <label class=\"control-label col-sm-4\" for=\"quiz_name\">What would you like to name the quiz? </label>
                <div class=\"col-sm-8\">
                <input required type=\"text\" name=\"quiz_name\" value=\"" . $quiz_data['NAME'] . "\"/>
                </div>
        </div>";
        echo "<input type=\"hidden\" name=\"netid\" value=\"". $student_netid ."\" />";
                echo "<input type=\"hidden\" name=\"emailAddress\" value=\"". $student_emailAddress ."\" />";
                echo "<input type=\"hidden\" name=\"quizid\" value=\"". $quiz_id ."\" />";
        echo "<div class=\"form-group\">
                    <label class=\"control-label col-sm-4\" for=\"quiz_date\">When is this quiz for?</label>
                    <div class=\"col-sm-8\">
                        <input required type=\"date\" name=\"quiz_date\" value=\"" . $quiz_data['DATE'] . "\" />
                    </div>
            </div>";
        echo "<div class=\"form-group\">
                    <div id=\"questions\">
                        <button type=\"button\" onclick=\"add_question()\" class=\"btn btn-primary\">Add Question!</button>
                    </div>
            </div>";
        
    
                
                
                // print out each question and its answers.
                foreach ($questions as $question) {
                    echo "<div><p>";
                    echo "<em>" . $question['Q_VALUE'] . "</em>";
                    echo "</p>";
                    if ($question['ANSWER1'])
                    {
                        echo "<p>";
                        echo "<input name=\"answer". $question['ID'] . "\" type=\"radio\" />" . $question['ANSWER1'];
                        echo "</p>";
                    }
                    if ($question['ANSWER2'])
                    {
                        echo "<p>";
                        echo "<input name=\"answer". $question['ID'] . "\"  type=\"radio\" />" . $question['ANSWER2'];
                        echo "</p>";
                    }
                    if ($question['ANSWER3'])
                    {
                        echo "<p>";
                        echo "<input name=\"answer". $question['ID'] . "\" type=\"radio\" />" . $question['ANSWER3'];
                        echo "</p>";
                    }
                    if ($question['ANSWER4'])
                    {
                        echo "<p>";
                        echo "<input name=\"answer". $question['ID'] . "\" type=\"radio\" />" . $question['ANSWER4'];
                        echo "</p>";
                    }
                    echo "</div>";
                }
                echo "<div class=\"form-group\">
                    <p>
                        <label class=\"control-label col-sm-4\" for=\"secret\">Secret: </label>
                        <div class=\"col-sm-8\">
                            <input required type=\"password\" name=\"secret\" />
                        </div>
                    </p>
                </div>";

                echo "<div class=\"form-group\">   
                <div class=\"col-sm-offset-2 col-sm-8\">
                    <input type=\"submit\" value=\"Submit!\" class=\"btn btn-primary active\" />
                </div>
            </div>";
                echo "</form>";
            }
            else {
                echo "<h1>Quiz has closed!</h1>";
            }
            
            $db->close();
        }
        ?>
</div>
                        
<!-- </div> -->
<?php
    class MyDB extends SQLite3 {

        function __construct() {
            $DB_FILE = 'quizzes.db';
            $this->open($DB_FILE);
            $this->init_db();
        }

        function init_db() {
            $create_tables ="
                CREATE TABLE IF NOT EXISTS QUIZ
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME           VARCHAR(50) NOT NULL,
                DATE           DATETIME    NOT NULL,
                ACTIVE         INTEGER     NOT NULL
                );
                CREATE TABLE IF NOT EXISTS USER
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME           VARCHAR(50),
                NETID          VARCHAR(50),
                ACTIVE         INTEGER     NOT NULL
                );
                CREATE TABLE IF NOT EXISTS RESPONSE
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                DATE           DATETIME     NOT NULL,
                USER           INTEGER      NOT NULL,
                QUIZ           INTEGER      NOT NULL,
                ANSWER         VARCHAR(200)
                );
                CREATE TABLE IF NOT EXISTS QUESTION
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Q_VALUE        VARCHAR(200),
                ANSWER1        VARCHAR(200),
                ANSWER2        VARCHAR(200),
                ANSWER3        VARCHAR(200),
                ANSWER4        VARCHAR(200),
                QUIZ_ID        INTEGER       NOT NULL
                );
            ";
            $ret = $this->exec($create_tables);
            if(!$ret) {
                echo $this->lastErrorMsg();
            } else {
                // do nothing, success!
            }
        }

        function get_active_quizzes() {
            $sql ="
                SELECT * FROM QUIZ WHERE QUIZ.ACTIVE=1 
            ";

            $ret = $this->query($sql);
            $results = array();
            
            while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
                array_push($results, $row);
            }

            return $results;
        }
    }
?>
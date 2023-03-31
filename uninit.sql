--drop tables & functions
DROP TABLE quiz_questions;
DROP TABLE quizzes;
DROP TABLE questions;
DROP FUNCTION add_quiz(text, INTEGER, INTEGER, INTEGER[]);
DROP FUNCTION delete_quiz(INTEGER);
DROP FUNCTION current_question_id();
DROP FUNCTION current_quiz_id();
DROP FUNCTION delete_question(INTEGER);


--move out of quiz_app database
\c postgres
DROP DATABASE quiz_app;

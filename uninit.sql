DROP TABLE quiz_questions;
DROP TABLE quizzes;
DROP TABLE questions;
DEALLOCATE questions_by_subject;
DEALLOCATE questions_by_author;
DEALLOCATE questions_by_id;
DEALLOCATE questions_by_regex;
DEALLOCATE add_question;
DEALLOCATE delete_question;
DROP FUNCTION add_quiz(text, INTEGER, text, text[]);
DROP FUNCTION delete_quiz(text);
DEALLOCATE add_quiz;
DEALLOCATE delete_quiz;
DROP FUNCTION current_question_id();
DROP FUNCTION current_quiz_id();
DROP FUNCTION delete_question(INTEGER);


--move out of quiz_app database
\c postgres
DROP DATABASE quiz_app;

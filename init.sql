--first create the database
CREATE DATABASE quiz_app;

--move into the new database
\c quiz_app

--create a questions table
CREATE TABLE questions(
    Question    VARCHAR(150) NOT NULL,
    A   VARCHAR(50) NOT NULL,
    B   VARCHAR(50) NOT NULL,
    C   VARCHAR(50) NOT NULL,
    D   VARCHAR(50) NOT NULL,
    Subjects    text[]  NOT NULL,
    Author  VARCHAR(50) NOT NULL,
    Answer  VARCHAR(1)  NOT NULL,
    ID  INTEGER NOT NULL,
    PRIMARY KEY(ID)
);

--create a quizzes table
CREATE TABLE quizzes(
    Creator     VARCHAR(50) NOT NULL,
    NumQuestions    INT NOT NULL,
    ID  INTEGER NOT NULL,
    PRIMARY KEY(ID)
);

--create a table mapping questions to quizzes
CREATE TABLE quiz_questions(
    QuizID  INTEGER NOT NULL REFERENCES quizzes(ID),
    QuestionID  INTEGER NOT NULL REFERENCES questions(ID),
    PRIMARY KEY(QuizID,QuestionID)
);


--add some default data
INSERT INTO questions(Question,A,B,C,D,Subjects,Author,Answer,ID)
VALUES 
(
    'How many states of matter are there?',
    '1',
    '2',
    '3',
    '4',
    ARRAY['Science'],
    'Default',
    'D',
    1
),
(
    'What is the acceleration of gravity in m^2/s?',
    '9.81',
    '10',
    '3.14',
    '1',
    ARRAY['Science','Physics'],
    'Default',
    'A',
    2
),
(
    'What is the equation to calculate pressure?',
    'F = ma',
    's = F/A',
    'P = F/A',
    'p = m/V',
    ARRAY['Physics', 'Engineering'],
    'Default',
    'C',
    3
);

INSERT INTO quizzes(Creator,NumQuestions,ID)
VALUES 
(
    'Default',
    3,
    1
);

INSERT INTO quiz_questions(QuizID,QuestionID)
VALUES
(
    1,1
),
(
    1,2
),
(
    1,3
);


--search questions by subject
PREPARE questions_by_subject(text) AS
SELECT * FROM questions WHERE $1 = ANY(Subjects);

--search questions by author
PREPARE questions_by_author(text) AS
SELECT * FROM questions WHERE Author = $1;

--search questions by id 
PREPARE questions_by_id(INTEGER) AS
SELECT * FROM questions WHERE ID = $1;

--search questions by regex
PREPARE questions_by_regex(text) AS
SELECT * FROM questions WHERE Question ~* $1;

--insert question
PREPARE add_question(text,text,text,text,text,text[],text,text,INTEGER) AS
INSERT INTO questions VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9);

--delete question
PREPARE delete_question(INTEGER) AS
DELETE FROM questions WHERE ID = $1;

--add quiz
CREATE FUNCTION add_quiz(Creator text, NumQuestions INTEGER, ID INTEGER, questions INTEGER[])
RETURNS VOID AS
$$
DECLARE 
    i INT;
BEGIN
    INSERT INTO quizzes VALUES (Creator, NumQuestions, ID);

    FOR i IN 1..array_length(questions, 1) LOOP
        INSERT INTO quiz_questions VALUES (ID,questions[i]);
    END LOOP;
END;
$$
LANGUAGE plpgsql;

PREPARE add_quiz(text, INTEGER, INTEGER, INTEGER[]) AS
SELECT add_quiz($1,$2,$3,$4);

--delete quiz
CREATE FUNCTION delete_quiz(delID INTEGER)
RETURNS VOID AS
$$ 
BEGIN
    DELETE FROM quiz_questions WHERE QuizID = delID;
    DELETE FROM quizzes WHERE ID = delID;
END;
$$
LANGUAGE plpgsql;

PREPARE delete_quiz(INTEGER) AS
SELECT delete_quiz($1);

--delete quiz
CREATE FUNCTION delete_question(delID INTEGER)
RETURNS VOID AS
$$ 
BEGIN
    DELETE FROM quiz_questions WHERE QuestionID = delID;
    DELETE FROM questions WHERE ID = delID;
END;
$$
LANGUAGE plpgsql;

CREATE FUNCTION current_question_id()
RETURNS INTEGER AS
$$
BEGIN
    RETURN(
    SELECT max(ID)
    FROM questions
    );
END;
$$
LANGUAGE plpgsql;

CREATE FUNCTION current_quiz_id()
RETURNS INTEGER AS
$$
BEGIN
    RETURN(
    SELECT max(ID)
    FROM quizzes
    );
END;
$$
LANGUAGE plpgsql;
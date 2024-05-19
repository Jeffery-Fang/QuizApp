<br />
<h3>
    About The Project
</h3>

---
A CLI application that lets the user add, delete and modify questions and quizzes and use those for test practice or studying.

### Prerequisites
In order to use this application you will need to have psycopg2 installed.

## Installation

1. Clone this repository
    ```sh
    git clone https://github.com/Jeffery-Fang/QuizApp.git
    ```

2. Open a terminal in this folder and connect to the PostgreSQL server
    ```sh
    psql -U postgres
    ```

3. Initialize the database by running the initialization script
    ```sh
    \i init.sql
    ```

4. Change the database variables in the main function to match your PostgreSQL credentials
    ```sh
    user = "postgres"
    password = "your password"
    ```
5. Leave psql and start the application
    ```sh
    \q
    python app.py
    ```

## Gallery & Demonstrations

https://github.com/Jeffery-Fang/QuizApp/assets/126544955/af081baa-84ec-4aab-916a-31b0aad51a42

*General Use*

https://github.com/Jeffery-Fang/QuizApp/assets/126544955/dd9b3436-d028-4623-b066-d72fd5af06ec

*Adding a Quiz*

## Tools & Technologies

- Python
- Postgres
- Psycopg2








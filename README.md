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
    git clone https://github.com/Jeffery-Fang/PersonalWebsite.git
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


## Tools & Technologies

- Python
- Postgres
- Psycopg2








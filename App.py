import psycopg2
class Question:
    '''
    question class groups information about a given question entity in the 
    database schema 
    '''
    def __init__(self, question, a, b, c, d, subjects, author, answer, id):
        '''
        constructor for question class
        initializes the question with given information
        '''
        
        self.question = question
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.subjects = subjects
        self.author = author
        self.answer = answer
        self.id = id
    
    def __str__(self):
        '''
        toString for question class
        '''

        return f"<{self.question},{self.a},{self.b},{self.c},{self.d},{self.subjects},{self.author},{self.answer},{str(self.id)}>"
    
    def display(self):
        '''
        displays the question in a presentable way
        '''

        print("Question: ", self.question)
        print("A. ", self.a)
        print("B. ", self.b)
        print("C. ", self.c)
        print("D. ", self.d)
        print("Answer: ", self.answer)
        print("Subjects", str(self.subjects))
        print("Author: ", self.author)
        print("QuestionID: ", self.id)
        print("")


    def getID(self):
        '''
        returns questionID
        '''

        return self.id
    
    def getQuestion(self):
        '''
        returns the question
        '''
        
        return self.question
    
    def ask(self):
        '''
        presents the question along with options
        '''

        print(self.question)
        print("A. " + self.a)
        print("B. " + self.b)
        print("C. " + self.c)
        print("D. " + self.d)

    def solve(self,answer):
        '''
        asks the questions and checks if it's correct
        '''

        if(answer == self.answer):
            print("Correct\n")
            return True
        else:
            print("Incorrect\n")
            return False
        
class Quiz:
    '''
    quiz class groups information about a quiz entity in the 
    database schema 
    '''

    def __init__(self, quizName, id, cur):
        '''
        constructor for quiz class
        initializes quiz with questions associated with the quizID in the database
        '''

        self.quizName = quizName
        self.id = id
        self.questions = []
        self.questions = self.getQuizz_questionsByQuizID(cur,self.id)
        self.numQuestions = len(self.questions)

    def __str__(self):
        '''
        toString for quiz class
        '''

        return f"<{self.quizName},{self.numQuestions},{str(self.id)},{self.questions}>"
    
    def display(self):
        '''
        diplays information about the quiz in a presentable way
        '''

        print("Quiz name: ", self.quizName)
        print("Length: ", self.numQuestions)
        print("QuizID: ", self.id)
        print("")

    def addQuestion(self,Q):
        '''
        add a question to the questions list
        '''

        self.questions.append(Q)
        self.numQuestions = len(self.questions)

    def questionsToIDs(self):
        '''
        returns the id of all the questions in this quizzes questions list
        '''

        out = []

        for i in self.questions:
            out.append(i.getID())

        return out
    
    def ask(self):
        '''
        asks this quiz by running ask on all the questions in the questions list
        '''

        score = 0

        for i in self.questions:
            i.ask()
            answer = input("Enter answer:")

            if(i.solve(answer) == True):
                score += 1
            
        print("")
        print("Score: " + str(score)+"/"+str(self.numQuestions)+"\n")

    def getQuizz_questionsByQuizID(self,cursor,quizid):
        '''
        returns an array of questiosn associated with this quizID from the database
        '''

        cursor.execute(f"SELECT * FROM questions q WHERE EXISTS(SELECT * FROM quiz_questions qq WHERE qq.QuizID = " + "'" + str(quizid) + "' AND qq.QuestionID = Q.ID);")
        results = cursor.fetchall()
    
        out = []

        for i in results:
            out.append(Question(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))

        return out


class Factory:
    '''
    factory class simplifies the creation and deletion of questions and quizzes
    '''
    def __init__(self,cursor):
        '''
        constructor for factory class
        '''

        temp = self.getCurrentIDs(cursor)
        self.currentQuizID = temp[0]
        self.currentQuestionID = temp[1]

    def getCurrentIDs(self,cursor):
        '''
        gets the highest quizID and questionID in order to prevent
        repeated IDs
        '''

        cursor.execute(f"SELECT current_quiz_id();")
        current_quiz_id = cursor.fetchone()[0]+1
        cursor.execute(f"SELECT current_question_id();")
        current_question_id = cursor.fetchone()[0]+1

        return (current_quiz_id, current_question_id)
    
    def refreshIDs(self,cursor):
        '''
        refreshs the current IDs
        '''

        temp = self.getCurrentIDs(cursor)
        self.currentQuizID = temp[0]
        self.currentQuestionID = temp[1]
    
    def createQuestion(self,cursor):
        '''
        creates a single question with user input and adds it to the database
        '''

        print("-----Creating a question-----\n")

        question = input("What is the question?\n")
        a = input("What is option A?\n")
        b = input("What is option B?\n")
        c = input("What is option C?\n")
        d = input("What is option D?\n")
        subjects = []
        temp = input("What are the subjects? Type -1 when done entering\n")
        
        while(temp != '-1'):
            subjects.append(temp)
            temp = input()

        author = input("Who made this question?\n")
        answer = input("What is the answer?\n")
        
        temp = Question(question,a,b,c,d,subjects,author,answer[0],self.currentQuestionID)
        self.addQuestion(cursor,temp)
        self.refreshIDs(cursor)

    def deleteQuestion(self,cursor):
        '''
        deletes a question according to questionID and removes it from the database
        '''

        print("-----Deleting a question-----\n")

        results = self.getQuestions(cursor)

        for i in results:
            i.display()

        delID = int(input("Which question do you want to delete?\n"))

        if(delID >= self.currentQuestionID or delID <= 0):
            print("\n[ERROR: QuestionID out of range]\n")
            return

        cursor.execute(f"SELECT delete_question("+str(delID)+");")

    def createQuiz(self,cursor):
        '''
        create a quiz according to user input and add it to the database
        '''

        print("-----Creating a quiz-----\n")

        quizname = input("What is the name of the quiz?\n")

        option = input("Filter the question database?\n 1.No Filter\n 2.Filter by subject\n 3.Filter by author\n 4.Find with pattern match\n")

        if(option == '1'):
            results = self.getQuestions(cursor)

            for i in results:
                print(i.getQuestion(), " id: ", i.getID())

        elif(option == '2'):
            temp = input("What subject?\n")
            results = self.getQuestionsBySubject(cursor,temp)

            for i in results:
                print(i.getQuestion(), " id: ", i.getID(), " subjects: ",i.subjects)

        elif(option == '3'):
            temp = input("What author?\n")
            results = self.getQuestionsByAuthor(cursor,temp)

            for i in results:
                print(i.getQuestion(), " id: ", i.getID(), " author: ", i.author)

        elif(option == '4'):
            temp = input("What pattern?\n")
            results = self.getQuestionsByPattern(cursor,temp)

            for i in results:
                print(i.getQuestion(), " id: ", i.getID(), " pattern: ", temp)

        questions = set()
        done = input("Type in question id to add to the quiz and -1 when you're done\n")

        while(done != '-1'):
            if(int(done) >= self.currentQuestionID or int(done) <= 0):
                print("\n[ERROR: QuestionID out of range]\n")
                return

            questions.add(int(done))
            done = input()

        
        temp = Quiz(quizname,self.currentQuizID,cursor)
        temp.numQuestions = len(questions)

        self.addQuiz(cursor,temp,list(questions))

        Quiz(quizname,self.currentQuizID,cursor)

        self.refreshIDs(cursor)

    def deleteQuiz(self,cursor):
        '''
        delete a quiz according to quizID and remove it and associated quiz_questions
        from the database
        '''

        print("-----Deleting quiz-----\n")

        results = self.getQuizzes(cursor)

        for i in results:
            i.display()
            print("")

        temp = input("Type in id of the quiz you want to delete\n")

        if(int(temp) >= self.currentQuizID or int(temp) <= 0):
            print("\n[ERROR: QuizID out of range]\n")
            return

        cursor.execute(f"SELECT delete_quiz("+"'"+temp+"'"+");")

    def getQuizzes(self,cursor):
        '''
        retrieve all the quizzes from the database
        '''

        cursor.execute(f"SELECT * FROM quizzes")
        results = cursor.fetchall()

        out = []

        for i in results:
            out.append(Quiz(i[0],int(i[2]),cursor))

        return out    

    def getQuizzesByID(self,cursor,id):
        '''
        retrieve quizzes with the given ID
        '''

        cursor.execute(f"SELECT * FROM quizzes WHERE ID = "+"'"+str(id)+"';")
        results = cursor.fetchone()

        out = Quiz(results[0],results[2],cursor)

        return out    

    def getQuestions(self,cursor):
        '''
        retrieve all questions from the database
        '''

        cursor.execute(f"SELECT * FROM questions")
        results = cursor.fetchall()

        out = []

        for i in results:
            out.append(Question(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))

        return out
    

    def getQuestionsBySubject(self,cursor,subject):
        '''
        retrieve questions with the given subject
        '''

        cursor.execute(f"SELECT * FROM questions WHERE "+"'"+subject+"' ~* ANY(Subjects);")
        results = cursor.fetchall()
    
        out = []

        for i in results:
            out.append(Question(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))

        return out

     
    def getQuestionsByAuthor(self,cursor,author):
        '''
        retrieve questions with the given author
        '''

        cursor.execute(f"SELECT * FROM questions WHERE Author ~*"+"'"+author+"';")
        results = cursor.fetchall()
    
        out = []

        for i in results:
            out.append(Question(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))

        return out
    
    def getQuestionsByPattern(self,cursor,pattern):
        '''
        retrieve questions with the given pattern
        '''

        cursor.execute(f"SELECT * FROM questions WHERE Question ~*"+"'"+pattern+"';")
        results = cursor.fetchall()
   
        out = []

        for i in results:
            out.append(Question(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))

        return out

    def addQuestion(self,cursor,Q):
        '''
        generic add question query
        '''

        cursor.execute(f"INSERT INTO questions VALUES("+"'"+Q.question+"'"+","+"'"+Q.a+"'"+","+"'"+Q.b+"'"+","+"'"+Q.c+"'"+","+"'"+Q.d+"'"+","+"ARRAY"+str(Q.subjects)+","+"'"+Q.author+"'"+","+"'"+Q.answer+"'"+","+"'"+str(Q.id)+"'"+");")
    
    def addQuiz(self,cursor,Q,questions):
        '''
        generic add quiz query
        '''

        cursor.execute(f"SELECT add_quiz("+"'"+Q.quizName+"'"+","+"'"+str(Q.numQuestions)+"'"+","+"'"+str(Q.id)+"'"+","+"ARRAY"+str(questions)+");")
        
    def getQuizz_questions(self,cursor):
        '''
        generic get quiz_questions query
        '''

        cursor.execute(f"SELECT * FROM quiz_questions")
        results = cursor.fetchall()
        return results
    
    def update_question(self,cursor):
        '''
        gather user input and do an UPDATE query with new fields
        '''

        print("-----Updating a question-----\n")
        
        editID = int(input("What is the id of the question you want to edit?\n"))

        if(editID >= self.currentQuestionID or editID <= 0):
            print("\n[ERROR: QuestionID out of range]\n")
            return

        question = input("What is the question?\n")
        a = input("What is option A?\n")
        b = input("What is option B?\n")
        c = input("What is option C?\n")
        d = input("What is option D?\n")
        subjects = []
        temp = input("What are the subjects? Type -1 when done entering\n")
        
        while(temp != '-1'):
            subjects.append(temp)
            temp = input()

        author = input("Who made this question?\n")
        answer = input("What is the answer?\n")
        cursor.execute(f"UPDATE questions SET question="+"'"+question+"'"+","+"a="+"'"+a+"'"+","+"b="+"'"+b+"'"+","+"c="+"'"+c+"'"+","+"d="+"'"+d+"'"+","+"subjects="+"ARRAY"+str(subjects)+","+"author='"+author+"'"+","+"answer='"+answer+"' WHERE id = " + str(editID))

    def update_quiz(self,cursor):
        '''
        gather user input and do an UPDATE query with new fields
        additionally we need to update the quiz_questions table
        '''

        print("-----updating a quiz-----\n")

        editID = int(input("What is the id of the quiz?\n"))

        if(editID >= self.currentQuizID or editID <= 0):
            print("\n[ERROR: QuestionID out of range]\n")
            return
        
        quizname = input("Who is the quiz name?\n")

        option = input("Filter the question database?\n 1.No Filter\n 2.Filter by subject\n 3.Filter by author\n 4.Find with pattern match\n")

        if(option == '1'):
            results = self.getQuestions(cursor)

            for i in results:
                print(i.getQuestion(), " id: ", i.getID())

        elif(option == '2'):
            temp = input("What subject?\n")
            results = self.getQuestionsBySubject(cursor,temp)

            for i in results:
                print(i.getQuestion(), " id: ", i.getID(), " subjects: ",i.subjects)

        elif(option == '3'):
            temp = input("What author?\n")
            results = self.getQuestionsByAuthor(cursor,temp)

            for i in results:
                print(i.getQuestion(), " id: ", i.getID(), " author: ", i.author)

        elif(option == '4'):
            temp = input("What pattern?\n")
            results = self.getQuestionsByPattern(cursor,temp)

            for i in results:
                print(i.getQuestion(), " id: ", i.getID(), " pattern: ", temp)

        questions = set()
        done = input("Type in question id to add to the quiz and -1 when you're done\n")

        while(done != '-1'):
            if(int(done) >= self.currentQuestionID or int(done) <= 0):
                print("\n[ERROR: QuestionID out of range]\n")
                return

            questions.add(int(done))
            done = input()

        cursor.execute(f"SELECT update_quiz("+"'"+quizname+"'"+","+"'"+str(len(questions))+"'"+","+"'"+str(editID)+"'"+","+"ARRAY"+str(list(questions))+");")


def main():
    #setup a connection to the database replace with your credentials
    
    dbname = "quiz_app"
    user = "postgres"
    password = "super"
    host = "localhost"
    port = "5432"

    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )

    #create a cursor
    cur = conn.cursor()

    #create a factory object for creating questions & quizzes
    fact = Factory(cur)

    #loop over options until user ends program
    while(True):
        print("\nWhat would you like to do?\n1.View the question database\n2.View the quizzes database\n3.Take a quiz\n4.Add or remove a question\n5.Add or remove a quiz\n6.Exit program")
        selection = input()

        if(selection == '1'):
            results = fact.getQuestions(cur)
            
            for i in results:
                i.display()

        elif(selection == '2'):
            results = fact.getQuizzes(cur)

            for i in results:
                i.display()

        elif(selection == '3'):
            results = fact.getQuizzes(cur)

            for i in results:
                i.display()

            taking = input("Which quiz do you want to take?\n")

            if(int(taking) <= 0 or int(taking) >= fact.currentQuizID):
                print("\n[ERROR: QuizID out of range]\n")
                continue

            results = fact.getQuizzesByID(cur,int(taking))

            results.ask()

            
        elif(selection == '4'):
            choice = input("Do you want to \n1.Add a question?\n2.Delete a question?\n3.Update a question?\n4.Cancel\n")

            if(choice == '1'):
                fact.createQuestion(cur)
            elif(choice == '2'):
                fact.deleteQuestion(cur)
            elif(choice == '3'):
                results = fact.getQuestions(cur)
            
                for i in results:
                    i.display()

                fact.update_question(cur)

            elif(choice == '4'):
                continue
            else:
                print("Select valid option")

            conn.commit()


        elif(selection == '5'):
            choice = input("Do you want to \n1.Create a quiz?\n2.Delete a quiz?\n3.Update a quiz?\n4.Cancel\n")

            if(choice == '1'):
                fact.createQuiz(cur)
            elif(choice == '2'):
                fact.deleteQuiz(cur)
            elif(choice == '3'):
                results = fact.getQuizzes(cur)
            
                for i in results:
                    i.display()

                fact.update_quiz(cur)

            elif(choice == '4'):
                continue
            else:
                print("Select valid option")

            conn.commit()

        elif(selection == '6'):
            break

        else:
            print("Enter a valid option")

    #commit changes and close cursor & connection
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()


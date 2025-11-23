import sqlite3


conn = sqlite3.connect(r"C:\Users\idyas\Desktop\Питончик\Sql\university.db")
cursor = conn.cursor()

try:

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        age INTEGER,
        city TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        time_start TEXT,
        time_end TEXT
    )
    ''')

    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Student_courses (
        student_id INTEGER,
        course_id INTEGER,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES Students(id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES Courses(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute("DELETE FROM Student_courses")
    cursor.execute("DELETE FROM Students")
    cursor.execute("DELETE FROM Courses")

    cursor.execute("INSERT INTO Courses VALUES (1, 'python', '21.07.21', '21.08.21')")
    cursor.execute("INSERT INTO Courses VALUES (2, 'java', '13.07.21', '16.08.21')")
    
    cursor.execute("INSERT INTO Students VALUES (1, 'Max', 'Brooks', 24, 'Spb')")
    cursor.execute("INSERT INTO Students VALUES (2, 'John', 'Stones', 15, 'Spb')")
    cursor.execute("INSERT INTO Students VALUES (3, 'Andy', 'Wings', 45, 'Manhester')")
    cursor.execute("INSERT INTO Students VALUES (4, 'Kate', 'Brooks', 34, 'Spb')")
    
    cursor.execute("INSERT INTO Student_courses VALUES (1, 1)")
    cursor.execute("INSERT INTO Student_courses VALUES (2, 1)")
    cursor.execute("INSERT INTO Student_courses VALUES (3, 1)")
    cursor.execute("INSERT INTO Student_courses VALUES (4, 2)")


    print("1. Студенты старше 30 лет:")
    cursor.execute("SELECT * FROM Students WHERE age > 30")
    students_over_30 = cursor.fetchall()
    for student in students_over_30:
        print(student)
    print()

 
    print("2. Студенты на курсе Python:")
    cursor.execute('''
        SELECT Students.* 
        FROM Students, Student_courses, Courses
        WHERE Students.id = Student_courses.student_id
        AND Student_courses.course_id = Courses.id
        AND Courses.name = 'python'
    ''')
    python_students = cursor.fetchall()
    for student in python_students:
        print(student)  
    print()
    

    print("3. Студенты на курсе Python из Spb:")
    cursor.execute('''
        SELECT Students.* 
        FROM Students, Student_courses, Courses
        WHERE Students.id = Student_courses.student_id
        AND Student_courses.course_id = Courses.id
        AND Courses.name = 'python'
        AND Students.city = 'Spb'
    ''')
    python_spb_students = cursor.fetchall()
    for student in python_spb_students:
        print(student)

    conn.commit()
    cursor.close()

except sqlite3.Error as error:
    print(f"Ошибка при создании базы данных: {error}")

finally:
    conn.close()
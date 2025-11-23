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
    print("Таблица создана!")
    conn.commit()
    cursor.close()

except sqlite3.Error as error:
    print(f"Ошибка при создании базы данных: {error}")

finally:
    conn.close()
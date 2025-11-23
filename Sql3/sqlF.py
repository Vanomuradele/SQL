import sqlite3
import os

class UniversityDB:
    def __init__(self, db_path='university.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Подключение к базе данных"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as error:
            print(f"Ошибка подключения к БД: {error}")
            return False
    
    def disconnect(self):
        """Закрытие соединения с БД"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def execute_query(self, query, params=None):
        """Выполнения SQL-запросов"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                return True
                
        except sqlite3.Error as error:
            print(f"Ошибка выполнения запроса: {error}")
            return False
    
    def is_database_initialized(self):
        """Проверка, была ли уже создана и заполнена БД"""
        try:
            # Проверяем существование всех таблиц
            tables_query = """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('Students', 'Courses', 'Student_courses')
            """
            tables = self.execute_query(tables_query)
            
            if len(tables) != 3:
                return False
            
            # Проверяем, есть ли данные в таблицах
            students_count = self.execute_query("SELECT COUNT(*) FROM Students")[0][0]
            courses_count = self.execute_query("SELECT COUNT(*) FROM Courses")[0][0]
            
            return students_count > 0 and courses_count > 0
            
        except:
            return False
    
    def create_tables(self):
        """Создание таблиц если они не существуют"""
        tables_queries = [
            '''
            CREATE TABLE IF NOT EXISTS Students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                age INTEGER,
                city TEXT
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS Courses (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                time_start TEXT,
                time_end TEXT
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS Student_courses (
                student_id INTEGER,
                course_id INTEGER,
                PRIMARY KEY (student_id, course_id),
                FOREIGN KEY (student_id) REFERENCES Students(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES Courses(id) ON DELETE CASCADE
            )
            '''
        ]
        
        for query in tables_queries:
            if not self.execute_query(query):
                return False
        return True
    
    def insert_initial_data(self):
        """Добавление начальных данных"""

        courses_data = [
            (1, 'python', '21.07.21', '21.08.21'),
            (2, 'java', '13.07.21', '16.08.21')
        ]
        
        students_data = [
            (1, 'Max', 'Brooks', 24, 'Spb'),
            (2, 'John', 'Stones', 15, 'Spb'),
            (3, 'Andy', 'Wings', 45, 'Manhester'),
            (4, 'Kate', 'Brooks', 34, 'Spb')
        ]
        
        student_courses_data = [
            (1, 1), (2, 1), (3, 1), (4, 2)
        ]
        
        try:
            self.cursor.executemany(
                "INSERT OR REPLACE INTO Courses VALUES (?, ?, ?, ?)", 
                courses_data
            )
            self.cursor.executemany(
                "INSERT OR REPLACE INTO Students VALUES (?, ?, ?, ?, ?)", 
                students_data
            )
            self.cursor.executemany(
                "INSERT OR REPLACE INTO Student_courses VALUES (?, ?)", 
                student_courses_data
            )
            
            self.conn.commit()
            return True
            
        except sqlite3.Error as error:
            print(f"Ошибка при добавлении данных: {error}")
            return False
    
    def initialize_database(self):
        """Создание таблиц и заполнение данными"""
        if not self.connect():
            return False
        
        try:
            if self.is_database_initialized():
                print("База данных уже есть!")
                return True
            
            if not self.create_tables():
                print("Ошибка при создании таблиц!")
                return False
            
            if not self.insert_initial_data():
                print("Ошибка при добавлении данных!")
                return False
            
            print("База данных успешно создана!")
            return True
            
        finally:
            self.disconnect()
    
    def display_all_data(self):
        """Отображение всех данных для проверки"""
        if not self.connect():
            return
        
        try:
            print("ВСЕ ДАННЫЕ В БАЗЕ:")
            
            print("\nСТУДЕНТЫ:")
            students = self.execute_query("SELECT * FROM Students")
            for student in students:
                print(student)
            
            print("\nКУРСЫ:")
            courses = self.execute_query("SELECT * FROM Courses")
            for course in courses:
                print(course)
             
        finally:
            self.disconnect()



db = UniversityDB()
    
db.initialize_database()
    
db.display_all_data()
   
print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ execute_query:")

db.connect()
result = db.execute_query("SELECT name, age FROM Students WHERE age > 20")
print("Студенты старше 20 лет:", result)

db.execute_query(
    "INSERT OR IGNORE INTO Students VALUES (?, ?, ?, ?, ?)", 
    (5, 'Anna', 'Smith', 28, 'Moscow')
)
    
result = db.execute_query("SELECT * FROM Students WHERE city = 'Moscow'")
print("Студенты из Москвы:", result)
    
db.disconnect()
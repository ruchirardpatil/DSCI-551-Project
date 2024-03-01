import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def execute_sql(conn, sql, params=None):
    """Execute an SQL statement and return the number of affected rows."""
    try:
        c = conn.cursor()
        if params:
            c.execute(sql, params)
        else:
            c.execute(sql)
        conn.commit()
        return c.rowcount  # Return the number of affected rows
    except Error as e:
        print(e)
        return None  # Indicate an error occurred during execution

def setup_database(conn):
    """Set up the database tables."""
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL CHECK (role IN ('Student', 'Instructor')) -- 'student' or 'instructor'
    );
    """
    sql_create_courses_table = """
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        start_date TEXT,
        end_date TEXT,
        capacity INTEGER NOT NULL,
        instructor_id INTEGER NOT NULL,
        FOREIGN KEY (instructor_id) REFERENCES users (id)
    );
    """
    sql_create_enrollments_table = """
    CREATE TABLE IF NOT EXISTS enrollments (
        id INTEGER PRIMARY KEY,
        course_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        FOREIGN KEY (course_id) REFERENCES courses (id),
        FOREIGN KEY (student_id) REFERENCES users (id)
    );
    """
    sql_create_materials_table = """
    CREATE TABLE IF NOT EXISTS materials (
        id INTEGER PRIMARY KEY,
        course_id INTEGER NOT NULL,
        material_type TEXT NOT NULL, -- 'syllabus', 'lecture_note', 'assignment', etc.
        content TEXT NOT NULL,
        FOREIGN KEY (course_id) REFERENCES courses (id)
    );
    """
    sql_create_grades_table = """
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY,
        enrollment_id INTEGER NOT NULL,
        grade TEXT NOT NULL,
        FOREIGN KEY (enrollment_id) REFERENCES enrollments (id)
    );
    """
    # Execute the SQL statements to create tables
    execute_sql(conn, sql_create_users_table)
    execute_sql(conn, sql_create_courses_table)
    execute_sql(conn, sql_create_enrollments_table)
    execute_sql(conn, sql_create_materials_table)
    execute_sql(conn, sql_create_grades_table)


def insert_user(conn, user_data):
    """Insert a new user."""
    sql = ''' INSERT INTO users(name, role)
              VALUES(?, ?) '''
    execute_sql(conn, sql, user_data)

def insert_course(conn, course_data):
    """Insert a new course."""
    sql = ''' INSERT INTO courses(title, description, start_date, end_date, capacity, instructor_id)
              VALUES(?,?,?,?,?,?) '''
    execute_sql(conn, sql, course_data)

def insert_enrollment(conn, enrollment_data):
    """Insert a new enrollment."""
    sql = ''' INSERT INTO enrollments(course_id, student_id)
              VALUES(?,?) '''
    execute_sql(conn, sql, enrollment_data)

def insert_material(conn, material_data):
    """Insert new course material."""
    sql = ''' INSERT INTO materials(course_id, material_type, content)
              VALUES(?,?,?) '''
    execute_sql(conn, sql, material_data)

def insert_grade(conn, grade_data):
    """Insert a new grade."""
    sql = ''' INSERT INTO grades(enrollment_id, grade)
              VALUES(?,?) '''
    execute_sql(conn, sql, grade_data)

def update_user(conn, user_data):
    """Update a user's details and return the number of affected rows."""
    sql = '''UPDATE users SET name = ?, role = ? WHERE id = ?'''
    c = conn.cursor()
    c.execute(sql, user_data)
    conn.commit()
    return c.rowcount

def update_course(conn, course_data):
    """Update course details directly."""
    sql = '''UPDATE courses
             SET title = ?, description = ?, start_date = ?, end_date = ?, capacity = ?, instructor_id = ?
             WHERE id = ?'''
    c = conn.cursor()
    c.execute(sql, course_data)
    conn.commit()
    return c.rowcount

def update_grade(conn, grade_data):
    """Update a student's grade directly."""
    sql = '''UPDATE grades
             SET grade = ?
             WHERE id = ?'''
    c = conn.cursor()
    c.execute(sql, grade_data)
    conn.commit()
    return c.rowcount

def delete_user(conn, user_id):
    """Delete a user."""
    sql = 'DELETE FROM users WHERE id = ?'
    c = conn.cursor()
    c.execute(sql, (user_id,))
    conn.commit()
    return c.rowcount 

def delete_course(conn, course_id):
    """Delete a course directly."""
    sql = 'DELETE FROM courses WHERE id = ?'
    c = conn.cursor()
    c.execute(sql, (course_id,))
    conn.commit()
    return c.rowcount

def delete_enrollment(conn, enrollment_id):
    """Delete an enrollment record directly."""
    sql = 'DELETE FROM enrollments WHERE id = ?'
    c = conn.cursor()
    c.execute(sql, (enrollment_id,))
    conn.commit()
    return c.rowcount

def delete_material(conn, material_id):
    """Delete course material directly."""
    sql = 'DELETE FROM materials WHERE id = ?'
    c = conn.cursor()
    c.execute(sql, (material_id,))
    conn.commit()
    return c.rowcount

def delete_grade(conn, grade_id):
    """Delete a grade directly."""
    sql = 'DELETE FROM grades WHERE id = ?'
    c = conn.cursor()
    c.execute(sql, (grade_id,))
    conn.commit()
    return c.rowcount

def query_db(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Example usage
database = "./course_management.db"
conn = create_connection(database)

if conn is not None:
    setup_database(conn)

else:
    print("Error! cannot create the database connection.")

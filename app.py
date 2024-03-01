# app.py (Flask Application)
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database_setup import create_connection, execute_sql, insert_user, insert_course, insert_enrollment, insert_material, insert_grade, update_user, update_course, update_grade, delete_user, delete_course, delete_enrollment, delete_material, delete_grade

app = Flask(__name__)
CORS(app)

def response_error(message, status_code=400):
    return jsonify({'error': message}), status_code

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test', methods=['GET'])
def test_route():
    return jsonify({'message': 'Test route accessible'}), 200

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if not all(k in data for k in ("name", "role")):
        return response_error("Missing data for user", 422)
    try:
        conn = create_connection('course_management.db')
        insert_user(conn, (data['name'], data['role']))
        conn.close()
        return jsonify({'message': 'User added successfully'}), 201
    except Exception as e:
        return response_error(str(e))

@app.route('/courses', methods=['POST'])
def add_course():
    data = request.json
    required_fields = ["title", "description", "start_date", "end_date", "capacity", "instructor_id"]
    if not all(k in data for k in required_fields):
        return response_error("Missing data for course", 422)
    try:
        conn = create_connection('course_management.db')
        insert_course(conn, (data['title'], data['description'], data['start_date'], data['end_date'], data['capacity'], data['instructor_id']))
        conn.close()
        return jsonify({'message': 'Course added successfully'}), 201
    except Exception as e:
        return response_error(str(e))

@app.route('/enrollments', methods=['POST'])
def add_enrollment():
    data = request.json
    try:
        conn = create_connection('course_management.db')
        insert_enrollment(conn, (data['course_id'], data['student_id']))
        conn.close()
        return jsonify({'message': 'Enrollment added successfully'}), 201
    except Exception as e:
        return response_error(str(e))

@app.route('/materials', methods=['POST'])
def add_material():
    data = request.json
    if not all(k in data for k in ["course_id", "material_type", "content"]):
        return response_error("Missing data for material", 422)
    try:
        conn = create_connection('course_management.db')
        insert_material(conn, (data['course_id'], data['material_type'], data['content']))
        conn.close()
        return jsonify({'message': 'Material added successfully'}), 201
    except Exception as e:
        return response_error(str(e))

@app.route('/grades', methods=['POST'])
def add_grade():
    data = request.json
    if not all(k in data for k in ["enrollment_id", "grade"]):
        return response_error("Missing data for grade", 422)
    try:
        conn = create_connection('course_management.db')
        insert_grade(conn, (data['enrollment_id'], data['grade']))
        conn.close()
        return jsonify({'message': 'Grade added successfully'}), 201
    except Exception as e:
        return response_error(str(e))

# Add similar endpoints for inserting into other tables...

@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    data = request.json
    print(data)
    if not all(key in data for key in ['name', 'role']):
        return response_error("Missing name or role in data", 422)
    try:
        conn = create_connection('course_management.db')
        affected_rows = update_user(conn, (data['name'], data['role'], user_id))
        print(affected_rows)
        conn.close()
        if affected_rows == 0 or affected_rows == None:
            return response_error("No user found with given ID to update", 404)
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return response_error(str(e))


# Update Course
@app.route('/update_course/<int:course_id>', methods=['PUT'])
def update_course_route(course_id):
    data = request.json
    if not all(k in data for k in ["title", "description", "start_date", "end_date", "capacity", "instructor_id"]):
        return response_error("Missing data for course", 422)
    try:
        conn = create_connection('course_management.db')
        affected_rows = update_course(conn, (data['title'], data['description'], data['start_date'], data['end_date'], data['capacity'], data['instructor_id'], course_id))
        conn.close()
        if affected_rows == 0 or affected_rows is None:
            return response_error("No course found with given ID to update", 404)
        return jsonify({'message': 'Course updated successfully'}), 200
    except Exception as e:
        return response_error(str(e))

# Update Grade
@app.route('/update_grade/<int:grade_id>', methods=['PUT'])
def update_grade_route(grade_id):
    data = request.json
    if "grade" not in data:
        return response_error("Missing grade data", 422)
    try:
        conn = create_connection('course_management.db')
        affected_rows = update_grade(conn, (data['grade'], grade_id))
        conn.close()
        if affected_rows == 0 or affected_rows is None:
            return response_error("No grade found with given ID to update", 404)
        return jsonify({'message': 'Grade updated successfully'}), 200
    except Exception as e:
        return response_error(str(e))


# Add similar endpoints for updating other tables...

@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    try:
        conn = create_connection('course_management.db')
        affected_rows = delete_user(conn, user_id)
        conn.close()
        if affected_rows == 0 or affected_rows == None:
            return response_error("No user found with given ID to delete", 404)
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return response_error(str(e))


@app.route('/delete_course/<int:course_id>', methods=['DELETE'])
def delete_course_route(course_id):
    try:
        conn = create_connection('course_management.db')
        affected_rows = delete_course(conn, course_id)
        conn.close()
        if affected_rows == 0 or affected_rows is None:
            return response_error("No course found with given ID to delete", 404)
        return jsonify({'message': 'Course deleted successfully'}), 200
    except Exception as e:
        return response_error(str(e))

# Delete Enrollment
@app.route('/delete_enrollment/<int:enrollment_id>', methods=['DELETE'])
def delete_enrollment_route(enrollment_id):
    try:
        conn = create_connection('course_management.db')
        affected_rows = delete_enrollment(conn, enrollment_id)
        conn.close()
        if affected_rows == 0 or affected_rows is None:
            return response_error("No enrollment found with given ID to delete", 404)
        return jsonify({'message': 'Enrollment deleted successfully'}), 200
    except Exception as e:
        return response_error(str(e))

# Delete Material
@app.route('/delete_material/<int:material_id>', methods=['DELETE'])
def delete_material_route(material_id):
    try:
        conn = create_connection('course_management.db')
        affected_rows = delete_material(conn, material_id)
        conn.close()
        if affected_rows == 0 or affected_rows is None:
            return response_error("No material found with given ID to delete", 404)
        return jsonify({'message': 'Material deleted successfully'}), 200
    except Exception as e:
        return response_error(str(e))

# Delete Grade
@app.route('/delete_grade/<int:grade_id>', methods=['DELETE'])
def delete_grade_route(grade_id):
    try:
        conn = create_connection('course_management.db')
        affected_rows = delete_grade(conn, grade_id)
        conn.close()
        if affected_rows == 0 or affected_rows is None:
            return response_error("No grade found with given ID to delete", 404)
        return jsonify({'message': 'Grade deleted successfully'}), 200
    except Exception as e:
        return response_error(str(e))

# Add similar endpoints for deleting from other tables...

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request
import mysql.connector

# Initialize the Flask app
app = Flask(__name__)

# Database connection configuration
db_config = {
    'user': 'root',
    'password': 'vivEK@789',
    'host': 'localhost',
    'database': 'school'
}

# Function to get a database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Endpoint to get all students
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(students)

# Endpoint to get a student by ID
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

# Endpoint to add a new student
@app.route('/students', methods=['POST'])
def add_student():
    new_student = request.json
    name = new_student.get('name')
    age = new_student.get('age')
    grade = new_student.get('grade')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)",
                   (name, age, grade))
    conn.commit()
    new_student_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({"id": new_student_id, "name": name, "age": age, "grade": grade}), 201

# Endpoint to update a student's details
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    updated_student = request.json
    name = updated_student.get('name')
    age = updated_student.get('age')
    grade = updated_student.get('grade')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students SET name = %s, age = %s, grade = %s WHERE id = %s
    """, (name, age, grade, student_id))
    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404
    
    return jsonify({"id": student_id, "name": name, "age": age, "grade": grade})

# Endpoint to delete a student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted"})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

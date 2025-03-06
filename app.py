from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Needed for form security

db = SQLAlchemy(app)


# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(100), nullable=False)
    gpa = db.Column(db.Float, nullable=False)
    enrollment_date = db.Column(db.String(20), nullable=False)


# Home route (Display all students)
@app.route('/')
def index():
    students = Student.query.all()
    courses = db.session.query(Student.course).distinct().all()
    courses = [c[0] for c in courses]
    return render_template('index.html', students=students, courses=courses)


# Search and Filter route
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    course_filter = request.args.get('course', 'All')
    gpa_min = request.args.get('gpa_min', type=float)
    gpa_max = request.args.get('gpa_max', type=float)

    students = Student.query

    if query:
        students = students.filter(Student.name.contains(query) | Student.course.contains(query))

    if course_filter and course_filter != "All":
        students = students.filter(Student.course == course_filter)

    if gpa_min is not None:
        students = students.filter(Student.gpa >= gpa_min)

    if gpa_max is not None:
        students = students.filter(Student.gpa <= gpa_max)

    students = students.all()
    courses = db.session.query(Student.course).distinct().all()
    courses = [c[0] for c in courses]

    return render_template('index.html', students=students, courses=courses)


# Route to add a new student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        gpa = request.form['gpa']
        enrollment_date = request.form['enrollment_date']

        new_student = Student(name=name, age=age, course=course, gpa=gpa, enrollment_date=enrollment_date)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_student.html')


# Route to edit a student
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        student.course = request.form['course']
        student.gpa = request.form['gpa']
        student.enrollment_date = request.form['enrollment_date']

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student)


# Route to delete a student
@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)

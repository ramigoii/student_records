from app import app, db, Student

# Create an application context
with app.app_context():
    # Add sample students
    sample_students = [
        Student(name="Alice Johnson", age=20, course="Computer Science", gpa=3.8, enrollment_date="2024-02-01"),
        Student(name="Bob Smith", age=22, course="Mathematics", gpa=3.5, enrollment_date="2023-09-15"),
        Student(name="Charlie Brown", age=21, course="Physics", gpa=3.9, enrollment_date="2024-01-10"),
        Student(name="Diana Prince", age=23, course="Engineering", gpa=3.7, enrollment_date="2023-08-20"),
        Student(name="Ethan Hunt", age=24, course="Business", gpa=3.6, enrollment_date="2022-07-11"),
    ]

    db.session.add_all(sample_students)
    db.session.commit()
    print("✅ Sample students added successfully!")

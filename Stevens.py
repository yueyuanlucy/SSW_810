import sqlite3
from flask import Flask, render_template

app=Flask(__name__)

@app.route('/instructors')
def courses_and_number():
    dbpath = "810_startup.db"

    try:
        db=sqlite3.connect(dbpath)
    except sqlite3.OperationalError:
        return f"Error: Unable to open database at {dbpath}"
    else:
        query='''select i.CWID, i.Name, i.Dept, g.Course, count(g.StudentCWID) as Students
                from instructors i join grades g
                on i.CWID=g.InstructorCWID
                group by i.CWID, i.Name, i.Dept, g.Course'''

        data=[{'cwid': cwid, 'name': name, 'dept': dept, 'course': course, 'student': student}
                for cwid, name, dept, course, student in db.execute(query)]

        db.close()

        return render_template('courses_and_student_counts.html',
                title="Stevens Repository",
                table_title="Courses and student counts",
                courses=data)

app.run(debug=True)
from flask import render_template, url_for, flash, redirect
from flaskDemo import app, db
from flaskDemo.forms import RegistrationForm, LoginForm
from flaskDemo.models import Student, Faculty, Qualified, Course, Section,Registration




@app.route("/")
@app.route("/home")

def home():
    courses=Course.query.all()
    students = Student.query.all()
    faculty = Faculty.query.all()
    return render_template('courses-students.html', coursesOut=courses,studentsOut=students, facultyOut=faculty)



@app.route("/join")
def join():

    results = Faculty.query.join(Qualified,Faculty.facultyID == Qualified.facultyID) \
              .add_columns(Faculty.facultyID, Faculty.facultyName, Qualified.Datequalified, Qualified.courseID)
#    results = db.session.query(Faculty,Qualified).filter(Faculty.facultyID == Qualified.facultyID)
    results2 = Faculty.query.join(Qualified,Faculty.facultyID == Qualified.facultyID) \
               .add_columns(Faculty.facultyID, Faculty.facultyName, Qualified.Datequalified, Qualified.courseID) \
               .join(Course, Course.courseID == Qualified.courseID).add_columns(Course.courseName)
    return render_template('join.html', title='Join',joined_1_n=results, joined_m_n=results2)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

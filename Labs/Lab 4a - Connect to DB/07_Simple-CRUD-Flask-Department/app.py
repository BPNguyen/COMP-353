from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_PORT'] = int(db['mysql_port'])
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        deptDetails = request.form
        dname = deptDetails['dname']
        dnumber = deptDetails['dnumber']
        mgr_ssn=deptDetails['mgr_ssn']
        mgr_start = deptDetails['mgr_start']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO department(dname, dnumber, mgr_ssn, mgr_start) VALUES(%s, %s, %s, %s)",(dname, dnumber,mgr_ssn, mgr_start))
        mysql.connection.commit()
        cur.close()
        return redirect('/departments')
    return render_template('index.html')

@app.route('/departments')
def departments():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM department")
    if resultValue > 0:
        deptDetails = cur.fetchall()
        return render_template('departments.html',data=deptDetails)

if __name__ == '__main__':
    app.run(debug=True)

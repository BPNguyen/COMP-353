from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)


# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
# app.config['MYSQL_PORT'] = 8889
app.config['MYSQL_PORT'] = int(db['mysql_port'])
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        user = userDetails['name']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        #db1=mysql.connect('localhost','cfn','naiman','company')
        #cur=db1.cursor()
        cur.execute("INSERT INTO user (username, email) VALUES(%s, %s)",(user, email))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM user")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users-dict.html',userDetails=userDetails)
    
if __name__ == '__main__':
    app.run(debug=True)



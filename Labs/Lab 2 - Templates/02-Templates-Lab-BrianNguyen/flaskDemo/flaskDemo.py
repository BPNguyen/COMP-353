from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        'author': 'Channah Naiman',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Peter Dordal',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Hey', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/lab")
def lab():
    favSnacks = ['Apple pie', 'Cookies', 'Cinnamon rolls']
    return render_template('lab.html', title='Brian Nguyen', posts=favSnacks)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://453RemoteUser:student453@45.55.59.121/COMP453Remote'


db = SQLAlchemy(app)

from flaskDemo import routes
# from flaskDemo import models

# models.db.create_all()

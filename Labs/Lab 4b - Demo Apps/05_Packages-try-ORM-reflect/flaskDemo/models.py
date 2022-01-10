from datetime import datetime
from flaskDemo import db


db.Model.metadata.reflect(db.engine)


class Course(db.Model):
    __table__ = db.Model.metadata.tables['course']
#class Course(db.Model):
#    __tablename__ = 'course'
 #   courseID = db.Column(db.String(8), primary_key=True)
 #   courseName=db.Column(db.String(15))
                         
class Student(db.Model):
    __table__ = db.Model.metadata.tables['student']
    
    
class Faculty(db.Model):
    __table__ = db.Model.metadata.tables['faculty']
    
class Qualified(db.Model):
    __table__ = db.Model.metadata.tables['qualified']
class Registration(db.Model):
    __table__ = db.Model.metadata.tables['registration']
class Section(db.Model):
    __table__ = db.Model.metadata.tables['section']

  

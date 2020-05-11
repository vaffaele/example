import os
from sqlalchemy import Column, String, Integer, create_engine, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import json

database_name = "agency"
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()
migrate = Migrate()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all()

'''
Actors
'''
class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  first_name = Column(String)
  last_name = Column(String)
  age = Column(Integer)
  gender = Column(String)
  image_link = Column(String)
  

  def __init__(self, first_name, last_name, age, gender,image_link):
    self.first_name = first_name
    self.last_name = last_name
    self.age = age
    self.gender = gender
    self.image_link = image_link

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'age': self.age,
      'gender': self.gender,
      'image_link':self.image_link
    }

'''
Movies

'''
class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(String)
  image_link = Column(String)

  def __init__(self, title, release_date,image_link):
    self.title = title
    self.release_date = release_date
    self.image_link = image_link

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date,
      'image_link':self.image_link
    }

import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   username = db.Column(db.String(80), unique=True, nullable=False)
#   email = db.Column(db.String(120), unique=True, nullable=False)

#   def __repr__(self):
#     return '<User {}>'.format(self.username)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.Text, nullable=False)
  done = db.Column(db.Boolean, nullable=False, default=False)
  add_date = db.Column(db.DateTime, nullable=False,
      default=datetime.datetime.utcnow)

  # user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
  #     nullable=False)
  # user = db.relationship('User',
  #     backref=db.backref('todos', lazy=True))

  def __repr__(self):
      return '<Todo {} ({})>'.format(self.text, self.done)

  @property
  def serialized(self):
   return {
     'id': self.id,
     'text': self.text,
     'done': self.done
   }

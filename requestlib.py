import datetime
import json
import uuid

from flask import request, Response

class RequestLib:
  def __init__(self, client, db_name):
    self.client = None
    self.db = None
    self.todos = []

  def get_todos(self, todo_id):
    now = datetime.datetime.utcnow()
    if todo_id is None:
      data = self.todos
    else:
      data = next(x for x in self.todos if x['id'] == todo_id)
    return Response(
      json.dumps({
        'data': data,
        'ts': str(now),
      }),
      status=200,
      mimetype='application/json'
    )

  def add_todo(self, todo_text):
    now = datetime.datetime.utcnow()
    todo = {
      'text': todo_text,
      'done': False,
      'id': str(uuid.uuid4()),
    }
    self.todos.append(todo)
    return Response(
      json.dumps({
        'data': todo,
        'ts': str(now),
      }),
      status=200,
      mimetype='application/json'
    )

  def change_done(self, todo_id):
    now = datetime.datetime.utcnow()
    todo = next(x for x in self.todos if x['id'] == todo_id)
    todo['done'] = not todo['done']
    return Response(
      json.dumps({
        'ts': str(now),
      }),
      status=200,
      mimetype='application/json'
    )

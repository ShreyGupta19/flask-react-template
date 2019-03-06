import argparse
import datetime
import hashlib
import json
import secrets

from models import *

from flask import Flask, Response, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user

app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  else:
    creds = request.get_json()
    user = User.query.filter_by(username=creds['email']).first()
    if user is None:
      salt = secrets.token_bytes(app.config['SALT_SIZE'])
    else:
      salt = user.pass_salt
    hasher = hashlib.sha256()
    hasher.update(creds['pass'].encode())
    hasher.update(salt)
    pass_hash = hasher.digest()
    if user is None:
      user = User(username=creds['email'],
                    pass_hash = pass_hash,
                    pass_salt = salt)
      db.session.add(user)
      db.session.commit()
    elif user.pass_hash != pass_hash:
      return Response(
        json.dumps({
          'ts': str(datetime.datetime.utcnow()),
        }),
        status=401,
        mimetype='application/json'
      )

    login_user(user)
    return Response(
        json.dumps({
          'ts': str(datetime.datetime.utcnow()),
          'location': url_for('index'),
        }),
        status=200,
        mimetype='application/json'
      )

@app.route('/', methods=['GET'])
@login_required
def index():
  return render_template('index.html')

@app.route('/todos', methods=['GET', 'POST'])
@login_required
def todos():
  if request.method == 'GET':
    todo_id = request.args.get('id', None)
    if todo_id is None:
      data = Todo.query.filter_by(user_id=current_user.id)
    else:
      data = [Todo.query.filter_by(id=todo_id, 
                                     user_id=current_user.id).first()]
    return Response(
      json.dumps({
        'data': [t.serialized for t in data],
        'ts': str(datetime.datetime.utcnow()),
      }),
      status=200,
      mimetype='application/json'
    )
  else:
    t = Todo(text=request.get_json()['todo'], user_id=current_user.id)
    db.session.add(t)
    db.session.commit()
    return Response(
      json.dumps({
        'data': t.serialized,
        'ts': str(datetime.datetime.utcnow()),
      }),
      status=200,
      mimetype='application/json'
    )

@app.route('/todos/done', methods=['POST'])
@login_required
def todos_done():
  todo_id = request.get_json()['id']
  t = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
  if t is None:
    return Response(
      json.dumps({
        'ts': str(datetime.datetime.utcnow()),
      }),
      status=401,
      mimetype='application/json'
    )
  t.done = not t.done
  db.session.add(t)
  db.session.commit()
  return Response(
    json.dumps({
      'data': t.serialized,
      'ts': str(datetime.datetime.utcnow()),
    }),
    status=200,
    mimetype='application/json'
  )


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description='Run a server for a Flask-React-MongoDB web application.')
  parser.add_argument('-d', '--deploy_mode', default='prod',
    choices=('prod', 'dev'), 
    help='Mode to deploy the server in (i.e. config to use).'
  )
  args = parser.parse_args()

  if args.deploy_mode == 'prod':
    app.config.from_object('config.ProductionConfig')
  else:
    app.config.from_object('config.DevelopmentConfig')

  app.static_folder = app.config['FLASK_STATIC_DIR']
  app.template_folder = app.config['FLASK_TEMPLATES_DIR']

  db_url = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(
    user=app.config['DB_USER'],
    pw=app.config['DB_PASSWORD'],
    host=app.config['DB_HOST'],
    port=app.config['DB_PORT'],
    db=app.config['DB_NAME']
  )
  app.config['SQLALCHEMY_DATABASE_URI'] = db_url
  with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()

  app.run()

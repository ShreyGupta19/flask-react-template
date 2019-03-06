import argparse
import datetime
import hashlib
import json
import secrets

import models as m
from settings.prod import settings as prod_settings
from settings.dev import settings as dev_settings

from flask import Flask, Response, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user

SALT_SIZE = 32

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description='Run a server for a Flask-React-MongoDB web application.')
  parser.add_argument('-d', '--deploy_mode', default='prod',
    choices=('prod', 'dev'), 
    help='Mode to deploy the server in (i.e. settings file to use).'
  )
  args = parser.parse_args()
  if args.deploy_mode == 'prod':
    settings = prod_settings
  elif args.deploy_mode == 'dev':
    settings = dev_settings
    # TODO: Add in FLASK_ENV=development env var

  app = Flask(__name__, static_folder=settings.FLASK_STATIC_DIR, 
              template_folder=settings.FLASK_TEMPLATES_DIR)
  db_url = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(
    user=settings.DB_USER,
    pw=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    db=settings.DB_NAME
  )
  app.config['SQLALCHEMY_DATABASE_URI'] = db_url
  app.config['SECRET_KEY'] = 'you-will-never-guess'
  with app.app_context():
    m.db.init_app(app)
    m.db.create_all()

  login_manager = LoginManager(app)
  login_manager.login_view = 'login'

  @login_manager.user_loader
  def load_user(user_id):
    return m.User.query.get(user_id)

  @app.route('/login', methods=['GET', 'POST'])
  def login():
    if request.method == 'GET':
      return render_template('login.html')
    else:
      creds = request.get_json()
      user = m.User.query.filter_by(username=creds['email']).first()
      if user is None:
        salt = secrets.token_bytes(SALT_SIZE)
      else:
        salt = user.pass_salt
      hasher = hashlib.sha256()
      hasher.update(creds['pass'].encode())
      hasher.update(salt)
      pass_hash = hasher.digest()
      if user is None:
        user = m.User(username=creds['email'],
                      pass_hash = pass_hash,
                      pass_salt = salt)
        m.db.session.add(user)
        m.db.session.commit()
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
        data = m.Todo.query.filter_by(user_id=current_user.id)
      else:
        data = [m.Todo.query.filter_by(id=todo_id, 
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
      t = m.Todo(text=request.get_json()['todo'], user_id=current_user.id)
      m.db.session.add(t)
      m.db.session.commit()
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
    t = m.Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    if t is None:
      return Response(
        json.dumps({
          'ts': str(datetime.datetime.utcnow()),
        }),
        status=401,
        mimetype='application/json'
      )
    t.done = not t.done
    m.db.session.add(t)
    m.db.session.commit()
    return Response(
      json.dumps({
        'data': t.serialized,
        'ts': str(datetime.datetime.utcnow()),
      }),
      status=200,
      mimetype='application/json'
    )
    

  app.run()

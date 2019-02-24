import argparse
import datetime
import json

import models as m
from settings.prod import settings as prod_settings
from settings.dev import settings as dev_settings

from flask import Flask, render_template, request, Response


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description='Run a server for a Flask-React-MongoDB web application.')
  parser.add_argument('-d', '--deploy_mode', default='prod',
    choices=('prod', 'dev'), 
    help='Mode to deploy the server in (i.e. settings file to use).'
  )
  args = parser.parse_args()
  if args.deploy_mode == "prod":
    settings = prod_settings
  elif args.deploy_mode == "dev":
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
  with app.app_context():
    m.db.init_app(app)
    m.db.create_all()

  @app.route("/", methods=['GET'])
  def index():
    return render_template("index.html")

  @app.route("/todos", methods=['GET', 'POST'])
  def todos():
    if request.method == 'GET':
      todo_id = request.args.get('id', None)
      if todo_id is None:
        data = m.Todo.query.all()
      else:
        data = [m.Todo.query.filter_by(id=todo_id).first()]
      return Response(
        json.dumps({
          'data': [t.serialized for t in data],
          'ts': str(datetime.datetime.utcnow()),
        }),
        status=200,
        mimetype='application/json'
      )
    else:
      t = m.Todo(text=request.get_json()['todo'])
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

  @app.route("/todos/done", methods=['POST'])
  def todos_done():
    todo_id = request.get_json()['id']
    t = m.Todo.query.filter_by(id=todo_id).first()
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

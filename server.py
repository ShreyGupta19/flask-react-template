import argparse

from settings.prod import settings as prod_settings
from settings.dev import settings as dev_settings
from requestlib import RequestLib

from flask import Flask, render_template, request


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
  reqlib = RequestLib(None, None)

  @app.route("/", methods=['GET'])
  def index():
    return render_template("index.html")

  @app.route("/todos", methods=['GET', 'POST'])
  def todos():
    if request.method == 'GET':
      todo_id = request.args.get('id', None)
      return reqlib.get_todos(todo_id)
    else:
      todo_data = request.get_json()['todo']
      return reqlib.add_todo(todo_data)

  @app.route("/todos/done", methods=['POST'])
  def todos_done():
    # import pdb
    print(request)
    # pdb.set_trace()
    todo_id = request.get_json()['id']
    return reqlib.change_done(todo_id)
    

  app.run()

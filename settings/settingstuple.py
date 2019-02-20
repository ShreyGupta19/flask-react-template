from collections import namedtuple

SettingsTuple = namedtuple('SettingsTuple', [
  'FLASK_STATIC_DIR',
  'FLASK_TEMPLATES_DIR',
  'DB_NAME',
  'DB_USER',
  'DB_PASSWORD',
  'DB_HOST',
  'DB_PORT',
  # TODO: Fill in the names of your deployment settings here.
])

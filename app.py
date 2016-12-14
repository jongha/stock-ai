#-*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
import modules.base as base
import numpy as np
from modules.decorators.minified_response import minified_response
import config
import sqlite3
import csv
import config

app = Flask(__name__)

# from flask.ext.sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')
# db = SQLAlchemy(app)

# class User(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(100))
#   email = db.Column(db.String(100))
#   def __init__(self, name, email):
#     self.name = name
#     self.email = email


@app.route('/', methods=['GET'])
@minified_response
def index(code=None):
  data = None
  return render_template('index.html', data=data)


@app.route('/evaluate.json', methods=['GET'])
def evaluate(code=None):
  # if request.method == 'POST':
  #   u = User(request.form['name'], request.form['email'])
  #   db.session.add(u)
  #   db.session.commit()
  # return redirect(url_for('index'))

  if code is None:
    code = request.args.get('code')
    if code is not None:
      return evaluate(code)

    else:
      return None

  else:
    data = None
    json = None

    if code:
      try:
        data, json, score = base.load(code)
      except:
        pass

      if data is None or json is None:
        import modules.loader as loader
        data, json = loader.load(code)
        score = loader.score(data, json)
        base.dump(code, (data, json, score))

  return jsonify(score)


@app.route('/code.json', methods=['GET'])
def get_code(name=None):
  result = []
  if name is None:
    name = request.args.get('name')

  if name is not None:
    connection = sqlite3.Connection(config.DATA_STOCKS_SQLITE)
    rows = connection.execute(
        'SELECT name, code FROM stocks WHERE name like ?',
        ('%' + name + '%', ))
    for row in rows:
      result.append({'name': row[0], 'code': row[1]})

  return jsonify(result)


def setup_database():
  try:
    os.remove(config.DATA_STOCKS_SQLITE)

  except:
    pass

  connection = None
  csv_file = None

  try:
    connection = sqlite3.Connection(config.DATA_STOCKS_SQLITE)
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE "stocks" ("name" varchar(50), "code" varchar(6), "category" varchar(50), "product" varchar(50), "date" varchar(10), "end" varchar(10), "ceo" varchar(20), "homepage" varchar(100), "location" varchar(30));'
    )
    cursor.execute('CREATE UNIQUE INDEX stocks_name ON stocks(name);')
    cursor.execute('CREATE UNIQUE INDEX stocks_code ON stocks(code);')

    csv_file = open(config.DATA_STOCKS_CSV)
    csv_reader = csv.reader(csv_file, delimiter=',')
    cursor.executemany('INSERT INTO stocks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       csv_reader)
    cursor.close()
    connection.commit()

  finally:
    if connection is not None:
      connection.close()
      connection = None

    if csv_file is not None:
      csv_file.close()
      csv_file = None


if __name__ == '__main__':
  import sys

  if len(sys.argv) <= 1:
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

  else:
    print('Argument List:', str(sys.argv))
    command = sys.argv[1]

    if command == 'analytics':
      analytics(sys.argv[2])

    elif command == 'database':
      setup_database()

#-*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
import modules.base as base
import numpy as np
from modules.decorators.minified_response import minified_response
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


@app.route('/analytics.json', methods=['GET'])
def analytics(code=None):
  # if request.method == 'POST':
  #   u = User(request.form['name'], request.form['email'])
  #   db.session.add(u)
  #   db.session.commit()
  # return redirect(url_for('index'))

  code = code or request.args.get('code')
  data = None

  if code:
    code = code or request.args.get('code')
    # data = base.download(code, 2016, 1, 1, 2016, 11, 1)
    data = base.load(code)

    if not config.PRODUCTION or data is None:
      import modules.loader as loader
      data = loader.load(code)
      base.dump(code, data)

      return jsonify(data['json'])

  return jsonify(data['json'])


if __name__ == '__main__':
  import sys

  if len(sys.argv) <= 1:
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

  else:
    print('Argument List:', str(sys.argv))

    if sys.argv[1] == 'test':
      analytics('005930')
      # analytics('001520')

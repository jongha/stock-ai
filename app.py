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

  if code is None:
    code = request.args.get('code')
    if code is not None:
      data = analytics(code)
      return jsonify(data)
    else:
      return None

  else:
    data = None
    if code:
      data = base.load(code)
      if not config.PRODUCTION or data is None:
        import modules.loader as loader
        data = loader.load(code)
        base.dump(code, data)
        return data

    return data


if __name__ == '__main__':
  import sys

  if len(sys.argv) <= 1:
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

  else:
    print('Argument List:', str(sys.argv))

    if sys.argv[1] == 'analytics':
      print(analytics('005930'))

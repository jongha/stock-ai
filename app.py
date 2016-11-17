import os
from flask import Flask, render_template, request, redirect, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import lib.base as base
import numpy as np
from lib.algorithm import grade, johntempleton

app = Flask(__name__)
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
def index(code=None):
  import lib.loader as loader

  code = code or request.args.get('code')
  # data = base.download(code, 2016, 1, 1, 2016, 11, 1)

  (price, simple, summary, raw) = loader.load(code)
  eps = simple['EPS'].mean()
  eps_ifrs = raw['EPS_IFRS'].dropna()[:5]

  result = {
    'price': price,
    'per_5': summary['PER_5'][0],
    'pbr_5': summary['PBR_5'][0],
    'roe_5': summary['ROE_5'][0],
    'bps_5_growth': summary['EPS_5_GROWTH'][0],
    'bps_5_growth': summary['BPS_5_GROWTH'][0],
    'grade': grade.evaluate(raw),
    'johntempleton': johntempleton.evaluate(eps, eps_ifrs),
  }

  print(result)

  # return render_template('index.html', data = { 'grade': table['grade'] })
  return result

  # if request.method == 'POST':
  #   u = User(request.form['name'], request.form['email'])
  #   db.session.add(u)
  #   db.session.commit()
  # return redirect(url_for('index'))

if __name__ == '__main__':
  import sys

  if len(sys.argv) <= 1:
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

  else:
    print('Argument List:', str(sys.argv))

    if sys.argv[1] == 'test':
      index('005930')
      # index('001520')


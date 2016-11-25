import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
import modules.base as base
import numpy as np
from modules.algorithm import grade, johntempleton
from modules.decorators.minified_response import minified_response

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
    import modules.loader as loader

    code = code or request.args.get('code')
    # data = base.download(code, 2016, 1, 1, 2016, 11, 1)
    (price, simple, summary, raw) = loader.load(code)
    eps = simple['EPS'].mean()
    eps_ifrs = raw['EPS_IFRS'].dropna()[:5]

    data = {
        'price': price,
        'per_5': summary['PER_5'][0],
        'pbr_5': summary['PBR_5'][0],
        'roe_5': summary['ROE_5'][0],
        'eps_5_growth': summary['EPS_5_GROWTH'][0],
        'bps_5_growth': summary['BPS_5_GROWTH'][0],
        'grade': grade.evaluate(raw),
        'johntempleton': johntempleton.evaluate(eps, eps_ifrs),
    }

  return jsonify(data)


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

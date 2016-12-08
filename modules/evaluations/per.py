#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.evaluations.evaluation import Evaluation


# 현 EPS 과거 5년 PER 평균을 곱한 값
class PER(Evaluation):
  def __init__(self, evaluation):
    data = evaluation.get_data()
    json = evaluation.get_json()

    Evaluation.__init__(self, data, json)
    self.set_json('PER', self.evaluate())

  def evaluate(self):
    json = self.get_json()
    return int(json['EPS'] * json['PER_5'])
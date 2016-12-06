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
    Evaluation.__init__(self, data)
    self.concat('EVALUATION_PER', self.evaluate())

  def evaluate(self):
    data = self.get_data()
    return int(data['EPS_SIMPLE'][0] * data['PER_5'][0])
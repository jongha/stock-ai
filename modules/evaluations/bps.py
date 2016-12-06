#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.evaluations.evaluation import Evaluation


# 현 BPS 과거 5년 PBR 평균값을 곱한 값
class BPS(Evaluation):
  def __init__(self, evaluation):
    data = evaluation.get_data()
    Evaluation.__init__(self, data)
    self.concat('EVALUATION_BPS', self.evaluate())

  def evaluate(self):
    data = self.get_data()
    return int(data['BPS'][0] * data['PBR_5'][0])


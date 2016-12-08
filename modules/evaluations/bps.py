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
    json = evaluation.get_json()

    Evaluation.__init__(self, data, json)
    self.set_json('BPS', self.evaluate())

  def evaluate(self):
    json = self.get_json()
    return int(json['BPS'] * json['PBR_5'])

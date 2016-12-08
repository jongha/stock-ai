#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.evaluations.evaluation import Evaluation


# 올슨 초과이익모형
class RIM(Evaluation):
  def __init__(self, evaluation):
    data = evaluation.get_data()
    json = evaluation.get_json()

    Evaluation.__init__(self, data, json)
    self.set_json('RIM', self.evaluate())

  def evaluate(self):
    json = self.get_json()
    value = json['BPS'] + (json['EPS'] - (json['BPS'] * 0.1)) * (
        1 - config.DATA_DISCOUNT_RATE)

    return int(value)

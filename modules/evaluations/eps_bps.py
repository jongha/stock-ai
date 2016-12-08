#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.evaluations.evaluation import Evaluation


# 5년후 BPS *BPS성장률 기업가치 할인
# 5년 EPS * EPS 성장률 년도별 할인된 흐름
# BPS(0.4)+EPS(0.6) = 기업가치
class EPS_BPS(Evaluation):
  def __init__(self, evaluation):
    data = evaluation.get_data()
    json = evaluation.get_json()

    Evaluation.__init__(self, data, json)
    self.set_json('EVALUATION_5_EPS_BPS', self.evaluate())

  def evaluate(self):
    data = self.get_data()
    json = self.get_json()

    bps = json['BPS']
    bps_5_growth = float(json['BPS_5_GROWTH'].replace('%', '')) / 100
    eps_5_growth = float(json['EPS_5_GROWTH'].replace('%', '')) / 100

    # BPS 미래 기업가치의 할인법
    bps_for_future = (bps * math.pow(1 + bps_5_growth, 5)) * math.pow(
        1 - config.DATA_DISCOUNT_RATE, 5)

    eps = data['EPS'].dropna()[:5]
    sum_of_product = 0
    for index in range(5):  # 0: latest ~
      sum_of_product += eps[index] * [0.4, 0.2, 0.2, 0.1, 0.1][index]

    # 5년 EPS 할인된 가치
    sum_of_5_year = 0

    # 영구가치
    value_of_fixed = 0

    for i in range(1, 6):
      value_year = sum_of_product * math.pow(1 + eps_5_growth, i) * (
          1 - config.DATA_DISCOUNT_RATE)
      sum_of_5_year += value_year

      if i == 5:
        value_of_fixed = value_year * config.DATA_FIXED_RATE

    # 할인된 가치
    value_of_discount = value_of_fixed / math.pow(
        1 + config.DATA_DISCOUNT_RATE, 5)

    # EPS 미래 기업가치 할인
    value_of_future = sum_of_5_year + value_of_discount

    # BPS 미래 기업가치의 할인법
    value = (bps_for_future * config.DATA_VALUE_OF_BPS) + (
        value_of_future * config.DATA_VALUE_OF_EPS)

    return value

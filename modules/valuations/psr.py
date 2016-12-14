#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.valuations.valuation import Valuation


# PSR이 1.5배가 넘으면 피하고 3배가 넘으면 매수해선 안된다고 봤다.
# 반면 PSR이 0.75배 이하인 기업은 적극적 매수
class PSR(Valuation):
  def __init__(self, valuation):
    data = valuation.get_data()
    json = valuation.get_json()

    Valuation.__init__(self, data, json)
    self.set_json('PSR', self.valuate())

  def valuate(self):
    try:
      data = self.get_data()
      json = self.get_json()

      bps = json['BPS']
      eps_5_growth = json['EPS_5_GROWTH']

      value = data['PRICE'].dropna()[:1][0] / (
          (data['SALES'].dropna()[:1][0] * 100000000) /
          (data['STOCK_COUNT'].dropna()[:1][0] * 1000))

      return float(value)
    except:
      return None
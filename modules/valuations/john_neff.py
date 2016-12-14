#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.valuations.valuation import Valuation


# 존네프- 상수값 4.0 이상
# (우리나라 평균PER 실정에 맞추게 되면 4.0이상)
# = ROE성장율(3~5년 평균)+배당수익율(3~5년평균) / PER
class JohnNeff(Valuation):
  def __init__(self, valuation):
    data = valuation.get_data()
    json = valuation.get_json()

    Valuation.__init__(self, data, json)
    self.set_json('JOHN_NEFF', self.valuate())

  def valuate(self):
    try:
      data = self.get_data()
      json = self.get_json()

      bps = json['BPS']
      eps_5_growth = json['EPS_5_GROWTH']

      value = ((json['ROE_5'] * 100) + data['DIVIDEND_RATE'].dropna()[:1][0]
               ) / json['PER']

      return float(value)
    except:
      return None
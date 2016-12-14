#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.valuations.valuation import Valuation


# 피터린치- 상수값 1.5 이상
# = EPS성장율(3~5년 평균)+배당수익율(3~5년평균) / PER
# 0.5 미만 투자우수
# 0.5~1 투자긍정
# 1이상 투자부적격
class PEG(Valuation):
  def __init__(self, valuation):
    data = valuation.get_data()
    json = valuation.get_json()

    Valuation.__init__(self, data, json)
    self.set_json('PEG', self.valuate())

  def valuate(self):
    data = self.get_data()
    json = self.get_json()

    bps = json['BPS']
    eps_5_growth = json['EPS_5_GROWTH']

    value = ((eps_5_growth * 100) + data['DIVIDEND_RATE'].dropna()[:1][0]
             ) / json['PER']

    return float(value)

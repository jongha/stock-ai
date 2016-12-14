#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.valuations.valuation import Valuation


# 매출채권회전율
# 매출채권 회전율이 높다는 것은 매출채권이 순조롭게 회수되고 있음을 나타내나, 반대로 이 회전율이 낮게 되면 매출채권의 회수기간이 길어지므로, 그에 따른 대손발생의 위험이 증가하고 수익감소의 원인이 된다
class RT(Valuation):
  def __init__(self, valuation):
    data = valuation.get_data()
    json = valuation.get_json()

    Valuation.__init__(self, data, json)
    self.set_json('RT', self.valuate())

  def valuate(self):
    try:
      data = self.get_data()
      json = self.get_json()

      value = data['SALES_AND_FLOATING_BOND'].dropna()[:1][0] / data[
          'SALES'].dropna()[:1][0]
      return value
    except:
      return None
#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.valuations.valuation import Valuation


# 부채비율
# 기업의 부채액은 적어도 자기자본액 이하인 것이 바람직하므로 부채비율은 100% 이하가 이상적이다
class DE(Valuation):
  def __init__(self, valuation):
    data = valuation.get_data()
    json = valuation.get_json()

    Valuation.__init__(self, data, json)
    self.set_json('DE', self.valuate())

  def valuate(self):
    try:
      data = self.get_data()
      json = self.get_json()

      value = data['DEBT_RATIO'].dropna()[:1][0]
      return value

    except:
      return None
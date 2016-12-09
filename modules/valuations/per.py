#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.valuations.valuation import Valuation


# 현 EPS 과거 5년 PER 평균을 곱한 값
class PER(Valuation):
  def __init__(self, valuation):
    data = valuation.get_data()
    json = valuation.get_json()

    Valuation.__init__(self, data, json)
    self.set_json('PER', self.valuate())

  def valuate(self):
    json = self.get_json()
    return int(json['EPS'] * json['PER_5'])
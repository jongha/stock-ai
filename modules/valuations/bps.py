#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.valuations.valuation import Valuation


# 현 BPS 과거 5년 PBR 평균값을 곱한 값
class BPS(Valuation):
  def __init__(self, valuation):
    data = valuation.get_data()
    json = valuation.get_json()

    Valuation.__init__(self, data, json)
    self.set_json('BPS', self.valuate())

  def valuate(self):
    try:
      json = self.get_json()
      return int(json['BPS'] * json['PBR_5'])
    except:
      return None
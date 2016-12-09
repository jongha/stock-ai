#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.valuations.valuation import Valuation


# 올슨 초과이익모형
class RIM(Valuation):
  def __init__(self, valuation):
    data = valuation.get_data()
    json = valuation.get_json()

    Valuation.__init__(self, data, json)
    self.set_json('RIM', self.valuate())

  def valuate(self):
    json = self.get_json()
    value = json['BPS'] + (json['EPS'] - (json['BPS'] * 0.1)) * (
        1 - config.DATA_DISCOUNT_RATE)

    return int(value)

#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.valuations.valuation import Valuation


# 브라운스톤 지표
# ROE / PER > 3 이상
class BrownStone(Valuation):
  def __init__(self, valuation):
    data = valuation.get_data()
    json = valuation.get_json()

    Valuation.__init__(self, data, json)
    self.set_json('BROWN_STONE', self.valuate())

  def valuate(self):
    data = self.get_data()
    json = self.get_json()

    value = (json['ROE'] * 100) / json['PER']
    return float(value)

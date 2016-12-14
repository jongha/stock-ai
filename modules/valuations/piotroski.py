#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.valuations.valuation import Valuation


# 9점 만점, 2점이하 부실
class Piotroski(Valuation):
  def __init__(self, valuation):
    data = valuation.get_data()
    json = valuation.get_json()

    Valuation.__init__(self, data, json)
    self.set_json('PIOTROSKI', self.valuate())

  def valuate(self):
    try:
      data = self.get_data()
      json = self.get_json()

      values = []

      # 순이익 > 0
      values.append(
          (1 if data['NET_PROFIT_DURING_A_YEAR'].dropna()[:1][0] > 0 else 0))

      # 영업현금흐름>0
      values.append((1 if data['TOTAL_CASH_FLOW'].dropna()[:1][0] > 0 else 0))

      # ROA 전년대비 증가
      roas = data['ROA'].dropna()[:2]
      values.append(1 if roas[0] > roas[1] else 0)

      # 영업현금흐름 > 순이익
      stocks = data['STOCK_COUNT'].dropna()[:2]
      values.append(
          (1 if
           (data['OPERATING_PROFIT_AFTER_TAX'].dropna()[:1][0] * 100000000) >
           (data['NET_PROFIT_DURING_A_YEAR'].dropna()[:1][0] * stocks[0]) else
           0))

      # 장기부채/자산 비율이 전년보다 감소 혹은 부채 없음
      debt_ratios = data['DEBT_RATIO'].dropna()[:2]
      values.append(1 if debt_ratios[1] > debt_ratios[0] or debt_ratios[0] == 0
                    else 0)

      # 유동비율
      current_ratios = data['CURRENT_RATIO'].dropna()[:2]
      values.append(1 if current_ratios[0] > current_ratios[1] else 0)

      # 잠재주식수 전년대비 감소 또는 변동없음
      values.append(1 if stocks[0] <= stocks[1] else 0)

      # 매출총이익률 전년대비 증가
      gross_profit_margins = data['GROSS_PROFIT_MARGIN'].dropna()[:2]
      values.append(1 if gross_profit_margins[1] < gross_profit_margins[0] else
                    0)

      # 매출증가율 > 자산증가율
      total_assets = data['TOTAL_ASSETS_AVERAGE'].dropna()[:2]
      values.append(1 if data['SALES_GROWTH_RATE'].dropna()[:1][0] > (((
          total_assets[0] - total_assets[1]) / total_assets[1]) * 100) else 0)

      return sum(values)

    except:
      return None

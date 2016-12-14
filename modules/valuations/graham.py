#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.valuations.valuation import Valuation


# 그레이엄 순수
# 순유동자산-순유동부채 값의 주가대비 60% 기준
# 하지만 현대사회 특성을 반영해 주가대비 20% 이상적용
class Graham(Valuation):
  def __init__(self, valuation):
    data = valuation.get_data()
    json = valuation.get_json()

    Valuation.__init__(self, data, json)
    self.set_json('GRAHAM', self.valuate())

  def valuate(self):
    try:
      data = self.get_data()
      json = self.get_json()

      bps = json['BPS']
      eps_5_growth = json['EPS_5_GROWTH']

      # 당좌자산
      # (유동금융자산+매출채권및기타유동채권+기타유동자산+현금및현금성자산+매각예정비유동자산및처분자산집단)*100000000
      quick_assets = (data['FLOATING_FINANCE_ASSETS'].dropna()[:1][0] +
                      data['SALES_AND_FLOATING_BOND'].dropna()[:1][0] +
                      data['ETC_FLOATING_ASSETS'].dropna()[:1][0] +
                      data['CACHE_ASSETS'].dropna()[:1][0] +
                      data['RESERVED_SALE_ASSETS'].dropna()[:1][0]) * 100000000

      # 재고자산
      # =재고자산*100000000
      inventory_assets = data['INVENTORY_ASSETS'].dropna()[:1][0] * 100000000

      # 매출채권
      # =매출채권및기타유동채권*100000000
      sales_bond = data['SALES_AND_FLOATING_BOND'].dropna()[:1][0] * 100000000

      # 유동부채
      # 유동부채*100000000
      floating_debt = data['FLOATING_DEBT'].dropna()[:1][0] * 100000000

      # 유통주식 수
      stock_count = data['STOCK_COUNT'].dropna()[:1][0] * 1000

      # 현재가
      price = data['PRICE'].dropna()[:1][0]

      value = (((quick_assets + inventory_assets + sales_bond) - floating_debt)
               / stock_count) / price

      return float(value)

    except:
      return None

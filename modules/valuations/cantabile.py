#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.valuations.valuation import Valuation

# 칸타빌레 기업가치
# http://cantabile.synology.me/58/?p=148
# 적정가 (full version) = (이익가치 * 6 + 자산가치 * 0.3 + 배당가치 * 5) * (1 + 기대성장률 * 3) * (1 – 고유 디스카운트 비율)
# 이익가치 = (과거 2년 ~ 미래 2년, 총 5년간 평균 순이익) / 유통주식수      (당해와 미래의 순이익은 기대성장률과 1회성 이익분을 반영하여 추정)
# 자산가치 = 최근 재무제표상의 자기자본 * 자본조정비율 / 유통주식수
# 배당가치 = 최근 회계년도 배당액      (혹은, 당해 예상 배당액)
# 기대성장률 = ROE * 성장률조정비율


# 적정가 (full version) = (이익가치 * 6 + 자산가치 * 0.3 + 배당가치 * 5) * (1 + 기대성장률 * 3) * (1 – 고유 디스카운트 비율)
# 적정가 (simplified version) = ((EPS * 6) + (BPS * 0.25) + (최근년도배당액 * 4)) * (1 + (ROE * 2))
class Cantabile(Valuation):
  def __init__(self, valuation):
    data = valuation.get_data()
    json = valuation.get_json()

    Valuation.__init__(self, data, json)
    self.set_json('CANTABILE', self.valuate())

  def valuate(self):
    data = self.get_data()
    json = self.get_json()

    dividend = float(data['DIVIDEND_PRICE'].dropna()[:1][0])

    # ROE
    roe = float(json['ROE'])

    # BPS
    bps = float(json['BPS'])

    # # EPS
    # eps = float(json['EPS'])

    # # 유통주식 수
    # stock_count = data['STOCK_COUNT'][0] * 1000

    # # 적정가 (simplified version)
    # simple_value = (
    #     (eps * 6) + (bps * 0.25) + (dividend * 4)) * (1 + (roe * 2))

    # 이익가치 = (과거 2년 ~ 미래 2년, 총 5년간 평균 순이익) / 유통주식수
    profit_value = 0

    profit_values = []
    eps_ifrs = data['EPS_IFRS'].dropna()[:3]

    for index in reversed(range(3)):  # 0: latest ~
      profit_values.append(eps_ifrs[index])

    eps1 = json['EPS'] * (1 + json['ROE_5'])
    eps2 = eps1 * (1 + json['ROE_5'])

    profit_values.append(eps1)
    profit_values.append(eps2)

    for index in range(5):  # 0: latest ~ ??
      profit_value += (profit_values[index] * [0.1, 0.2, 0.4, 0.2, 0.1][index])

    profit_value *= 6

    # 자산가치 = 최근 재무제표상의 자기자본 * 자본조정비율 / 유통주식수
    asset_value = bps * config.DATA_CAPITAL_RATIO_RATE

    # 기대성장률 = ROE * 성장률조정비율
    expect_growth_rate = roe * config.DATA_EXPECT_GROWTH_RATE

    full_value = (profit_value + asset_value + (dividend * 5)) * (
        1 + (expect_growth_rate * 3)) * (1 - config.DATA_DISCOUNT_RATE)

    return full_value

#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.evaluations.evaluation import Evaluation


# 현금흐름할인법
# -FCF 증가율 : 과거 증가율을 토대로 하되 평균보다 조금 보수적으로 설정 (평균증가율에서 10% 할인)
#                         1단계 예측에서 잉여현금흐름 성장율을 단계적으로 할인 적용
# -영구가치 증가율(g) 고려사항 -   GDP성장율(美 3%) 근거/쇠락업종은 2%정도
# -안전마진 -   모닝스타: Min20 Max60 (일반적 30~40%), 안정적인 사업모델 20, 사업리스크가 큰 순환기업 60
# -할인율 : Min 7% Max 13% 모닝스타의 평균 복합성할인률 10.5%
#                 할인율을 결정하는 요소 (기업규모, 재무레버리지, 경기순환성, 경영 기업지배구조, 경제적해자)
class DCF(Evaluation):
  def __init__(self, evaluation):
    data = evaluation.get_data()
    Evaluation.__init__(self, data)
    self.concat('EVALUATION_DCF', self.evaluate())

  def evaluate(self):
    data = self.get_data()

    # print(data['FCFF'].dropna()[:5].multiply({1,1,1,1,1}))
    fcff = data['FCFF'].dropna()[:5]
    fcff_count = len(fcff)
    dcf = None

    if fcff_count == 5:
      index = 0

      sum_of_product = 0
      for index in range(5): # 0: latest ~
        sum_of_product += fcff[index] * [0.3, 0.3, 0.3, 0.1, 0.1][index]

      percent_fcff = fcff[0] / fcff[-1]
      direction = 1 if percent_fcff >= 0 else -1
      fcff_growth = math.pow(abs(percent_fcff), 1 / (fcff_count - 1)) * direction

      # 1단계: 차후 10년간 FCF(잉여현금흐름) 예측
      fcff_year = [sum_of_product]
      for index in range(1, 10):
        fcff_year.append(fcff_year[index - 1] * fcff_growth)

      # 2단계: FCF를 현재가치로 할인 [현재가치=미래가치/(1+R)^N] : R=할인율. N=할인연수
      fcff_year_discount = []
      fcff_year_discount_sum = 0
      for index in range(10):
        value = fcff_year[index] / math.pow(1 + config.DATA_DISCOUNT_RATE, index + 1)
        fcff_year_discount.append(value)
        fcff_year_discount_sum += value

      # 3단계: 영구가치계산및 현재가치로 할인 [영구가치=10년뒤 FCF x (1+g)/(R-g)] : g=영구가치증가율
      fcff_10_year = fcff_year[len(fcff_year) - 1] * fcff_growth
      value_growth = (1 + config.DATA_CFN) / (config.DATA_DISCOUNT_RATE - config.DATA_CFN)
      value_growth_fixed = fcff_10_year * value_growth # 영구가치
      fcff_discount_rate = value_growth_fixed / math.pow(1 + config.DATA_DISCOUNT_RATE, 10)

      # 4단계: 총 주식가치 계산 (할인된 영구가치+ 10년동안 할인된 현금흐름의합)
      total_stock_price = fcff_year_discount_sum + fcff_discount_rate # 총주식가치

      # 5단계: 1주당 주식가치 계산 (총주식가치/주식수)
      dcf = (total_stock_price* 100000000) / (data['STOCK_COUNT'][0] * 1000)

    return int(dcf)

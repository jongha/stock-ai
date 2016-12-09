#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.valuations.valuation import Valuation

# working draft
# 야마구치 요헤이
# 사업가치 = 영업이익 * 0.78 / 0.06685 = 영업이익 * 11.6 (배)
#     ▷ 0.78 : 기업 법인세율 22%
#     ▷ 0.06685 : (기업대출금리 4.30% + 종합주가지수 년평균수익율 9.07%)/2 = 6.685%
#     ▷ 정부가 기업의 법인세를 낮춰 주거나, 기업대출금리가 인하되면 기업의 가치가 상승하겠
# 기업대출금리 통계		http://ecos.bok.or.kr/		4.61


# 재산가치 = 유동자산 - (유동부채*1.2) + 투자자산
# ▷ 유동부채에 1.2배를 곱해 공제하는 이유는 혹시 모를 부채를 대비한 보수적인 관점
# ▷ 저자는 유형,무형자산을 제외하였는데, 이유는 유형,무형 자산 사용으로 결국 기업의 수익에 기 반영되었다고
# 판단한 것 같음
# ▷ 그래서 저는 진정한 재산가치를 구하기 위해서는 유동자산에서 매출채권을 차감해 줘야 된다고 판단하여 매출채권
# 을 추가로 공제하여 재산가치를 보수적으로 산출 합니다. ( 매출로 잡히기에 기 수익에 반영되었다고 보는 것이죠)
# 즉, 재산가치 = 유동자산 -(유동부채*1.2) - 매출채권 + 투자자산
class YamaguchiYohei(Valuation):
  def __init__(self, valuation):
    data = valuation.get_data()
    json = valuation.get_json()

    Valuation.__init__(self, data, json)
    self.set_json('BPS', self.valuate())

  def valuate(self):
    data = self.get_data()
    json = self.get_json()

    value = (data['STOCK_COUNT'][0] * 1000) * (1 - config.DATA_DISCOUNT_RATE)
    # print(data['STOCK_COUNT'][0], value)
    return int(value)

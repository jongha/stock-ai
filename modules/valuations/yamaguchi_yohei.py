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
    self.set_json('YAMAGUCHI_YOHEI', self.valuate())

  def valuate(self):
    data = self.get_data()
    json = self.get_json()

    value = 0
    value = (data['STOCK_COUNT'][0] * 1000) * (1 - config.DATA_DISCOUNT_RATE)

    # 영업이익
    business_profits_consensus = data['BUSINESS_PROFITS_CONSENSUS'].dropna(
    )[:1][0] * 100000000

    # 사업가치
    business_value = business_profits_consensus * (
        (1 - config.DATA_CORPORATE_TAX) /
        ((config.DATA_BUSINESSRATE_OF_INTEREST + config.DATA_SOTCK_YEARLY_MEAN)
         / 2))

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

    # 유동부채
    # 유동부채*100000000
    floating_debt = data['FLOATING_DEBT'].dropna()[:1][0] * 100000000

    # 매출채권
    # =매출채권및기타유동채권*100000000
    sales_bond = data['SALES_AND_FLOATING_BOND'].dropna()[:1][0] * 100000000

    # 투자자산
    # =(장기금융자산+관계기업등지분관련투자자산+장기매출채권및기타비유동채권+이연법인세자산+기타비유동자산)*100000000
    investment_assets = (
        data['LONG_FINANCE_ASSETS'].dropna()[:1][0] +
        data['IFRS_COMPANY_FINANCE_ASSETS'].dropna()[:1][0] +
        data['LONG_SALES_AND_NON_FLOATING_BOND'].dropna()[:1][0] +
        data['DEFERRED_CORPORATE_TAXES_ASSETS'].dropna()[:1][0] +
        data['ETC_NON_FLOATING_ASSETS'].dropna()[:1][0]) * 100000000

    # 재산가치
    asset_value = (quick_assets + inventory_assets) - (
        floating_debt * 1.2) - sales_bond + investment_assets

    # 비유동부채
    # =L125*100000000
    non_floating_bond = data['NON_FLOATING_BOND'].dropna()[:1][0] * 100000000
    # 기업가치
    company_value = business_value + asset_value - non_floating_bond

    # 주당 기업가치
    company_value_per = company_value / (data['STOCK_COUNT'].dropna()[:1][0] *
                                         1000)
    # 안전마진 가치
    value = company_value_per * (1 - config.DATA_DISCOUNT_RATE)

    return int(value)

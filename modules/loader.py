#-*- coding: utf-8 -*-
import os
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd
import config
import pandas
import re
import math
import modules.base as base

from modules.venders.itooza import Itooza
from modules.venders.fnguide_invest import FnguideInvest
from modules.venders.fnguide_ratio import FnguideRatio
from modules.venders.fnguide_finance import FnguideFinance
from modules.venders.sejong import Sejong
from modules.venders.post_cleaning import PostCleaning

from modules.venders import itooza, fnguide_invest
from modules.valuations.valuation import Valuation
from modules.valuations.grade import Grade
from modules.valuations.john_templeton import JohnTempleton
from modules.valuations.dcf import DCF
from modules.valuations.bps import BPS
from modules.valuations.per import PER
from modules.valuations.eps_bps import EPS_BPS
from modules.valuations.rim import RIM
from modules.valuations.yamaguchi_yohei import YamaguchiYohei
from modules.valuations.cantabile import Cantabile
from modules.valuations.peg import PEG
from modules.valuations.psr import PSR
from modules.valuations.graham import Graham
from modules.valuations.john_neff import JohnNeff
from modules.valuations.piotroski import Piotroski


def load(code):
  # fnguide_main_data = load_url(FNGUIDE_MAIN_URL, code)
  # # fnguide_invest_data = load_url(FNGUIDE_INVEST_URL, code)

  vender = Itooza(code)
  vender = FnguideInvest(code, vender)
  vender = FnguideRatio(code, vender)
  vender = FnguideFinance(code, vender)

  vender = Sejong(code, vender)
  vender = PostCleaning(code, vender)

  data = vender.get_data()
  json = vender.get_json()

  valuation = Valuation(data, json)
  valuation = Grade(valuation)
  valuation = JohnTempleton(valuation)
  valuation = DCF(valuation)
  valuation = BPS(valuation)
  valuation = PER(valuation)
  valuation = EPS_BPS(valuation)
  valuation = RIM(valuation)
  valuation = YamaguchiYohei(valuation)
  valuation = Cantabile(valuation)
  valuation = PEG(valuation)
  valuation = PSR(valuation)
  valuation = Graham(valuation)
  valuation = JohnNeff(valuation)
  valuation = Piotroski(valuation)

  # print(valuation.get_data())
  # print(valuation.get_json())

  # STOCK_COUNT: 주식수(천주)
  # PRICE: 주가
  # SALES: 매출액 (억)
  # BUSINESS_PROFITS: 영업이익 (억)
  # EPS_IFRS: EPS (연결)
  # EPS: EPS
  # EPS_RATE_OF_INCREASE: EPS증가율
  # ROE: ROE
  # ROA: ROA
  # ROIC: ROIC
  # PER: PER
  # BPS: BPS
  # PBR: PBR
  # DIVIDEND_PRICE: 배당금
  # DIVIDEND_RATE: 시가배당률 (%)
  # ROS: 순이익률
  # OPM: 영업이익률
  # FCFF: FCFF (억)
  # DIVIDEND_PAYOUT_RATIO: 배당성향(연결)
  # NET_INCOME_RATIO: 순이익률(매출/이익)
  # SALES_FCFF: 매출액/현금흐름
  # EV_FCFF: 현금투자수익률
  # DEBT_RATIO: 부채비율
  # CURRENT_RATIO: 유동비율
  # INTEREST_REWARD_POWER: 이자보상배율
  # EV/EBITDA
  # BPS_TIMES_0.5: PBR  0.5
  # BPS_TIMES_2: PBR  2
  # BPS_TIMES_3: PBR 3
  # EV1: EV시가총액(비지배주주지분포함) + 순차입부채
  # EPS_SIMPLE:
  # INVENTORY_ASSETS: 재고자산
  # FLOATING_FINANCE_ASSETS: 유동금융자산
  # SALES_AND_FLOATING_BOND: 매출채권및기타유동채권
  # ETC_FLOATING_ASSETS: 기타유동자산
  # CACHE_ASSETS: 현금및현금성자산
  # RESERVED_SALE_ASSETS: 매각예정비유동자산및처분자산집단
  # FLOATING_DEBT: 유동부채
  # LONG_FINANCE_ASSETS: 장기금융자산
  # IFRS_COMPANY_FINANCE_ASSETS: 관계기업등지분관련투자자산
  # LONG_SALES_AND_NON_FLOATING_BOND: 장기매출채권및기타비유동채권
  # DEFERRED_CORPORATE_TAXES_ASSETS: 이연법인세자산
  # ETC_NON_FLOATING_ASSETS: 기타비유동자산
  # NON_FLOATING_BOND: 비유동부채
  # NET_PROFIT_DURING_A_YEAR: 당기순이익(연율화)
  # TOTAL_CASH_FLOW: 총현금흐름
  # OPERATING_PROFIT_AFTER_TAX: 세후영업이익
  # GROSS_PROFIT_MARGIN: 매출총이익율
  # SALES_GROWTH_RATE: 매출액증가율
  # TOTAL_ASSETS_AVERAGE: 자산총계(평균)

  # PER_5:
  # PBR_5:
  # ROE_5:
  # EPS_5_GROWTH:
  # BPS_5_GROWTH:

  # Valuations
  # VALUATION_GRADE: 등급
  # VALUATION_JOHN_TEMPLETON: 존 템플턴 가치
  # VALUATION_DCF: 현금 흐름법 가치
  # VALUATION_BPS:
  # VALUATION_PER:
  # VALUATION_5_EPS_BPS: 5 EPS/BPS
  # VALUATION_RIM: 올슨 초과이익모형

  return data

  # fnguide_main_result = fnguide_main.load(fnguide_main_data['html'],
  #                                         fnguide_main_data['soup'])
  # fnguide_invest_result = fnguide_invest.load(fnguide_invest_data['html'], fnguide_invest_data['soup'])

  # data = {
  #     'json': {
  #         'code': code,
  #         'title': itooza_result['title'],
  #         'price': itooza_result['price'],
  #         'summary': fnguide_main_result['summary'],
  #         'eps': itooza_result['eps'],
  #         'per_5': itooza_result['per_5'],
  #         'pbr_5': itooza_result['pbr_5'],
  #         'roe_5': itooza_result['roe_5'],
  #         'eps_5_growth': itooza_result['eps_5_growth'],
  #         'bps_5_growth': itooza_result['eps_5_growth'],
  #         'grade': grade.valuate(itooza_result['roe_5_mean'],
  #                                 itooza_result['ros_5_mean']),
  #         'valuate': {
  #             # 현 EPS 과거 5년 PER 평균을 곱한 값
  #             'per_5': itooza_result['eps'] * itooza_result['per_5'],
  #             # 현 BPS 과거 5년 PBR 평균값을 곱한 값
  #             'pbr_5': itooza_result['bps'] * itooza_result['pbr_5'],
  #             # 주가수익배수(PER) 평가법, 과거 EPS성장률로 향후 5년의 EPS 추정하여 그 합의 1배~2배를 적용 (중간값 1.5배를 적용함)
  #             'johntempleton': johntempleton.valuate(
  #                 itooza_result['eps'], itooza_result['raw']['EPS_IFRS']),
  #         }
  #     },
  #     'itooza': itooza_result,
  #     'fnguide': {
  #         'main': fnguide_main_result,
  #         # 'invest': fnguide_invest_result,
  #     },
  # }

  # return data

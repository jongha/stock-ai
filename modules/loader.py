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
from modules.venders.sejong import Sejong
from modules.venders.post_cleaning import PostCleaning

from modules.venders import itooza, fnguide_invest
from modules.evaluations.evaluation import Evaluation
from modules.evaluations.grade import Grade
from modules.evaluations.johntempleton import JohnTempleton
from modules.evaluations.dcf import DCF
from modules.evaluations.bps import BPS
from modules.evaluations.per import PER
from modules.evaluations.eps_bps import EPS_BPS
from modules.evaluations.rim import RIM


def load(code):
  # fnguide_main_data = load_url(FNGUIDE_MAIN_URL, code)
  # # fnguide_invest_data = load_url(FNGUIDE_INVEST_URL, code)

  vender = Itooza(code)
  vender = FnguideInvest(code, vender)
  vender = FnguideRatio(code, vender)
  vender = Sejong(code, vender)
  vender = PostCleaning(code, vender)

  data = vender.get_data()
  json = vender.get_json()

  evaluation = Evaluation(data, json)
  evaluation = Grade(evaluation)
  evaluation = JohnTempleton(evaluation)
  evaluation = DCF(evaluation)
  evaluation = BPS(evaluation)
  evaluation = PER(evaluation)
  evaluation = EPS_BPS(evaluation)
  evaluation = RIM(evaluation)

  print(evaluation.get_json())

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
  # DIVIDEND_RATE: 시가배당률
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

  # PER_5:
  # PBR_5:
  # ROE_5:
  # EPS_5_GROWTH:
  # BPS_5_GROWTH:

  # EVALUATION_GRADE: 등급
  # EVALUATION_JOHN_TEMPLETON: 존 템플턴 가치
  # EVALUATION_DCF: 현금 흐름법 가치
  # EVALUATION_BPS:
  # EVALUATION_PER:
  # EVALUATION_5_EPS_BPS: 5 EPS/BPS
  # EVALUATION_RIM: 올슨 초과이익모형

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
  #         'grade': grade.evaluate(itooza_result['roe_5_mean'],
  #                                 itooza_result['ros_5_mean']),
  #         'evaluate': {
  #             # 현 EPS 과거 5년 PER 평균을 곱한 값
  #             'per_5': itooza_result['eps'] * itooza_result['per_5'],
  #             # 현 BPS 과거 5년 PBR 평균값을 곱한 값
  #             'pbr_5': itooza_result['bps'] * itooza_result['pbr_5'],
  #             # 주가수익배수(PER) 평가법, 과거 EPS성장률로 향후 5년의 EPS 추정하여 그 합의 1배~2배를 적용 (중간값 1.5배를 적용함)
  #             'johntempleton': johntempleton.evaluate(
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

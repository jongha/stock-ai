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
from modules.venders import itooza, fnguide_main, fnguide_invest
from modules.algorithm import grade, johntempleton

ITOOZA_URL = 'http://search.itooza.com/index.htm?seName=%s'
FNGUIDE_MAIN_URL = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=a%s'
FNGUIDE_INVEST_URL = 'http://comp.fnguide.com/SVO2/ASP/SVD_invest.asp?pGB=1&gicode=a%s'


def load_url(url, code):
  html = urlopen(
      Request(
          url % code, headers={'User-Agent': config.REQUEST_USER_AGENT}))

  soup = BeautifulSoup(
      html, 'lxml', from_encoding='utf-8')  # the content is utf-8

  return {'html': html, 'soup': soup}


def load(code):
  itooza_data = load_url(ITOOZA_URL, code)
  fnguide_main_data = load_url(FNGUIDE_MAIN_URL, code)
  # fnguide_invest_data = load_url(FNGUIDE_INVEST_URL, code)

  itooza_result = itooza.load(itooza_data['html'], itooza_data['soup'])
  fnguide_main_result = fnguide_main.load(fnguide_main_data['html'],
                                          fnguide_main_data['soup'])
  # fnguide_invest_result = fnguide_invest.load(fnguide_invest_data['html'], fnguide_invest_data['soup'])

  data = {
      'json': {
          'code': code,
          'title': itooza_result['title'],
          'price': itooza_result['price'],
          'summary': fnguide_main_result['summary'],
          'eps': itooza_result['eps'],
          'per_5': itooza_result['per_5'],
          'pbr_5': itooza_result['pbr_5'],
          'roe_5': itooza_result['roe_5'],
          'eps_5_growth': itooza_result['eps_5_growth'],
          'bps_5_growth': itooza_result['eps_5_growth'],
          'grade': grade.evaluate(itooza_result['roe_5_mean'],
                                  itooza_result['ros_5_mean']),
          'evaluate': {
              # 현 EPS 과거 5년 PER 평균을 곱한 값
              'per_5': itooza_result['eps'] * itooza_result['per_5'],
              # 현 BPS 과거 5년 PBR 평균값을 곱한 값
              'pbr_5': itooza_result['bps'] * itooza_result['pbr_5'],
              # 주가수익배수(PER) 평가법, 과거 EPS성장률로 향후 5년의 EPS 추정하여 그 합의 1배~2배를 적용 (중간값 1.5배를 적용함)
              'johntempleton': johntempleton.evaluate(
                  itooza_result['eps'], itooza_result['raw']['EPS_IFRS']),
          }
      },
      'itooza': itooza_result,
      'fnguide': {
          'main': fnguide_main_result,
          # 'invest': fnguide_invest_result,
      },
  }

  return data

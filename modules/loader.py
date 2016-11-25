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
from modules.venders import itooza, fnguide
from modules.algorithm import grade, johntempleton

ITOOZA_URL = 'http://search.itooza.com/index.htm?seName=%s'
FNGUIDE_URL = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=a%s'


def load_url(url, code):
  html = urlopen(
      Request(
          url % code, headers={'User-Agent': config.REQUEST_USER_AGENT}))

  soup = BeautifulSoup(
      html, 'lxml', from_encoding='utf-8')  # the content is utf-8

  return {'html': html, 'soup': soup}


def load(code):
  itooza_data = load_url(ITOOZA_URL, code)
  fnguide_data = load_url(FNGUIDE_URL, code)

  itooza_result = itooza.load(itooza_data['html'], itooza_data['soup'])
  fnguide_result = fnguide.load(fnguide_data['html'], fnguide_data['soup'])

  data = {
      'json': {
          'code': code,
          'title': itooza_result['title'],
          'price': itooza_result['price'],
          'summary': fnguide_result['summary'],
          'eps': itooza_result['eps'],
          'per_5': itooza_result['per_5'],
          'pbr_5': itooza_result['pbr_5'],
          'roe_5': itooza_result['roe_5'],
          'eps_5_growth': itooza_result['eps_5_growth'],
          'bps_5_growth': itooza_result['eps_5_growth'],
          'grade': grade.evaluate(itooza_result['roe_5_mean'],
                                  itooza_result['ros_5_mean']),
          'johntempleton': johntempleton.evaluate(itooza_result['eps'],
                                                  itooza_result['raw']['EPS_IFRS']),
      },
      'itooza': itooza_result,
      'fnguide': fnguide_result,
  }

  return data

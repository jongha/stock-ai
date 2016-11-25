#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math


# 존 템플턴
# 주가수익배수(PER) 평가법
# 과거 EPS성장률로 향후 5년의 EPS 추정하여 그 합의 1배~2배를 적용 (중간값 1.5배를 적용함)
# http://www.itooza.com/common/iview.php?no=2009020617100668054
def evaluate(eps, eps_ifrs):
  if not eps_ifrs.keys()[0].endswith('-12'):
    eps_ifrs = eps_ifrs.drop(eps_ifrs.index[[0]])

  eps_ifrs = eps_ifrs.dropna()[:5]
  df = pandas.DataFrame(columns=['EPS'])
  eps_count = len(eps_ifrs)

  percent_ifrs = eps_ifrs[0] / eps_ifrs[-1]
  direction = 1 if percent_ifrs >= 0 else -1
  eps_growth = math.pow(abs(percent_ifrs), 1 / (eps_count - 1)) * direction

  for i in range(5):
    new_eps = eps * eps_growth
    df.loc[i] = new_eps
    eps = new_eps

  return int(df.sum()['EPS'] * 1.5)
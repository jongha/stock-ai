#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math


# A등급 5년 순이익률 15% 이상, ROE 15% 이상 이상
# B등급 5년 순이익률 10% 이상, ROE 10% 이상 이상
# C등급 5년 ROE 10% 이상
# D등급 그외
def evaluate(roe_5_mean, ros_5_mean):
  if roe_5_mean is not None and ros_5_mean is not None:
    if ros_5_mean >= 15 and roe_5_mean >= 15:
      return 'A'

    elif ros_5_mean >= 10 and roe_5_mean >= 10:
      return 'B'

    elif roe_5_mean >= 10:
      return 'C'

    else:
      return 'D'

  else:
    return ''

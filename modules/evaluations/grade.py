#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math
from modules.evaluations.evaluation import Evaluation


# A등급 5년 순이익률 15% 이상, ROE 15% 이상 이상
# B등급 5년 순이익률 10% 이상, ROE 10% 이상 이상
# C등급 5년 ROE 10% 이상
# D등급 그외
class Grade(Evaluation):
  def __init__(self, evaluation):
    data = evaluation.get_data()
    json = evaluation.get_json()

    Evaluation.__init__(self, data, json)
    self.set_json('EVALUATION_GRADE', self.evaluate())

  def evaluate(self):
    data = self.get_data()
    roe_5_mean = data['ROE'].dropna()[:5].mean()
    ros_5_mean = data['ROS'].dropna()[:5].mean()

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

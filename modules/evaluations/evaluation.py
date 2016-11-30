#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math


class Evaluation:
  data = None

  def __init__(self, data):
    self.data = data
    pass

  def set_data(self, data):
    self.data = data

  def get_data(self):
    return self.data

  def evaluate(self):
    pass

  def concat(self, column_name, value):
    if value:
      df = pd.DataFrame(columns=[column_name], index=self.data.index.values)
      df[column_name][self.data.index[0]] = value
      self.data = pd.concat(
          [self.data, df], axis=1, join_axes=[self.data.index])
#-*- coding: utf-8 -*-
import os
import pandas as pd
import config
import pandas
import re
import math


class Valuation:
  data = None
  json = {}

  def __init__(self, data, json={}):
    self.data = data
    self.json = json

  def set_data(self, data):
    self.data = data

  def get_data(self):
    return self.data

  def set_json(self, key, value):
    self.json['VALUATION_' + key] = value

  def get_json(self):
    return self.json

  def valuate(self):
    pass

  def concat(self, column_name, value):
    if value:
      df = pd.DataFrame(columns=[column_name], index=self.data.index.values)
      df[column_name][self.data.index[0]] = value
      self.data = pd.concat(
          [self.data, df], axis=1, join_axes=[self.data.index])
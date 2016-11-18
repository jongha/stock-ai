#-*- coding: utf-8 -*-
import pandas as pd
import pandas_datareader.data as web
import datetime
import config
import os
import re

def get_file_path(code):
  return os.path.join(config.DATA_PATH, 'data', code)

def download(code, year1, month1, day1, year2, month2, day2):
  start = datetime.datetime(year1, month1, day1)
  end = datetime.datetime(year2, month2, day2)
  df = web.DataReader("%s.KS" % code, "yahoo", start, end)
  df.to_pickle(get_file_path(code))

  return df

def load(code):
  df = pd.read_pickle(get_file_path(code))
  return df
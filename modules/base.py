#-*- coding: utf-8 -*-
import pandas as pd
import pandas_datareader.data as web
import datetime
import config
import os
import re
import pickle

def get_file_path(code):
  return os.path.join(config.DATA_PATH, 'data', code + '.pkl')

def download(code, year1, month1, day1, year2, month2, day2):
  start = datetime.datetime(year1, month1, day1)
  end = datetime.datetime(year2, month2, day2)
  df = web.DataReader('%s.KS' % code, 'yahoo', start, end)
  save(code, df)

  return df

def load(code):
  try:
    return pd.read_pickle(code)
  except:
    pass

  return None

def save(code, df):
  df.to_pickle(code)

def dump(code, df):
  with open(get_file_path(code), 'wb') as handle:
    pickle.dump(df, handle)

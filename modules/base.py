#-*- coding: utf-8 -*-
import pandas as pd
import pandas_datareader.data as web
import datetime
import config
import os
import re
import pickle


def get_file_path(name):
  if not os.path.exists(config.DATA_PATH):
    try:
      os.makedirs(config.DATA_PATH)
    except:
      pass

  return os.path.join(config.DATA_PATH, name + config.DATA_EXTENSION)


def download(code, year1, month1, day1, year2, month2, day2):
  start = datetime.datetime(year1, month1, day1)
  end = datetime.datetime(year2, month2, day2)
  df = web.DataReader('%s.KS' % code, 'yahoo', start, end)
  df.to_pickle(get_file_path(code))

  return df


def load(code):
  try:
    with open(get_file_path(code), 'rb') as handle:
      return pickle.load(handle)
  except:
    pass

  return None


def dump(code, data):
  with open(get_file_path(code), 'wb') as handle:
    pickle.dump(data, handle)
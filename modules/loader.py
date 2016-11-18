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

BASE_URL = 'http://search.itooza.com/index.htm?seName=%s'

def load(code):
  url = BASE_URL % code
  html = urlopen(Request(url, headers={'User-Agent': config.REQUEST_USER_AGENT}))
  soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8') # the content is utf-8


  price_contents = soup.find('div', class_='item-detail').find('span').contents
  price = ''.join(re.findall('\d+', price_contents[0])) if len(price_contents) > 0 else 0

  tables = soup.find_all('table', limit=4)

  simple = get_data_simple(tables)
  summary = get_data_summary(tables)
  raw = get_data_raw(tables)

  return (price, simple, summary, raw)


def get_data_simple(tables):
  df = pd.read_html(str(tables[0]), header=0)[0]
  return df


def get_data_summary(tables):
  df = pd.read_html(str(tables[1]), header=0)[0]
  df.columns = ['PER_5', 'PBR_5', 'ROE_5', 'EPS_5_GROWTH', 'BPS_5_GROWTH']
  return df


def get_data_raw(tables):
  if len(tables) >= 4:
    df = pd.read_html(str(tables[3]), header=0)[0]
    columns = []
    for index in range(len(df.columns)):
      columns.append(date_column(df.columns[index]))

    df.columns = columns
    if len(df['MONTH'].dropna()) > 0:
      for index in range(len(df['MONTH'])):
        df.loc[index,('MONTH')] = column_name(df['MONTH'][index])

      df = df.transpose()
      df.columns = df.iloc[0]
      df = df.reindex(df.index.drop('MONTH'))
      return df

  return None

def date_column(data):
  data = data.replace('월', '').replace('.', '-')
  if bool(re.match('\d{2}-\d{2}', data)):
    data = '20' + data
  else:
    data = 'MONTH'

  return data


def column_name(data):
  name = {
    '주당순이익(EPS,연결지배)': 'EPS_IFRS',
    '주당순이익(EPS,개별)': 'EPS',
    'PER (배)': 'PER',
    '주당순자산(지분법)': 'BPS',
    'PBR (배)': 'PBR',
    '주당 배당금': 'DIVIDEND_PRICE',
    '시가 배당률 (%)': 'DIVIDEND_RATE',
    'ROE (%)': 'ROE',
    '순이익률 (%)': 'ROS',
    '영업이익률 (%)': 'OPM',
  }

  if data and data in name:
    return name[data]

  return data
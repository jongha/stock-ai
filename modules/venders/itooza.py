#-*- coding: utf-8 -*-
import os
import re
import pandas as pd


def load(html, soup):
  price_contents = soup.find('div', class_='item-detail').find('span').contents

  price = ''.join(re.findall('\d+', price_contents[0])) if len(
      price_contents) > 0 else 0

  title = soup.find('div', class_='item-head').find('h1').contents[0].strip()
  tables = soup.find_all('table', limit=4)

  simple = get_data_simple(tables)
  summary = get_data_summary(tables)

  raw = get_data_raw(tables)
  raw = get_dividend_payout_ratio(raw)
  raw = get_bps_multiple(raw, 0.5)
  raw = get_bps_multiple(raw, 2)
  raw = get_bps_multiple(raw, 3)
  raw = get_price(raw)

  return {
      'price': price,
      'title': title,
      'eps': simple['EPS'].mean(),
      'bps': simple['BPS'].mean(),
      'per_5': summary['PER_5'][0],
      'pbr_5': summary['PBR_5'][0],
      'roe_5': summary['ROE_5'][0],
      'eps_5_growth': summary['EPS_5_GROWTH'][0],
      'bps_5_growth': summary['BPS_5_GROWTH'][0],
      'roe_5_mean': raw['ROE'].dropna()[:5].mean(),
      'ros_5_mean': raw['ROS'].dropna()[:5].mean(),
      'simple': simple,
      'summary': summary,
      'raw': raw,
      'html': html,
  }


# 주가
def get_price(raw):
  column_name = 'Price'
  df = pd.DataFrame(columns=[column_name], index=raw.index.values)
  for month in raw.index.values:
    value = raw['BPS'][month] * raw['PBR'][month]
    df[column_name][month] = int(value if not pd.isnull(value) else 0)
  raw = pd.concat([raw, df], axis=1, join_axes=[raw.index])
  return raw


def get_bps_multiple(raw, multiple):
  column_name = 'BPS*' + str(multiple)
  df = pd.DataFrame(columns=[column_name], index=raw.index.values)
  for month in raw.index.values:
    value = raw['BPS'][month] * multiple
    df[column_name][month] = int(value if not pd.isnull(value) else 0)
  raw = pd.concat([raw, df], axis=1, join_axes=[raw.index])
  return raw


# 배당성향(연결)
def get_dividend_payout_ratio(raw):
  column_name = 'Dividend Payout Ratio'
  df = pd.DataFrame(columns=[column_name], index=raw.index.values)
  for month in raw.index.values:
    value = raw['DIVIDEND_PRICE'][month] / raw['EPS_IFRS'][month] * 100
    df[column_name][month] = int(value if not pd.isnull(value) else 0)
  raw = pd.concat([raw, df], axis=1, join_axes=[raw.index])
  return raw


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
        df.loc[index, ('MONTH')] = column_name(df['MONTH'][index])

      df = df.transpose()
      df.columns = df.iloc[0]
      df = df.reindex(df.index.drop('MONTH'))
      return df

  return None


def date_column(data):
  data = data.replace('월', '').replace('.', '-')
  if bool(re.match('\d{2}-\d{2}', data)):
    data = '20' + data[0:2]
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

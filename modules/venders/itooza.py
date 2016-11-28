#-*- coding: utf-8 -*-
import os
import re
import pandas as pd
from modules.venders.vender import Vender


class Itooza(Vender):
  URL = 'http://search.itooza.com/index.htm?seName=%s'

  def __init__(self, code, vender=None):
    Vender.__init__(self, self.URL, vender)

    response = self.load_url(code)
    html, soup = response['html'], response['soup']

    price_contents = soup.find(
        'div', class_='item-detail').find('span').contents

    price = ''.join(re.findall('\d+', price_contents[0])) if len(
        price_contents) > 0 else 0

    title = soup.find('div', class_='item-head').find('h1').contents[0].strip()
    tables = soup.find_all('table', limit=4)

    simple = self.get_data_simple(tables)
    summary = self.get_data_summary(tables)

    self.set_tables(tables)
    self.set_dividend_payout_ratio()
    self.set_bps_multiple(0.5)
    self.set_bps_multiple(2)
    self.set_bps_multiple(3)
    self.set_get_price()

    # return {
    #     'price': price,
    #     'title': title,
    #     'eps': simple['EPS'].mean(),
    #     'bps': simple['BPS'].mean(),
    #     'per_5': summary['PER_5'][0],
    #     'pbr_5': summary['PBR_5'][0],
    #     'roe_5': summary['ROE_5'][0],
    #     'eps_5_growth': summary['EPS_5_GROWTH'][0],
    #     'bps_5_growth': summary['BPS_5_GROWTH'][0],
    #     'roe_5_mean': data['ROE'].dropna()[:5].mean(),
    #     'ros_5_mean': data['ROS'].dropna()[:5].mean(),
    #     'simple': simple,
    #     'summary': summary,
    #     'data': data,
    #     'html': html,
    # }

  # 주가

  def set_get_price(self):
    column_name = 'PRICE'
    df = pd.DataFrame(columns=[column_name], index=self.data.index.values)
    data = self.get_data()

    for month in data.index.values:
      value = data['BPS'][month] * self.data['PBR'][month]
      df[column_name][month] = int(value if not pd.isnull(value) else 0)

    self.concat_data(df)

  def set_bps_multiple(self, multiple):
    column_name = 'BPS_TIMES_' + str(multiple)
    df = pd.DataFrame(columns=[column_name], index=self.data.index.values)
    data = self.get_data()

    for month in data.index.values:
      value = data['BPS'][month] * multiple
      df[column_name][month] = int(value if not pd.isnull(value) else 0)

    self.concat_data(df)

  # 배당성향(연결)
  def set_dividend_payout_ratio(self):
    column_name = 'DIVIDEND_PAYOUT_RATIO'
    df = pd.DataFrame(columns=[column_name], index=self.data.index.values)
    data = self.get_data()

    for month in data.index.values:
      value = data['DIVIDEND_PRICE'][month] / self.data['EPS_IFRS'][
          month] * 100
      df[column_name][month] = int(value if not pd.isnull(value) else 0)

    self.concat_data(df)

  def get_data_simple(self, tables):
    df = pd.read_html(str(tables[0]), header=0)[0]
    return df

  def get_data_summary(self, tables):
    df = pd.read_html(str(tables[1]), header=0)[0]
    df.columns = ['PER_5', 'PBR_5', 'ROE_5', 'EPS_5_GROWTH', 'BPS_5_GROWTH']
    return df

  def set_tables(self, tables):
    if len(tables) >= 4:
      df = pd.read_html(str(tables[3]), header=0)[0]
      columns = []
      for index in range(len(df.columns)):
        columns.append(self.date_column(df.columns[index]))

      df.columns = columns
      if len(df['MONTH'].dropna()) > 0:
        for index in range(len(df['MONTH'])):
          df.loc[index, ('MONTH')] = self.column_name(df['MONTH'][index])

        df = df.transpose()
        df.columns = df.iloc[0]
        df = df.reindex(df.index.drop('MONTH'))
        self.concat_data(df)

  def date_column(self, data):
    data = data.replace('월', '').replace('.', '-')
    if bool(re.match('\d{2}-\d{2}', data)):
      data = '20' + data[0:2]
    else:
      data = 'MONTH'

    return data

  def column_name(self, data):
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

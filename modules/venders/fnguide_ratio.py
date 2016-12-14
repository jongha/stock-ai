#-*- coding: utf-8 -*-
import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from modules.venders.vender import Vender


class FnguideRatio(Vender):
  URL = 'http://comp.fnguide.com/SVO2/ASP/SVD_FinanceRatio.asp?pGB=1&gicode=a%s'

  def __init__(self, code, vender=None):
    Vender.__init__(self, self.URL, vender)

    response = self.load_url(code)
    html, soup = response['html'], response['soup']

    tables = soup.find_all('div', class_='um_table')
    df = self.get_data_from_table(tables[0])

    self.concat(df, 'EPS_RATE_OF_INCREASE')
    self.concat(df, 'ROA')
    self.concat(df, 'ROIC')
    self.concat(df, 'CURRENT_RATIO')
    self.concat(df, 'INTEREST_REWARD_POWER')
    self.concat(df, 'BUSINESS_PROFITS_CONSENSUS')
    self.concat(df, 'NET_PROFIT_DURING_A_YEAR')
    self.concat(df, 'GROSS_PROFIT_MARGIN')
    self.concat(df, 'SALES_GROWTH_RATE')
    self.concat(df, 'TOTAL_ASSETS_AVERAGE')

  def concat(self, df, column):
    data = self.get_data()
    self.concat_data(df[column])

  def get_data_from_table(self, table):
    soup = BeautifulSoup(str(table), 'lxml')
    for th in soup.find_all('th', class_='clf'):
      items = th.find_all(['dd', 'a', 'span'])
      for item in items:
        item.extract()

    df = pd.read_html(str(soup), header=0)[0]
    columns = []
    for index in range(len(df.columns)):
      columns.append(self.date_column(df.columns[index]))

    df.columns = columns
    df = df.transpose()
    df.columns = df.iloc[0]
    df = df.reindex(df.index.drop('MONTH'))

    columns = []
    for index in range(len(df.columns)):
      columns.append(self.date_column(df.columns[index]))

    duplicate_postfix = {}
    for i in range(len(columns)):
      column = columns[i]
      if columns.count(column) > 1:
        count = 0
        if column in duplicate_postfix:
          count = duplicate_postfix[column] + 1

        duplicate_postfix[column] = count

      columns[i] = column + (str(duplicate_postfix[column])
                             if column in duplicate_postfix and
                             duplicate_postfix[column] > 0 else '')

    df.columns = columns

    return df

  def date_column(self, data):
    if not self.isNaN(data):
      if bool(re.match('\d{4}/\d{2}', data)):
        data = data[0:4]
      else:
        data = self.column_name(data)
    else:
      data = self.id_generator()

    return data

  def column_name(self, name):
    names = {
        'IFRS(연결)': 'MONTH',
        'EPS증가율': 'EPS_RATE_OF_INCREASE',
        '유동비율': 'CURRENT_RATIO',
        '이자보상배율(배)': 'INTEREST_REWARD_POWER',
        '영업이익': 'BUSINESS_PROFITS_CONSENSUS',
        '당기순이익(연율화)': 'NET_PROFIT_DURING_A_YEAR',
        '매출총이익율': 'GROSS_PROFIT_MARGIN',
        '매출액증가율': 'SALES_GROWTH_RATE',
        '자산총계(평균)': 'TOTAL_ASSETS_AVERAGE',
    }

    if name and name in names:
      return names[name]

    return name

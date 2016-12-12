#-*- coding: utf-8 -*-
import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from modules.venders.vender import Vender


class FnguideInvest(Vender):
  URL = 'http://comp.fnguide.com/SVO2/ASP/SVD_invest.asp?pGB=1&gicode=a%s'

  def __init__(self, code, vender=None):
    Vender.__init__(self, self.URL, vender)

    response = self.load_url(code)
    html, soup = response['html'], response['soup']

    tables = soup.find_all('div', class_='um_table')
    df = self.get_data_from_table(tables[1])

    self.concat(df, 'FCFF')
    self.concat(df, 'STOCK_COUNT')
    self.concat(df, 'EV/EBITDA')
    self.concat(df, 'EV1')

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
        'IFRS 연결': 'MONTH',
        '수정평균주식수': 'STOCK_COUNT',
    }

    if name and name in names:
      return names[name]

    return name

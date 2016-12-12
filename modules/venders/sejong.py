#-*- coding: utf-8 -*-
import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from modules.venders.vender import Vender


class Sejong(Vender):
  URL = 'http://www.sejongdata.com/business_include_fr/table_main0_bus_01.html?&no=%s'

  def __init__(self, code, vender=None):
    Vender.__init__(self, self.URL, vender)

    response = self.load_url(code)
    html, soup = response['html'], response['soup']

    tables = soup.find_all('table')
    df = self.get_data_from_table(tables[1])

    self.concat(df, 'SALES')
    self.concat(df, 'BUSINESS_PROFITS')
    self.concat(df, 'CAPITAL_TOTAL')
    self.concat(df, 'DEBT_TOTAL')
    self.set_debt_ratio()

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

  # 부채비율
  def set_debt_ratio(self):
    column_name = 'DEBT_RATIO'
    df = pd.DataFrame(columns=[column_name], index=self.data.index.values)
    data = self.get_data()

    for month in data.index.values:
      value = data['DEBT_TOTAL'][month] / self.data['CAPITAL_TOTAL'][
          month] * 100
      df[column_name][month] = int(value if not pd.isnull(value) else 0)

    self.concat_data(df)

  def date_column(self, data):
    if not self.isNaN(data):
      if bool(re.match('\d{4}\.\d{2}', data)):
        data = data[0:4]
      else:
        data = self.column_name(data)
    else:
      data = self.id_generator()

    return data

  def column_name(self, name):
    names = {
        'Unnamed: 0': 'MONTH',
        '매출액': 'SALES',
        '영업이익': 'BUSINESS_PROFITS',
        '자본총계': 'CAPITAL_TOTAL',
        '부채총계': 'DEBT_TOTAL',
    }

    if name and name in names:
      return names[name]

    return name

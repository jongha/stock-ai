#-*- coding: utf-8 -*-
import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from modules.venders.vender import Vender


class FnguideFinance(Vender):
  URL = 'http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=a%s'
  unknown_column_map = {}
  unknown_column_counter = 0

  def __init__(self, code, vender=None):
    Vender.__init__(self, self.URL, vender)
    self.unknown_column_map = {3: 'FLOATING_DEBT', 4: 'NON_FLOATING_BOND'}
    self.unknown_column_counter = 0

    response = self.load_url(code)
    html, soup = response['html'], response['soup']

    tables = soup.find_all('div', class_='um_table')
    df = self.get_data_from_table(tables[2])

    self.concat(df, 'INVENTORY_ASSETS')
    self.concat(df, 'FLOATING_FINANCE_ASSETS')
    self.concat(df, 'SALES_AND_FLOATING_BOND')
    self.concat(df, 'ETC_FLOATING_ASSETS')
    self.concat(df, 'CACHE_ASSETS')
    self.concat(df, 'RESERVED_SALE_ASSETS')
    self.concat(df, 'FLOATING_DEBT')
    self.concat(df, 'LONG_FINANCE_ASSETS')
    self.concat(df, 'IFRS_COMPANY_FINANCE_ASSETS')
    self.concat(df, 'LONG_SALES_AND_NON_FLOATING_BOND')
    self.concat(df, 'DEFERRED_CORPORATE_TAXES_ASSETS')
    self.concat(df, 'ETC_NON_FLOATING_ASSETS')
    self.concat(df, 'NON_FLOATING_BOND')

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
      self.unknown_column_counter += 1
      data = self.unknown_column_map[
          self.
          unknown_column_counter] if self.unknown_column_counter in self.unknown_column_map else self.id_generator(
          )

    return data

  def column_name(self, name):
    names = {
        'IFRS(연결)': 'MONTH',
        '재고자산': 'INVENTORY_ASSETS',
        '유동금융자산': 'FLOATING_FINANCE_ASSETS',
        '매출채권및기타유동채권': 'SALES_AND_FLOATING_BOND',
        '기타유동자산': 'ETC_FLOATING_ASSETS',
        '현금및현금성자산': 'CACHE_ASSETS',
        '매각예정비유동자산및처분자산집단': 'RESERVED_SALE_ASSETS',
        '유동부채': 'FLOATING_DEBT',
        '장기금융자산': 'LONG_FINANCE_ASSETS',
        '관계기업등지분관련투자자산': 'IFRS_COMPANY_FINANCE_ASSETS',
        '장기매출채권및기타비유동채권': 'LONG_SALES_AND_NON_FLOATING_BOND',
        '이연법인세자산': 'DEFERRED_CORPORATE_TAXES_ASSETS',
        '기타비유동자산': 'ETC_NON_FLOATING_ASSETS',
        '비유동부채': 'NON_FLOATING_BOND'
    }

    if name and name in names:
      return names[name]

    return name

#-*- coding: utf-8 -*-
import os
import re
import pandas as pd
from modules.venders.vender import Vender


class PostCleaning(Vender):
  def __init__(self, code, vender=None):
    Vender.__init__(self, None, vender)

    self.set_dividend_payout_ratio()
    self.set_bps_multiple(0.5)
    self.set_bps_multiple(2)
    self.set_bps_multiple(3)
    self.set_get_price()
    self.set_net_income_ratio()
    self.set_sales_fcff()
    self.set_ev1_fcff()

  def set_ev1_fcff(self):
    column_name = 'EV_FCFF'
    df = pd.DataFrame(columns=[column_name], index=self.data.index.values)
    data = self.get_data()

    if 'FCFF' in data.columns and 'EV1' in data.columns:
      for month in data.index.values:
        value = (data['FCFF'][month] / data['EV1'][month]) * 100
        df[column_name][month] = round(value if not pd.isnull(value) else 0, 2)

      self.concat_data(df)

  def set_sales_fcff(self):
    column_name = 'SALES_FCFF'
    df = pd.DataFrame(columns=[column_name], index=self.data.index.values)
    data = self.get_data()

    if 'FCFF' in data.columns and 'SALES' in data.columns:
      for month in data.index.values:
        value = (data['FCFF'][month] / data['SALES'][month]) * 100
        df[column_name][month] = round(value if not pd.isnull(value) else 0, 2)

      self.concat_data(df)

  def set_net_income_ratio(self):
    column_name = 'NET_INCOME_RATIO'
    df = pd.DataFrame(columns=[column_name], index=self.data.index.values)
    data = self.get_data()

    if 'EPS_IFRS' in data.columns and 'SALES' in data.columns:
      for month in data.index.values:
        value = (data['EPS_IFRS'][month] /
                 ((data['SALES'][month] * 100000000) /
                  (self.data['STOCK_COUNT'][month] * 1000))) * 100
        df[column_name][month] = round(value if not pd.isnull(value) else 0, 2)

      self.concat_data(df)

  # 주가
  def set_get_price(self):
    column_name = 'PRICE'
    df = pd.DataFrame(columns=[column_name], index=self.data.index.values)
    data = self.get_data()

    if 'BPS' in data.columns and 'PBR' in data.columns:
      for month in data.index.values:
        value = data['BPS'][month] * self.data['PBR'][month]
        df[column_name][month] = int(value if not pd.isnull(value) else 0)

      self.concat_data(df)

  def set_bps_multiple(self, multiple):
    column_name = 'BPS_TIMES_' + str(multiple)
    df = pd.DataFrame(columns=[column_name], index=self.data.index.values)
    data = self.get_data()

    if 'BPS' in data.columns:
      for month in data.index.values:
        value = data['BPS'][month] * multiple
        df[column_name][month] = int(value if not pd.isnull(value) else 0)

      self.concat_data(df)

  # 배당성향(연결)
  def set_dividend_payout_ratio(self):
    column_name = 'DIVIDEND_PAYOUT_RATIO'
    df = pd.DataFrame(columns=[column_name], index=self.data.index.values)
    data = self.get_data()

    if 'DIVIDEND_PRICE' in data.columns:
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

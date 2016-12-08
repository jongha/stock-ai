#-*- coding: utf-8 -*-
import os
import re
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import config
import pandas as pd


class Vender:
  data = None
  json = {}
  url = ''

  def __init__(self, url, vender, json={}):
    if url is not None:
      self.set_url(url)

    if vender is not None:
      self.set_vender(vender)

  def set_json(self, key, value):
    self.json[key] = value

  def get_json(self):
    return self.json

  def get_url(self):
    return self.url

  def set_url(self, url):
    self.url = url

  def load_url(self, code):
    html = urlopen(
        Request(
            self.url % code, headers={'User-Agent': config.REQUEST_USER_AGENT
                                      }))

    soup = BeautifulSoup(
        html, 'lxml', from_encoding='utf-8')  # the content is utf-8

    return {'html': html, 'soup': soup}

  def set_vender(self, vender):
    if vender is not None:
      self.set_data(vender.get_data())

  def set_data(self, data):
    self.data = data

  def get_data(self):
    return self.data

  def concat_data(self, df):
    if self.data is not None:
      self.data = pd.concat(
          [self.data, df], axis=1, join_axes=[self.data.index])
    else:
      self.data = df
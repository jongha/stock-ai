#-*- coding: utf-8 -*-
import os
import re
import pandas as pd


def load(html, soup):
  # summary = ' '.join([
  #     content.contents[0]
  #     for content in soup.find(
  #         'ul', id='bizSummaryContent').find_all('li')
  # ])

  return {'html': html, }

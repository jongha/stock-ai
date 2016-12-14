#-*- coding: utf-8 -*-
import os
import tempfile

APP_NAME = 'stock-ai'
PRODUCTION = True  #False

REQUEST_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'

# os.path.dirname(os.path.abspath(__file__))
DATA_DISCOUNT_RATE = 0.1  # 할인율, percent
DATA_CFN = 0.03  # 영구가치증가율, percent
DATA_FIXED_RATE = (1 + DATA_CFN) / (
    DATA_DISCOUNT_RATE - DATA_CFN)  # 가치증가율, percent
DATA_VALUE_OF_BPS = 0.4  # BPS 기업가치, percent
DATA_VALUE_OF_EPS = 0.6  # EPS 기업가치, percent
DATA_EXPECT_GROWTH_RATE = 1  # 기대성장률 조정비율
DATA_CAPITAL_RATIO_RATE = 0.3  # 자본조정비율
DATA_CORPORATE_TAX = 0.22  # 법인세
DATA_BUSINESSRATE_OF_INTEREST = 0.0461  # 기업대출금리		4.61
DATA_SOTCK_YEARLY_MEAN = 0.0907  # 종합주가 연평균수익			9.07

DATA_BASE_PATH = tempfile.gettempdir()
DATA_PATH = os.path.join(DATA_BASE_PATH, APP_NAME)
DATA_EXTENSION = '.pkl'

DATA_STOCKS_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'database', 'stocks.csv')
DATA_STOCKS_SQLITE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'database', 'stocks.sqlite')

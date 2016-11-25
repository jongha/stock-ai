#-*- coding: utf-8 -*-
import os
import tempfile

APP_NAME = 'stock-ai'
REQUEST_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'

DATA_DISCOUNT_RATE = 0.1  # percent
DATA_BASE_PATH = tempfile.gettempdir(
)  # os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(DATA_BASE_PATH, APP_NAME)

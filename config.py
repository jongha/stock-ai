#-*- coding: utf-8 -*-
import os
import tempfile

REQUEST_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'

DATA_DISCOUNT_RATE = 0.1 # percent
DATA_PATH = tempfile.gettempdir() # os.path.dirname(os.path.abspath(__file__))
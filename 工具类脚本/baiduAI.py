# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2020/12/11 14:59'
from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = 'ba8b5a68ae32473f8dadded5d77c769a'
API_KEY = 'd11b843b0aad4f7793a6902f5c6d42c1'
SECRET_KEY = '8f0cc679142047ebad21e5094c0d3fbc'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

text = "百度是一家人工只能公司"

a=client.ecnet(text)

print(a)
#coding:utf-8
'''
Created on 2017年10月9日

@author: cjj


'''
import requests

s = requests

data={"quest":"小李"}
r = s.post('http://127.0.0.1:8000/my_love', data)

print (r.status_code)
print (r.headers['content-type'])
r.encoding = 'utf-8'
print (r.text)
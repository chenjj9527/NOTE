#coding:utf-8
'''
Created on 2017年10月9日

@author: cjj

@email:

'''
import requests
import json
s = requests
data_lookup={"method":'lookup','id':1,'jsonrpc':2.0,'params':{'user_id':2}}
data_chat={"method":'chat','id':1,'jsonrpc':2.0,'params':{'user_id':2,"quest":"银联二维码支付怎么用"}}
data_retrain={"method":'retrain','id':1,'jsonrpc':2.0,'params':{'user_id':2}}
r = s.post('http://127.0.0.1:8000/deep_chat', json.dumps(data_lookup))

print (r.status_code)
print (r.headers['content-type'])
r.encoding = 'utf-8'
print (r.text)
#coding:utf-8

import re
import json
import requests
from multiprocessing import Pool
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    #.*是贪婪模型,.*?是最小匹配模式,()里的是目标结果,re.S代表匹配任何字符(避免换行符匹配不上)
    '''
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?<img alt.*?src="(.*?)"></a>'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    '''
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?<p.*?title="(.*?)".*?star">(.*?)</p>.*?releasetime">(.*?)</p>',re.S)
    items = re.findall(pattern,html)
    print(items)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4][5:]
            }

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
   
def main(offset):
    url='http://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url)
    #print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__=='__main__':
    Pool=Pool(processes=10)
    Pool.map(main,[i*10 for i in range(10)])


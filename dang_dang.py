import re
import requests
import json



def request_dangdang(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.ResponseException:
        return None

def parse_result(html):
    pattern = re.compile('<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {'range':item[0],
               'name':item[1],
               'star':item[2],
               'author' :item[3],
               'price':item[4],
        }

def write_to_book(item):
    print('写入'+str(item))
    with open('book.txt','a',encoding='UTF-8') as f:
        f.write(json.dumps(item,ensure_ascii=False) + '/n')
        f.close

def carry(page):
    url = ('http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-'+str(page))
    html = request_dangdang(url)
    items = parse_result(html)
    for item in items:
        write_to_book(item)






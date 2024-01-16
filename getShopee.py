import requests, json, random
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os, re, datetime, time, json
import requests, random
from bs4 import BeautifulSoup 
import multiprocessing as mp
from functools import partial
from itertools import product


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
    'X-Requested-With': 'XMLHttpRequest'
}    

url = 'https://shopee.vn/api/v4/pages/get_category_tree'

def convertName(name):
    pass

# return list category_categoryChild_level
# url = 'https://shopee.vn/api/v4/pages/get_category_tree'
def get_category(link):
    with requests.get(link, headers=headers) as r:
        data = r.json()['data']['category_list']

    category = []
    for x in data:
        catid = x['catid']
        level = x['level']
        _data = f'{catid}_{catid}_{level}'
        category.append(_data)

        for y in x['children']:
            _idc = y['catid']
            _lvc = y['level']
            _data = f'{catid}_{_idc}_{_lvc}'
            category.append(_data)
    return category

# print(get_category(url))


# url = 'https://shopee.vn/api/v4/recommend/recommend?bundle=category_landing_page&cat_level=1&catid=11035567&limit=200&offset=200' 
# params: cat_level, catid, offset, limit: max 200 records
# input: category_categoryChild_level, page
def parse_page(catid_level, page):

    info = catid_level.split('_')
    catid    = info[0]
    catchild = info[1]
    level    = info[2]
    pathDir = None
    
    print(catchild)

    if catid == catchild:
        pathDir = catid
        os.makedirs(pathDir, exist_ok=True)
    else:
        pathDir = f'{catid}/{catchild}'
        os.makedirs(pathDir, exist_ok=True)


    link = f'https://shopee.vn/api/v4/recommend/recommend?bundle=category_landing_page&cat_level={level}&catid={catchild}&limit=200'
    
    offset = page*200
    link = f'{link}&offset={offset}'
    # print(link)

    with requests.get(link, headers=headers) as r:
        rawData = r.json()
    
    # save data
    path = f'{pathDir}/{page}.json'
    with open(path, 'w') as f:
        json.dump(rawData, f)



if __name__ == "__main__":
    # multiprocessing
    catid_level = get_category(url)
    st = time.time()

    # code run

    en = time.time()
    print("Time taken = ", en-st)
    print("Done!")



import requests
import time
import json
import threading
import queue
import random
import datetime
import os
import urllib3
import pickle

from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from collections import defaultdict
from pprint import pprint

from config.assistant import *
from config.site_config import *

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

from starlette.responses import JSONResponse


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()
job_group = {}

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


# JSON 파일 저장
def save_json():
    global job_group
    tf = open(file_path, 'w')
    json.dump(job_group, tf)
    tf.close()
    job_group = {}
    
# JSON 파일 불러오기
@app.get("/load_json/")
def load_json():
    global job_group
    with open(file_path, 'r') as file:
        job_group = json.load(file)
   
    
# 구직사이트 크롤링 시작
@app.get("/get_info/")
def crawling_info():
    # 저장된 키워드 별 검색
    for search_word in search_words:

        item_count = 0
        current_page = 1
        
        # 검색 결과 리스트 페이지 별 확인
        search_loop = True
        while(search_loop):
            search_link = f'https://www.saramin.co.kr/zf_user/search/recruit'\
                + f'?search_area=main'\
                + f'&search_done=y'\
                + f'&search_optional_item=n'\
                + f'&searchType=search'\
                + f'&recruitSort=relation'\
                + f'&searchword={search_word}'\
                + f'&recruitPage={current_page}'\
                + f'&recruitPageCount={page_view_items}'\
                + f'&company_cd={company_cd}'\
                + f'&mainSearch=y'

            response = requests.get(search_link, verify=False)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            if len(soup.find_all('div', attrs={'class': 'info_no_result'})) == 1:
                search_loop = False
            else:
                current_page += 1

                page_items = len(soup.find_all('h2', attrs={'class': 'job_tit'}))

                # 해당 페이지 리스트 (1 ~ 100)
                for i in range(1, page_items+1):
                    elements = soup.select(f'div.content > div:nth-child({i})')[0]

                    # 채용공고명
                    str_title = elements.find('a', attrs={'class': 'data_layer'})['title']

                    # 회사명
                    try:
                        str_company1 = elements.find('a', attrs={'class': 'track_event data_layer'}).text
                        #str_company = str_company.replace(' ', '').replace('\n', '').replace('(주)', '')
                        str_company2 = str_company1.replace(' ', '')
                        str_company3 = str_company2.replace('\n', '')
                        str_company = str_company3.replace('(주)', '')
                    except:
                        print(str_company1)
                        print(str_company2)
                        print(str_company3)
                        print(str_company)

                    # 채용공고 링크
                    str_title_link = base_link + elements.find('a', attrs={'class': 'data_layer'})['href']

                    # 회사 링크
                    str_company_link = base_link + elements.find('a', attrs={'class': 'track_event data_layer'})['href']

                    # Dictionary에 저장
                    if str_company in job_group:    # 회사명 - 기존에 있으면
                        for company in job_group[str_company]:
                            if company['title'] == str_title:    # 채용공고명 - 기존에 있으면
                                break
                        else:
                            job_group[str_company].append({'company': str_company, \
                                                        'title': str_title, \
                                                        'title_link': str_title_link, \
                                                        'company_link': str_company_link, \
                                                        'input_date': datetime.date.today().isoformat(), \
                                                        'status': 'wait'
                                                        })

                    else:    # 회사명 - 신규진입
                        job_group[str_company] = []
                        job_group[str_company].append({'company': str_company, \
                                                    'title': str_title, \
                                                    'title_link': str_title_link, \
                                                    'company_link': str_company_link, \
                                                    'input_date': datetime.date.today().isoformat(), \
                                                    'status': 'wait'
                                                    })

                    item_count += 1
                    
        print(f'{search_word}: {item_count}')
        
    return "DONE"


# JOB_GROUP 정보 획득 (길이)
@app.get("/return_info_len/")
def return_info_len():
    global job_group
    
    if len(job_group) == 0:
        load_json()

    print(len(job_group))
    return JSONResponse({
        'length': str(len(job_group))
    })


# JOB_GROUP 전체 정보 획득
@app.get("/return_info/")
def return_info():
    global job_group
    if len(job_group) == 0:
        load_json()

    return JSONResponse(job_group)


# 정보 업데이트 (SAVE, HOLD, CLOSE)
# http://127.0.0.1:8000/update_item/?str_company='삼성전자'&job_list=10&status=3
@app.get("/update_item/")
async def update_item(str_company: str='', job_list: int=0, status: int=0):
    global job_group
    if len(job_group) == 0:
        load_json()

    if status == 0:
        return 0
    elif status == 1:       # SAVE
        job_group[str_company][job_list]['status'] = 'save'
    elif status == 2:       # HOLD
        job_group[str_company][job_list]['status'] = 'hold'
    elif status == 3:       # CLOSE
        job_group[str_company][job_list]['status'] = 'close'
    else:
        return 0    
    save_json()
    return 1
    #return {"item_name": item.name, "item_id": item_id}



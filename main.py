from asyncio.windows_events import NULL
import requests
import json
import datetime
import urllib3

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
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()

origins = [
    "http://localhost.jeffrey.com",
    "https://localhost.jeffrey.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


job_group = {}

class Item(BaseModel):
    result_list : List[str] = []
    # name: str
    # job_list: float
    # status: None
    

@app.get("/")
def read_root():
    return {"Hello World"}


# JSON 파일 저장
@app.get("/save_json/")
def save_json():
    global job_group
    tf = open(file_path, 'w')
    json.dump(job_group, tf)
    tf.close()
    job_group = {}
    return "Done"
    
    
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
                                                        'title_idx' : len(job_group[str_company]), \
                                                        'title': str_title, \
                                                        'title_link': str_title_link, \
                                                        'company_link': str_company_link, \
                                                        'input_date': datetime.date.today().isoformat(), \
                                                        'status': 'wait'
                                                        })

                    else:    # 회사명 - 신규진입
                        job_group[str_company] = []
                        job_group[str_company].append({'company': str_company, \
                                                    'title_idx' : len(job_group[str_company]), \
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
async def return_info_len():
    global job_group
    
    if len(job_group) == 0:
        load_json()

    print(len(job_group))
    return str(len(job_group))
    # return JSONResponse({
    #     'length': str(len(job_group))
    # })


# JOB_GROUP 전체 정보 획득
# ALL   : 1
# WAIT  : 2
# SAVE  : 3
# HOLD  : 4
# CLOSE : 5

@app.get("/return_info_num/")
def return_info_num():
    global job_group
    if len(job_group) == 0:
        load_json()

    num_all = 0
    num_wait = 0
    num_save = 0
    num_hold = 0
    num_close = 0

    for companys in job_group:
        for idx, _ in enumerate(job_group[companys]):
            if job_group[companys][idx]['status'] == "wait":
                num_wait += 1
            elif job_group[companys][idx]['status'] == "save":
                num_save += 1
            elif job_group[companys][idx]['status'] == "hold":
                num_hold += 1
            elif job_group[companys][idx]['status'] == "close":
                num_close += 1
            num_all = num_wait + num_save + num_hold + num_close

    copy_group = {}
    copy_group['all'] = num_all
    copy_group['wait'] = num_wait
    copy_group['save'] = num_save
    copy_group['hold'] = num_hold
    copy_group['close'] = num_close
    
    return JSONResponse(copy_group)


@app.get("/return_info/")
def return_info(status: int=0):
    global job_group
    if len(job_group) == 0:
        load_json()

    copy_group = {}
    
    if status == 1:     str_status = 'all'
    elif status == 2:   str_status = 'wait'
    elif status == 3:   str_status = 'save'
    elif status == 4:   str_status = 'hold'
    elif status == 5:   str_status = 'close'
            
    if str_status == 'all':    # ALL
        print("return all")
        return JSONResponse(job_group)
        
    def filter_status_func():
        try:
            copy_group[companys].append(job_group[companys][idx])
        except:
            copy_group[companys] = []
            copy_group[companys].append(job_group[companys][idx])
    
    for companys in job_group:
        for idx, _ in enumerate(job_group[companys]):
            if job_group[companys][idx]['status'] == str_status:    # WAIT
                filter_status_func()
            elif job_group[companys][idx]['status'] == str_status:    # SAVE
                filter_status_func()
            elif job_group[companys][idx]['status'] == str_status:    # HOLD
                filter_status_func()
            elif job_group[companys][idx]['status'] == str_status:    # CLOSE
                filter_status_func()

    return JSONResponse(copy_group)


# 정보 업데이트 (SAVE, HOLD, CLOSE)
@app.get("/update_item/")
async def update_item(str_company: str='', job_list: int=0, status: int=0):
    global job_group
    if len(job_group) == 0:
        load_json()
    
    if status == 0:
        return 0
    elif status == 3:       # SAVE
        job_group[str_company][job_list]['status'] = 'save'
    elif status == 4:       # HOLD
        job_group[str_company][job_list]['status'] = 'hold'
    elif status == 5:       # CLOSE
        job_group[str_company][job_list]['status'] = 'close'
    else:
        return 0    
    save_json()
    return 1

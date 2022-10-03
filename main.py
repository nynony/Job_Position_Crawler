from asyncio.windows_events import NULL
import json
import urllib3

from config.assistant import *
from config.site_config import *

from fastapi import FastAPI
from pydantic import BaseModel

from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from typing import List

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
    load_json()

    num_all = 0
    num_wait = 0
    num_save = 0
    num_hold = 0
    num_close = 0
    company_count = 0

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
    print("---------- Return Info ----------")
    load_json()

    status_filter_group = {}

    if status == 1:     str_status = 'all'
    elif status == 2:   str_status = 'wait'
    elif status == 3:   str_status = 'save'
    elif status == 4:   str_status = 'hold'
    elif status == 5:   str_status = 'close'
            
    # 상단 ALL 버튼 클릭
    if str_status == 'all':
        return JSONResponse(job_group)
        
    def filter_status_func():
        try:
            status_filter_group[companys].append(job_group[companys][idx])
        except:
            status_filter_group[companys] = []
            status_filter_group[companys].append(job_group[companys][idx])

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

    # 포지션 누적 개수 추가
    for idx, corp_name in enumerate(status_filter_group):
        status_filter_group[corp_name][0]['company_count'] = len(job_group[corp_name])


    send_job_group = {}
    view_num = 15
    if status == 2 and len(status_filter_group) > view_num:
        for idx, corp_name in enumerate(status_filter_group):
            send_job_group[corp_name] = status_filter_group[corp_name]

            if idx == view_num:
                break

        return JSONResponse(send_job_group)
    else:
        
        return JSONResponse(status_filter_group)
    



# 정보 업데이트 (SAVE, HOLD, CLOSE)
@app.get("/update_item/")
def update_item(str_company: str='', job_list: int=0, status: int=0):
    print("---------- Update Item ----------")
    
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


# 정보 업데이트 (ALL CLOSE)
@app.get("/update_all_item/")
def update_item(str_company: str='', view_status: int=0):
    print("---------- Update All Item ----------")
    print(str_company)
    print(view_status)

    
    global job_group
    if len(job_group) == 0:
        load_json()
    
    if view_status == 2:
        str_view_status = 'wait'
    elif view_status == 3:
        str_view_status = 'save'
    elif view_status == 4:
        str_view_status = 'hold'
    
    for idx, _ in enumerate(job_group[str_company]):
        if job_group[str_company][idx]['status'] == str_view_status:
            job_group[str_company][idx]['status'] = 'close'

    save_json()
    return 1


# 회사 이름 Block
@app.get("/company_block/")
def company_block(str_company: str=''):
    print("---------- Company Block ----------")

    update_item(str_company)

    filter_list_company_name_path = "config/filter_list_company_name.txt"
    with open(filter_list_company_name_path, 'a', encoding="EUC-KR") as f:
        f.write(str_company+'\n')
    
    return 1

import calendar
import json
import logging
import random
import time
from functools import wraps

import requests

from SimpleError.error import SimpleError
from createSign.sign import create_sign
from decryptencrypt.encrypt import aes_encrypt
from textHandle.count import count_day

# info api log
logging.basicConfig(format="[%(asctime)s] %(name)s %(levelname)s: %(message)s", level=logging.INFO,
                    datefmt="%Y-%m-%d %I:%M:%S")
api_module_log = logging.getLogger("api_module")
headers = {
    'Host': 'api.moguding.net:9000',
    'accept-language': 'zh-CN,zh;q=0.8',
    'user-agent': 'Mozilla/5.0 (Linux; U; Android 9; zh-cn; SM-G977N Build/LMY48Z) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
    'authorization': "",
    'rolekey': "",
    'content-type': 'application/json; charset=UTF-8',
    'content-length': '161',
    'accept-encoding': 'gzip',
    'cache-control': 'no-cache'
}
# basic url
basic_url = "https://api.moguding.net:9000/"


# save token
def save_token(user_login_info):
    user_login_info.to_save_local(user_login_info.__dict__)


# repeat
def repeat_api(func):
    @wraps(func)
    def repeat(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except SimpleError as e:
            api_module_log.error(e)
            get_token_userid(*args, **kwargs)
            api_module_log.info('token 刷新成功')
            func(*args)

    return repeat


# login
def get_token_userid(user_info):
    url = 'session/user/v3/login'
    # param
    data = {"password": aes_encrypt(user_info.password), "loginType": "android",
            "t": aes_encrypt(int(time.time() * 1000)), "uuid": "", "phone": aes_encrypt(user_info.phone)}
    try:
        rsp = requests.post(headers=headers, url=basic_url + url, data=json.dumps(data)).json()
    except Exception as f:
        api_module_log.error(f)
        raise SimpleError("大概率ip被拉黑了(deny),当前环境可能存在问题(处于服务器上或开了代理,非国内代理)")
    data = rsp['data']
    user_info.token = data["token"]
    user_info.user_id = data['userId']


@repeat_api
# get plan
def get_plan(user_login_info) -> None:
    url = 'practice/plan/v3/getPlanByStu'
    # params
    data = {"state": ''}
    # add header
    headers['sign'] = create_sign(user_login_info.user_id, 'student')
    headers['authorization'] = user_login_info.token
    # return rsp
    rsp = requests.post(url=basic_url + url, headers=headers, data=json.dumps(data)).json()
    # check response
    handle_response(rsp)
    # response success
    plan_id = rsp["data"][0]['planId']
    user_login_info.plan_id = plan_id
    # save plan id
    user_login_info.to_save_local(user_login_info.__dict__)


@repeat_api
# clock in
def clock_in(user_login_info) -> None:
    url = 'attendence/clock/v2/save'
    # judge clock in
    now = time.strftime('%H', time.localtime())
    upload_type = "START"
    if now == user_login_info.start_time or now == user_login_info.end_time:
        upload_type = "START" if int(now) <= 12 else "END"
    else:
        api_module_log.info('未到打卡时间,已退出')
        return
        # exit(-1)
    api_module_log.info("开始打卡")
    # params
    data = {"device": "Android",
            "address": user_login_info.address,
            "t": aes_encrypt(int(time.time() * 1000)),
            "description": "",
            "country": "中国",
            "longitude": user_login_info.longitude,
            "city": user_login_info.city,
            "latitude": user_login_info.latitude,
            "planId": user_login_info.plan_id,
            "province": user_login_info.province,
            "type": upload_type}
    # change header
    # "Android" + state + plan_id + user_id + address
    headers['sign'] = create_sign("Android", upload_type, user_login_info.plan_id, user_login_info.user_id,
                                  user_login_info.address)
    headers['authorization'] = user_login_info.token
    rsp = requests.post(url=basic_url + url, headers=headers, data=json.dumps(data)).json()
    handle_response(rsp)
    # save token
    save_token(user_login_info)


@repeat_api
# repeat clock in
def repeat_clock_in(user_login_info, date):
    url = 'attendence/attendanceReplace/v2/save'
    data = {"device": "Android",
            "address": user_login_info.address,
            "t": aes_encrypt(int(time.time() * 1000)),
            "description": "",
            "country": "中国",
            "longitude": user_login_info.longitude,
            # no verify
            'createTime': f'{date} 0{random.randint(8, 9)}:{random.randint(10, 59)}:{random.randint(10, 59)}',
            "city": user_login_info.city,
            "latitude": user_login_info.latitude,
            "planId": user_login_info.plan_id,
            "province": user_login_info.province,
            "type": "START"}
    headers['sign'] = create_sign("Android", "START", user_login_info.plan_id, user_login_info.user_id,
                                  user_login_info.address)
    rsp = requests.post(basic_url + url, headers=headers, data=json.dumps(data)).json()
    handle_response(rsp)


@repeat_api
# get previous clock in log
def get_previous_month_data(user_login_info):
    year, now_month, now_day = [int(i) for i in time.strftime('%Y:%m:%d', time.localtime()).split(':')]
    url = 'attendence/clock/v1/listSynchro'
    api_module_log.info('获取上个月打卡日期')
    # handle year and month
    year = year if now_month != 1 else year - 1
    previous_month = now_month - 1 if now_month > 1 else 12
    previous_month_day_end = calendar.monthrange(year, previous_month)[1]
    previous_month_data = {"endTime": f"{year}-{previous_month}-{previous_month_day_end} 23:59:59",
                           "startTime": f"{year}-{previous_month}-1 00:00:00"}
    # sign exist
    if headers.get('sign'):
        headers.pop('sign')
    # update token
    headers['authorization'] = user_login_info.token
    rsp = requests.post(url=basic_url + url, headers=headers, data=json.dumps(previous_month_data)).json()
    handle_response(rsp)
    # clock in count
    day_set = count_day(rsp)
    # 上个月能打卡的天数
    previous_day = set([day for day in range(1, calendar.monthrange(year, previous_month)[1] + 1)][-(31 - now_day):])
    # 未打卡日期
    empty_day = []
    for day in previous_day:
        if day not in day_set:
            empty_day.append(day)
    api_module_log.info("上月补签阻塞3~15秒后打卡")
    for day in empty_day:
        time.sleep(random.randint(3, 15))
        api_module_log.info(f'补签:{previous_month}-{day}')
        repeat_clock_in(user_login_info, date=f"{year}-{previous_month}-{day}")
    api_module_log.info("上个月补签已完成")


@repeat_api
# get clock in log
def get_attendance_log(user_login_info):
    api_module_log.info("开始获取考勤记录")
    url = 'attendence/clock/v1/listSynchro'
    # get now month clock in  log
    year, now_month, now_day = [int(i) for i in time.strftime('%Y:%m:%d', time.localtime()).split(':')]
    now_month_day_end = calendar.monthrange(year, now_month)[1]
    data = {"endTime": f"{year}-{now_month}-{now_month_day_end} 23:59:59",
            "startTime": f"{year}-{now_month}-1 00:00:00"}
    # sign exist
    if headers.get('sign'):
        headers.pop('sign')
    # update token
    headers['authorization'] = user_login_info.token
    api_module_log.info("获取本月考勤日期")
    rsp = requests.post(url=basic_url + url, headers=headers, data=json.dumps(data)).json()
    handle_response(rsp)
    # save token
    save_token(user_login_info)
    # handle response text
    day_set = count_day(dict(rsp))
    empty_day = day_set ^ set(range(1, now_day))
    # repeat clock in
    api_module_log.info("本月补签阻塞3~15秒后打卡")
    for day in empty_day:
        time.sleep(random.randint(3, 15))
        api_module_log.info(f'补签:{now_month}-{day}')
        day = '0' + day if 10 > day else day
        repeat_clock_in(user_login_info, date=f'{year}-{now_month}-{day} ')
    # day > 30
    if 31 - now_day > 0:
        get_previous_month_data(user_login_info)
    # save token
    save_token(user_login_info)


# submit weekly
def submit_weekly(user_login_info):
    pass


@repeat_api
def submit_daily(user_login_info, daily):
    api_module_log.info('提交日报')
    url = 'practice/paper/v2/save'
    headers['sign'] = create_sign(user_login_info.user_id, "day", user_login_info.plan_id, "日报")
    data = {"yearmonth": "", "address": "", "t": aes_encrypt(int(time.time() * 1000)), "title": "日报",
            "longitude": "0.0",
            "latitude": "0.0", "planId": "5e4cda2cab725f3c60d46c2dae3740bd", "reportType": "day",
            "content": daily.get_daily()['data']}
    print(data)
    print('')
    rsp = requests.post()


# check response
def handle_response(rsp: dict) -> None:
    response_code = rsp['code']
    if response_code == 401:
        raise SimpleError(f"token expire {rsp}")
    elif response_code == 200:
        api_module_log.info(f"成功:{rsp}")
    else:
        api_module_log.info(f'请检测请求带的参数或发送issues 错误信息:{rsp}')
        api_module_log.info("其他错误,已退出")
        exit()

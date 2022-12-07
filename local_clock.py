import calendar
import copy
import hashlib
import json
import random
import time

import requests
from aes_pkcs5.algorithms.aes_ecb_pkcs5_padding import AESECBPKCS5Padding

"""
author:rsp
"""
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

with open('./basic_info/user.txt', 'r', encoding='utf-8') as f:
    user_info = f.read()
    user_info_json = json.loads(user_info)
    phone = user_info_json['phone']
    password = user_info_json['password']
    local_all = user_info_json["地址全称"]
    latitude = user_info_json["纬度"]
    longitude = user_info_json["经度"]
    start_time = user_info_json["start_time"]
    buqian = user_info_json["buqian"]
    requirement_week_num = user_info_json["requirement_week_num"]
    weekly = user_info_json["weekly"]
    remedy = user_info_json["remedy"]
    end_time = user_info_json["end_time"]
    province = local_all[:local_all.find('省') + 1]
    city = local_all[local_all.find('省') + 1:local_all.find('市') + 1]
print(phone, password, local_all, latitude, longitude, province, city, "\n早上打卡时间{}".format(start_time),
      "\n晚上打卡时间{}".format(end_time), "\n是缶提交周报{}".format(weekly))


def time_shift(date):
    """
    :param time:
    :return: 将时间转成时间戳
    """
    time_array = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def aes_encrypt(data):
    """
    :param data:
    :return: AES encrypt
    """
    key = '23DbtQHR2UMbH6mJ'
    encrypt_type = AESECBPKCS5Padding(key, "hex")
    text_encrypt = encrypt_type.encrypt(str(data))
    return text_encrypt


def md5_encrypt(data):
    """
    :param data:
    :return: md5
    """
    return hashlib.md5(data.encode("utf-8")).hexdigest()


def this_month_conunt(planid):
    """
    :param planid:
    :return: 未打卡的日期
    """
    # 深拷贝
    header = copy.deepcopy(headers)
    header.pop("sign")
    # 获取当前月的起始和结尾

    month = time.strftime("%Y-%m-", time.localtime())
    start_time = month + '01'
    print(month.split("-")[0])
    end_time = month + str(calendar.monthrange(int(month.split("-")[0]), int(month.split("-")[1]))[1])
    print(start_time, end_time)
    data = {
        "pageSize": "10",
        "planId": planid,
        "endTime": f"{end_time} 23:59:59",
        "startTime": f"{start_time} 00:00:00",
        "currPage": "1"
    }
    rsp = requests.post('https://api.moguding.net:9000/attendence/clock/v1/list', headers=headers,
                        data=json.dumps(data)).json()
    login = rsp["data"]
    clock_in_count = []
    for i in login:
        date = int(i["dateYmd"].split("-")[-1])
        if clock_in_count.count(date) > 0:
            continue
        else:
            clock_in_count.append(date)
    print(clock_in_count)
    day = int(time.strftime("%d", time.localtime()))
    not_clock_in_day = day - len(clock_in_count)
    print(time.strftime("%m", time.localtime()) + f"月您有{not_clock_in_day}天未签到")
    not_clock_in_date = [i for i in range(1, day + 1) if clock_in_count.count(i) == 0]
    try:
        # 去除今天
        not_clock_in_date.remove(day)
    except ValueError:
        pass
    return not_clock_in_date


def get_week_count(plan_id, user_id):
    """
    :param plan_id:
    :return: 提交周报次数
    """
    sign = md5_encrypt(user_id + 'studentweek' + "3478cbbc33f84bd00d75d7dfa69e0daa")
    headers.update({"sign": sign})
    data = {"reportType": "week", "currPage": "1", "pageSize": "10", "planId": plan_id}
    rsp = requests.post(url='https://api.moguding.net:9000/practice/paper/v2/listByStu', headers=headers,
                        data=json.dumps(data)).json()
    return int(rsp['flag'])


def get_weeks(plan_id):
    """
    获取去年该月到该月周的时间段
    :param plan_id:
    :return: 当前周和前19周的时间段
    """
    rsp = requests.post(url="https://api.moguding.net:9000" + '/practice/paper/v1/getWeeks1', headers=headers,
                        data=json.dumps({"planId": plan_id})).json()
    return rsp['data'][:20]


def submit_week(url, plan_id, user_id):
    """
    提交周报
    :param url:
    :param plan_id:
    :param user_id:
    :return:
    """
    # week_end = datetime.datetime.now()
    # week_start = (week_end - datetime.timedelta(days=6)).date()
    # 上面comment的为备用方案,防止API挂了
    weeks = get_weeks(plan_id)
    week_start = weeks[0]["startTime"]
    week_end = weeks[0]["endTime"]
    # # 已提交周报个数
    total = get_week_count(plan_id, user_id)
    # # 第几周的周报
    nowweek = total + 1
    with open(r'./basic_info/week_diary', 'r',
              encoding="utf-8") as f:
        text = f.read()
        division = text.split(',')
        content = json.loads(division[int(nowweek) - 1])["content"]
    data = {
        "yearmonth": "",
        "address": "",
        "t": aes_encrypt(int(str(time_shift(week_end)) + "000") - 3600),
        "title": "周报",
        "longitude": "0.0",
        "latitude": "0.0",
        "weeks": f'第{str(nowweek)}周',
        "endTime": f"{str(week_end)}",
        "startTime": f"{str(week_start)}",
        "planId": plan_id,
        "reportType": "week",
        "content": content
    }
    week_sign = user_id + "week" + plan_id + "周报" + "3478cbbc33f84bd00d75d7dfa69e0daa"
    if remedy:
        # 补交周报
        not_submit_week = weeks[:requirement_week_num + 1]
        not_submit_week.reverse()
        for i in not_submit_week:
            time.sleep(30)
            after_week = get_week_count(plan_id, user_id) + 1
            headers.update({'sign': md5_encrypt(week_sign)})
            week_end = i["endTime"]
            data["t"] = aes_encrypt(time_shift(week_end) - 36000 + 1000)
            data["startTime"] = i['startTime']
            data["endTime"] = week_end
            data["weeks"] = f'第{str(after_week)}周'
            data["content"] = json.loads(division[int(nowweek) - 1])["content"]
            rsp = requests.post(url="https://api.moguding.net:9000" + url, headers=headers, data=json.dumps(data))
            print(rsp.text)
    else:
        headers.update({'sign': md5_encrypt(week_sign)})
        print("开始写周报")
        rsp = requests.post(url="https://api.moguding.net:9000" + url, headers=headers, data=json.dumps(data))
        print(rsp.text)


def clock_in(url, plan_id, user_id, state):
    """
    阻塞10-30s后打卡
    """
    print('开始打卡')
    time.sleep(random.randint(10, 30))
    local_all = user_info_json["地址全称"]
    address = local_all
    province = local_all[:local_all.find('省') + 1]
    city = local_all[local_all.find('省') + 1:local_all.find('市') + 1]
    post_sign = "Android" + state + plan_id + user_id + address + "3478cbbc33f84bd00d75d7dfa69e0daa"
    headers.update({'sign': md5_encrypt(post_sign)})
    data2 = {"device": "Android", "address": address,
             "description": "", "country": "中国", "longitude": user_info_json["经度"], "city": city,
             "latitude": user_info_json["纬度"],
             "t": aes_encrypt(int(time.time() * 1000)),
             "planId": plan_id, "province": province, "type": state}
    if buqian:
        for i in this_month_conunt(plan_id):
            # 单数日期前面加0如09,08
            if i < 10:
                i = "0" + str(i)
            time.sleep(random.randint(20, 40))
            # 深copy 不影响正常打卡
            buqian_data = copy.deepcopy(data2)
            buqian_data.update({"createTime": f'{time.strftime(f"%Y-%m-{i} %H:%M:%S", time.localtime())}'})
            # buqian_data.update({"createTime": f'2022-10-01 08:25:55'})
            rsp = requests.post(url="https://api.moguding.net:9000/attendence/attendanceReplace/v2/save",
                                headers=headers, data=json.dumps(buqian_data))
            print(rsp.text)
    rsp = requests.post(url="https://api.moguding.net:9000/" + url, headers=headers, data=json.dumps(data2))
    print(rsp.text)
    if weekly:
        submit_week("/practice/paper/v2/save", plan_id, user_id)


def get_plan(url, user_id):
    data = {
        'state': ''
    }
    rsp = requests.post(url="https://api.moguding.net:9000/" + url, headers=headers, data=json.dumps(data)).json()
    if rsp.get("code") > 400:
        print(rsp)
    data = rsp["data"][0]
    plan_id = data["planId"]
    # 早晚打卡,判断是否为设置的打卡时间
    if time.strftime("%H", time.localtime()) == start_time:
        clock_in("attendence/clock/v2/save", plan_id, user_id, "START")
    elif time.strftime("%H", time.localtime()) == end_time:
        clock_in("attendence/clock/v2/save", plan_id, user_id, "END")
    else:
        print("还没到打卡时间,请修改配置参数")


def save_token():
    """
    将token和userid存到配置文件中
    :return:
    """
    with open("./basic_info/user.txt", 'w', encoding="utf-8") as file:
        file.write(json.dumps(user_info_json))


def main(log_url):
    auto_login = user_info_json.get("token")
    if not auto_login:
        # 请求体
        print('手动登录')
        data = {
            "phone": aes_encrypt(phone),
            "password": aes_encrypt(password),
            "t": aes_encrypt(int(time.time() * 1000)),
            "loginType": "android",
            "uuid": "",
        }
        rsp = requests.post(url=log_url, headers=headers, data=json.dumps(data)).json()
        data = rsp["data"]
        token = data["token"]
        user_id = data["userId"]
        user_info_json.setdefault("token", token)
        user_info_json.setdefault("user_id", user_id)
        # 保存token
        save_token()
        plan_sign = user_id + "student" + "3478cbbc33f84bd00d75d7dfa69e0daa"
        headers.update({"authorization": token, "rolekey": "student", 'sign': md5_encrypt(plan_sign)})
        get_plan('practice/plan/v3/getPlanByStu', user_id)
    else:
        # 提取userid 加密sign
        print('自动登录')
        user_id = user_info_json["user_id"]
        plan_sign = user_id + "student" + "3478cbbc33f84bd00d75d7dfa69e0daa"
        headers.update({"authorization": user_info_json["token"], "rolekey": "student", 'sign': md5_encrypt(plan_sign)})
        try:
            get_plan('practice/plan/v3/getPlanByStu', user_id)
        except Exception:
            user_info_json.pop("token")
            main(url)


if __name__ == '__main__':
    url = 'https://api.moguding.net:9000/session/user/v3/login'
    main(url)

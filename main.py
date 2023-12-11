import json
import logging
import os
import time

from api.api_all import get_token_userid, get_plan, clock_in, get_attendance_log, submit_daily, get_weeks_date, \
    submit_weekly, submit_log, submit_month_report
from config.info import Info
from textHandle.get_daily import Daily
from textHandle.get_month_report import MonthReport
from textHandle.get_weekly import Weekly
from textHandle.handle_weeks_date import WeeksDate
from textHandle.submitTime import SubmitTime
from util.tomorrow import tomorrow_1_clock, next_week_submit_time,next_submit_month_time

# print log config
logging.basicConfig(format="[%(asctime)s] %(name)s %(levelname)s: %(message)s", level=logging.INFO,
                    datefmt="%Y-%m-%d %I:%M:%S")
main_module_log = logging.getLogger("main_module")
# user config file place
config_file = "./user_config.json"
path = os.path.dirname(__file__)


# get daily file
def load_daily_file() -> Daily:
    with open(os.path.join(path, r'textFile\daily.json'), 'r', encoding="UTF-8") as f:
        daily = json.load(f)
    return Daily(daily)


# load local file
def load_weekly_file() -> Weekly:
    with open(os.path.join(path, 'textFile/weekly.json'), 'r', encoding="UTf-8") as f:
        weekly = json.load(f)
    return Weekly(weekly)


# load local file
def load_month_report() -> MonthReport:
    with open(os.path.join(path, 'textFile/month_report.json'), 'r', encoding="UTf-8") as f:
        return MonthReport(json.load(f))


# load login info
def load_login_info() -> Info:
    with open(config_file, encoding="utf-8") as f:
        user_info = json.load(f)
    return Info(user_info, os.path.join(path, 'user_config.json'))


def login(user_login_info: Info) -> None:
    # exist token
    if not user_login_info.token:
        main_module_log.info("获取 token")
        get_token_userid(user_login_info)
        # save token user_id
        user_login_info.to_save_local(user_login_info.__dict__)
        main_module_log.info("登录成功")
    else:
        main_module_log.info("使用本地token")


# get plan
def plan_id(user_login_info: Info) -> None:
    # get plan
    if not user_login_info.plan_id:
        main_module_log.info("获取plan id")
        get_plan(user_login_info)
    else:
        main_module_log.info("使用本地plan id")


def load_weeks_info(data) -> WeeksDate:
    return WeeksDate(data)


def run():
    main_module_log.info('检测配置文件')
    # get user login info
    user_login_info = load_login_info()
    # login
    main_module_log.info("开始登录")
    login(user_login_info)
    # get plan_id
    plan_id(user_login_info)
    # get submit log
    main_module_log.info('获取提交记录')
    submit_all = submit_log(user_login_info)
    # clock in
    main_module_log.info("启动打卡")
    clock_in(user_login_info)
    # repeat clock in
    if user_login_info.is_repeat_clock_in:
        main_module_log.info("开始补签")
        get_attendance_log(user_login_info)
    # get local file
    # get submit time
    submit_time = SubmitTime(path)
    # submit daily
    if user_login_info.is_submit_daily:
        main_module_log.info("判断今天是否提交日报")
        if not submit_time.daily_next_submit_Time or int(time.time()) > submit_time.daily_next_submit_Time:
            main_module_log.info('载入日报文件')
            daily = load_daily_file()
            main_module_log.info('载入成功')
            main_module_log.info("提交日报")
            submit_daily(user_login_info, daily=daily, day=submit_all['dayReportNum'])
            # set next submit time
            submit_time.daily_next_submit_Time = tomorrow_1_clock()
            submit_time.to_save_local()
        else:
            main_module_log.error("今天已提交日报了,不会重复提交")

    # submit weekly
    # is user config week
    now_week = int(time.strftime("%w", time.localtime()))
    now_week = now_week if now_week != 0 else 7
    if now_week == user_login_info.submit_weekly_time:
        if user_login_info.is_submit_weekly:
            main_module_log.info('判断今天是否提交过周报')
            if not submit_time.weekly_next_submit_Time or int(time.time()) > submit_time.weekly_next_submit_Time:
                weeks_dict = get_weeks_date(user_login_info)
                weeks_date = load_weeks_info(weeks_dict)
                now_week = weeks_date.get_now_week_date()
                main_module_log.info("从本地文件获取周报")
                weekly = load_weekly_file()
                main_module_log.info("开始提交周报")
                #
                weeks = submit_all['weekReportNum']
                main_module_log.info(f'提交第{weeks}周周报')
                # add weeks
                now_week['weeks'] = weeks
                submit_weekly(user_login_info, week=now_week, weekly=weekly.get_now_weekly(weeks))
                # set next submit time
                submit_time.weekly_next_submit_Time = next_week_submit_time()
                submit_time.to_save_local()
            else:
                main_module_log.error('已提交周报，不会重复提交')
    else:
        main_module_log.info("未到提交周报时间")
    # submit month report
    date = time.localtime()
    day = date.tm_mday
    # is user set time
    if day == user_login_info.submit_month_report_time:
        # is submit month report
        if submit_time.month_next_submit_Report == "" or int(time.time()) > submit_time.month_next_submit_Report:
            main_module_log.info('读取月报内容.....')
            month_report = load_month_report()
            main_module_log.info("开始提交月报")
            submit_month_report(user_login_info, date=date, month_report=month_report.get_month_report())
            submit_time.month_next_submit_Report = next_submit_month_time()
            # sava local file
            submit_time.to_save_local()
        else:
            main_module_log.info('今天已提交月报,不在重复提交')

    else:
        main_module_log.info("未到提交月报时间")


if __name__ == '__main__':
    main_module_log.info("开始")
    run()

import json
import logging
import os

from api.api_all import get_token_userid, get_plan, clock_in, get_attendance_log
from config.info import Info

# print log config
logging.basicConfig(format="[%(asctime)s] %(name)s %(levelname)s: %(message)s", level=logging.INFO,
                    datefmt="%Y-%m-%d %I:%M:%S")
main_module_log = logging.getLogger("main_module")
# user config file place
config_file = "./user_config.json"
path = os.path.dirname(__file__)


# get info login info
def load_login_info() -> Info:
    with open(config_file, encoding="utf-8") as f:
        user_info = json.load(f)
    return Info(user_info, os.path.join(path, 'user_config.json'))


# save token
def save_token_user_id(config: Info, token: str, user_id) -> None:
    config.token = token
    config.user_id = user_id
    with open(config_file, 'w', encoding="UTF_8") as f:
        f.write(str(json.dumps(config.__dict__)))


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


def plan_id(user_login_info: Info) -> None:
    # get plan
    if not user_login_info.plan_id:
        main_module_log.info("获取plan id")
        get_plan(user_login_info)
    else:
        main_module_log.info("使用本地plan id")


def run():
    main_module_log.info('检测配置文件')
    # get user login info
    user_login_info = load_login_info()
    # login
    main_module_log.info("开始登录")
    login(user_login_info)
    # get plan_id
    plan_id(user_login_info)
    # clock in
    clock_in(user_login_info)
    # repeat clock in
    main_module_log.info("开始补签")
    get_attendance_log(user_login_info)


if __name__ == '__main__':
    main_module_log.info("开始")
    run()

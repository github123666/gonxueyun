import json
import logging

# log basic
logging.basicConfig(format="[%(asctime)s] %(name)s %(levelname)s: %(message)s", level=logging.INFO,
                    datefmt="%Y-%m-%d %I:%M:%S")
config_module_log = logging.getLogger("User_config")


class Info:

    def __init__(self, login_info, path):
        self.password = login_info.get("password").strip()
        try:
            self.phone = login_info.get("phone").strip()
            int(self.phone)
        except Exception as f:
            config_module_log.info("手机号格式错误(带有非数字)")
            config_module_log.error(f)
            exit(-1)
        self.address = login_info["address"]
        self.latitude = login_info["latitude"]
        self.longitude = login_info['longitude']
        self.start_time = login_info['start_time']
        self.end_time = login_info["end_time"]
        self.token = login_info.get("token")
        self.user_id = login_info.get("user_id")
        self.plan_id = login_info.get("plan_id")
        self.city = login_info['city']
        self.province = login_info['province']
        self.path = path

    def __str__(self):
        return "user config"

    # save local
    def to_save_local(self, arg: dict):
        with open(self.path, 'w', encoding="UTF_8") as f:
            f.write(str(json.dumps(arg)))

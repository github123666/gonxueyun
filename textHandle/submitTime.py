import json
import os


class SubmitTime:
    def __str__(self):
        return "submit log"

    def __init__(self, path):
        self.path = os.path.join(path, 'textFile/submit_time.json')
        with open(self.path, 'r', encoding="UTF-8") as f:
            self.submit_time = json.load(f)
        self.daily_next_submit_Time = self.submit_time['daily_next_submit_Time']
        self.weekly_next_submit_Time = self.submit_time['weekly_next_submit_Time']
        self.month_next_submit_Report = self.submit_time['month_next_submit_Report']

    def to_save_local(self):
        with open(self.path, 'w', encoding="UTF-8") as f:
            f.write(str(self.__dict__))

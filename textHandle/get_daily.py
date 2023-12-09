import random


class Daily:
    def __init__(self, daily: dict):
        self.daily = daily

    def __str__(self):
        return "handler daily"

    def get_daily(self):
        return random.choice(self.daily)

import random


class MonthReport:
    def __str__(self):
        return "month content"

    def __init__(self, month_report: list):
        self.month_report = month_report

    def get_month_report(self) -> str:
        return random.choice(self.month_report)['content']

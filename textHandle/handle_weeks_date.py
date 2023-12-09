class WeeksDate:
    def __init__(self, weeks_date: dict):
        self.weeks_date = weeks_date

    def __str__(self):
        return 'weeks date'

    # get now week date
    def get_now_week_date(self):
        return self.weeks_date['data'][0]

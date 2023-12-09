class Weekly:
    def __str__(self):
        return "weekly"

    def __init__(self, weeks: dict):
        self.weeks = weeks

    def get_now_weekly(self, number: int):
        return self.weeks[number]['content']

from datetime import datetime


class User:
    def __init__(self, user_id, name,
                 first_date=datetime.today().strftime("%H.%M.%S-%Y-%m-%d"),
                 last_date=datetime.today().strftime("%H.%M.%S-%Y-%m-%d"),
                 use_count=1):
        self.id = user_id
        self.firstName = name
        self.last_date = last_date
        self.first_date = first_date
        self.use = int(use_count)

    def increase_actions(self):  # add_use
        self.use += 1

    def __str__(self):
        return f"{self.id} | {self.firstName} | {self.first_date} | {self.last_date} | {self.use}"

    def __repr__(self):
        return f"{self.id} | {self.firstName} | {self.first_date} | {self.last_date} | {self.use}"

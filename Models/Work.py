import datetime


class Work:
    def __init__(self):
        self.task_id = None
        self.work_id = None
        self.start_time = None
        self.end_time = None
        self.employee = 'John Doe'

    def add_start(self, time):
        self.start_time = time

    def add_end(self, time):
        self.end_time = time;

    def get_time(self):
        return datetime.timedelta(self.end_time, self.start_time)

    def serialize(self):
        return {
            'task_id': self.task_id,
            'work_id': self.work_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'employee': self.employee
        }

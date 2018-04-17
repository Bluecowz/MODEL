
class Customer:
    def __init__(self, name='name', task_count=0):
        self.name = name
        self.task_count = task_count
        self.rank = 3

    def add_task(self):
        self.task_count = self.task_count + 1
        if self.task_count >= 5:
            self.rank = 1
        elif self.task_count >= 3:
            self.rank = 2

    def serialize(self):
        return {
            'name': self.name,
            'task_count': self.task_count,
            'rank': self.rank
        }

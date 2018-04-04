
class Customer:
    def __init__(self, name='name', task_count=0):
        self.name = name
        self.task_count = task_count

    def serialize(self):
        return {
            'name': self.name,
            'task_count': self.task_count
        }

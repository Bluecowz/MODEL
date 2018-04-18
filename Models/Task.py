class Task:

    def __init__(self):
        self.ID = None
        self.company = None
        self.work = list()
        self.rank = 3
        self.posted = None
        self.est_hrs = None

    def set_company(self, company):
        self.company = company
        self.rank = self.company.rank

    def set_rank(self, rank):
        self.rank = rank

    def add_work(self, work):
        self.work.append(work)

    def total_work(self):
        time = 0
        for derp in self.work:
            time = time + derp.get_time()
        return time

    def serialize(self):
        derp = '{ '
        for x in self.work:
            derp = derp + str(x.serialize()) + ','
        derp = derp + '}'
        return {
            'id': self.ID,
            'company': self.company.serialize(),
            'rank': self.rank,
            'posted': self.posted,
            'work': derp,
            'est-hrs': self.est_hrs
        }

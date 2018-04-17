from datetime import datetime, timedelta


class Performance:
    def __init__(self):
        self.stats = list()
        self.start_time = datetime.now()

    def start(self):
        self.start_time = datetime.now()

    def end(self, call_name):
        total = datetime.now() - self.start_time
        self.stats.append((call_name, total))

    def serialize_stats(self):
        most = self.stats[0]
        least = self.stats[0]
        total = timedelta(0)
        count = 0
        for x in self.stats:
            if x[1] < least[1]:
                least = x
            elif x[1] > most[1]:
                most = x
            total = total + x[1]
            count = count + 1

        most = (most[0], most[1].total_seconds())
        least = (least[0], least[1].total_seconds())
        return {
            "longest": most,
            "fastest": least,
            "average": (total.total_seconds()/count),
            "total": len(self.stats)
        }




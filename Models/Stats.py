from datetime import datetime, timedelta


class Stats:
    @staticmethod
    def get_stats(tasks, work):
        tasks_added = list()
        work_added = list()
        hours_completed = 0
        for x in tasks:
            if (datetime.now() - x.posted) >= timedelta(days=-30):
                tasks_added.append(x)
        for x in work:
            if (datetime.now() - x.start_time) >= timedelta(days=-30):
                work_added.append(x)
        for x in work:
            if x.end_time is not None:
                if (datetime.now() - x.end_time) >= timedelta(days=-30):
                    if x.end_time is not None:
                        hours_completed = hours_completed + ((x.end_time - x.start_time).total_seconds())/60/60
        return {
            "tasks_added": len(tasks_added),
            "work_added": len(work_added),
            "hours": hours_completed
        }



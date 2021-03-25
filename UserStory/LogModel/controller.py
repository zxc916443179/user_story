from .models import Log
import time
class LogController:
    @staticmethod
    def add_log(username, startTime, endTime, url):
        t = int(time.time())
        log = Log()
        log.dateTime = t
        log.username = username
        log.startTime = startTime
        log.endTime = endTime
        log.url = url
        log.save()
        return log
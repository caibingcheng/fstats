import psutil
import time

class LiveTime():
    def __init__(self, *timer):
        self._day, self._hour, self._min, self._second = timer

    @property
    def day(self):
        return self._day
    @property
    def hour(self):
        return self._hour
    @property
    def min(self):
        return self._min
    @property
    def second(self):
        return self._second

    def __str__(self):
        if self._day < 1:
            return '{:>2}h {:>2}m'.format(int(self._hour), int(self._min))
        else:
            return '{:>2}d {:>2}h'.format(int(self._day), int(self._hour))

def info():
    upSecond = time.time() - psutil.boot_time()
    upDay = upSecond / 86400
    upSecond %= 86400
    upHour = upSecond / 3600
    upSecond %= 3600
    upMin = upSecond / 60
    upSecond %= 60
    live = LiveTime(upDay, upHour, upMin, upSecond)
    return live
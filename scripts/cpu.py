
import psutil

def info():
    return psutil.cpu_percent(interval=1)
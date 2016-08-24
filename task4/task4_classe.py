#!/usr/bin/python
import configparser
import datetime
import json
import psutil
import schedule
import time


snapshotn = 0
conf = configparser.ConfigParser()
conf.read('conf.ini')
output = conf.get('common', 'output')
intervalt = conf.get('common', 'interval')


class ParentClass(object):
    @staticmethod
    def variables(self):
        global snapshotn
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        mem = (psutil.virtual_memory().total / (1024 * 1024)).__round__(2)
        mem_available = (psutil.virtual_memory().available / (1024 * 1024)).__round__(2)
        mem_used = (psutil.virtual_memory().used / (1024 * 1024)).__round__(2)
        mem_percent = psutil.virtual_memory().percent
        mem_swap = (psutil.swap_memory().total / (1024 * 1024)).__round__(2)
        mem_swap_p = psutil.swap_memory().percent
        cpu_percent = psutil.cpu_percent(interval=0.5, percpu=False)
        disk_counters = psutil.disk_io_counters()[8]
        net_count_sent = (psutil.net_io_counters(pernic=False)[0] / (1024 * 1024)).__round__(2)
        net_count_received = (psutil.net_io_counters(pernic=False)[1] / (1024 * 1024)).__round__(2)
        return timestamp, mem, mem_available, mem_used, mem_percent, mem_swap, mem_swap_p, cpu_percent, disk_counters, net_count_sent, net_count_received


class FunctionLog(ParentClass):
    def log(self):
        global snapshotn
        snapshotn += 1
        flog = open('log.txt', 'a+')
        flog.write("snapshot " + str(snapshotn) + ": " + ParentClass.variables(self)[0] + '\n')
        flog.write(str(ParentClass.variables(self)[1]) + "mb total memory count" + '\n')
        flog.write(str(ParentClass.variables(self)[2]) + "mb available memory" + '\n')
        flog.write(str(ParentClass.variables(self)[3]) + "mb used RAM" + '\n')
        flog.write(str(ParentClass.variables(self)[4]) + "% used memory, %" + '\n')
        flog.write(str(ParentClass.variables(self)[5]) + "mb swap memory total" + '\n')
        flog.write(str(ParentClass.variables(self)[6]) + "% swap memory usage" + '\n')
        flog.write(str(ParentClass.variables(self)[7]) + "% of CPU load" + '\n')
        flog.write(str(ParentClass.variables(self)[8]) + "disk time usage in milliseconds" + '\n')
        flog.write(str(ParentClass.variables(self)[9]) + "mb sent via all interfaces" + '\n')
        flog.write(str(ParentClass.variables(self)[10]) + "mb received via all interfaces" + '\n')
        flog.write('\n')
        flog.close()


def log2():
    global snapshotn
    snapshotn += 1
    timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    snapshot = {
        '% of CPU load': psutil.cpu_percent(interval=0.2, percpu=False),
        'mb of total memory count': (psutil.virtual_memory().total / (1024 * 1024)).__round__(2),
        'mb available memory': (psutil.virtual_memory().available / (1024 * 1024)).__round__(2),
        'mb used RAM': (psutil.virtual_memory().used / (1024 * 1024)).__round__(2),
        'used memory, %': psutil.virtual_memory().percent,
        'mb swap memory total': (psutil.swap_memory().total / (1024 * 1024)).__round__(2),
        '% swap memory usage': psutil.swap_memory().percent,
        'disk time usage in milliseconds': psutil.disk_io_counters()[8],
        'mb sent via all interfaces': (psutil.net_io_counters(pernic=False)[0] / (1024 * 1024)).__round__(2),
        'mb received via all interfaces': (psutil.net_io_counters(pernic=False)[1] / (1024 * 1024)).__round__(2)
    }
    data = ['SNAPSHOT' + str(snapshotn) + ": " + str(timestamp) + ": ", snapshot]
    with open("log.json", "a") as f:
        json.dump(data, f, indent=3, sort_keys=True)


myclass1 = FunctionLog()


def start_fun():
    global intervalt
    if output == 'txt':
        myclass1.log()
    elif output == 'json':
        log2()

schedule.every(int(intervalt)).seconds.do(start_fun)
while True:
    schedule.run_pending()
    time.sleep(0)
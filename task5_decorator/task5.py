#!/usr/bin/python
import configparser
import datetime
import json
import psutil
import schedule


snapshotn = 0
conf = configparser.ConfigParser()
conf.read('conf.ini')
output = conf.get('common', 'output')
intervalt = conf.get('common', 'interval')
wrapper_state = conf.get('common', 'wrapper')


def trace(func):
    def inner(*args, **kwargs):
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        file_wrap = open('wrapper', 'a+')
        file_wrap.write('At ' + timestamp + ' start ' + func.__name__ + str(args) + '\n')
        file_wrap.write("END" '\n')
        file_wrap.write('\n')
        func(*args, **kwargs)
        file_wrap.write(func.__name__ + str(args) + '\n')
        file_wrap.close()
    return inner if wrapper_state else func


class ParentClass:
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


class FunctionLog(ParentClass):
    @trace
    def log(self):
        global snapshotn
        snapshotn += 1
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        flog = open('log.txt', 'a+')
        flog.write("snapshot " + str(snapshotn) + ": " + timestamp + '\n')
        flog.write(str(ParentClass.mem) + "mb total memory count" + '\n')
        flog.write(str(ParentClass.mem_available) + "mb available memory" + '\n')
        flog.write(str(ParentClass.mem_used) + "mb used RAM" + '\n')
        flog.write(str(ParentClass.mem_percent) + "% used memory, %" + '\n')
        flog.write(str(ParentClass.mem_swap) + "mb swap memory total" + '\n')
        flog.write(str(ParentClass.mem_swap_p) + "% swap memory usage" + '\n')
        flog.write(str(ParentClass.cpu_percent) + "% of CPU load" + '\n')
        flog.write(str(ParentClass.disk_counters) + "disk time usage in milliseconds" + '\n')
        flog.write(str(ParentClass.net_count_sent) + "mb sent via all interfaces" + '\n')
        flog.write(str(ParentClass.net_count_received) + "mb received via all interfaces" + '\n')
        flog.write('\n')
        flog.close()


class FunctionJson(ParentClass):
    @trace
    def log2(self):
        global snapshotn
        snapshotn += 1
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        snapshot = {
            '% of CPU load': ParentClass.cpu_percent,
            'mb of total memory count': ParentClass.mem,
            'mb available memory': ParentClass.mem_available,
            'mb used RAM': ParentClass.mem_used,
            'used memory, %': ParentClass.mem_percent,
            'mb swap memory total': ParentClass.mem_swap,
            '% swap memory usage': ParentClass.mem_swap_p,
            'disk time usage in milliseconds': ParentClass.disk_counters,
            'mb sent via all interfaces': ParentClass.net_count_sent,
            'mb received via all interfaces': ParentClass.net_count_received
        }
        data = ['SNAPSHOT' + str(snapshotn) + ": " + str(timestamp) + ": ", snapshot]
        with open("log.json", "a") as f:
            json.dump(data, f, indent=3, sort_keys=True)


myclass1 = FunctionLog()
myclass2 = FunctionJson()


def start_fun():
    global intervalt
    if output == 'txt':
        myclass1.log()
    elif output == 'json':
        myclass2.log2()

schedule.every(int(intervalt)).seconds.do(start_fun)
while True:
    schedule.run_pending()

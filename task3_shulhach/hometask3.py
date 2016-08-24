#!/usr/bin/python
import psutil
import datetime
import time
import json
import configparser
import schedule

snapshotn = 0
conf = configparser.ConfigParser()
conf.read('conf.ini')
output = conf.get('common', 'output')
intervalt = conf.get('common', 'interval')


def log():
    global snapshotn
    snapshotn +=1
    timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    mem = psutil.virtual_memory().total/(1024*1024)
    b = psutil.virtual_memory().available/(1024*1024)
    c = psutil.virtual_memory().used/(1024*1024)
    d = psutil.virtual_memory().percent
    e = psutil.swap_memory().total/(1024*1024)
    f = psutil.swap_memory().percent
    i = psutil.cpu_percent(interval=0.2, percpu=False)
    g = psutil.disk_io_counters()[8]
    h = psutil.net_io_counters(pernic=False)[0]/(1024*1024)
    j = psutil.net_io_counters(pernic=False)[1]/(1024*1024)
    flog = open('log.txt','a+')
    flog.write("snapshot "+str(snapshotn)+": "+timestamp+'\n')
    flog.write(str(mem.__round__(2))+"mb total memory count"+'\n')
    flog.write(str(b.__round__(2))+"mb available memory"+'\n')
    flog.write(str(c.__round__(2))+"mb used RAM"+'\n')
    flog.write(str(d)+"% used memory, %"+'\n')
    flog.write(str(e.__round__(2))+"mb swap memory total"+'\n')
    flog.write(str(f)+"% swap memory usage"+'\n')
    flog.write(str(i)+"% of CPU load"+'\n')
    flog.write(str(g)+"disk time usage in milliseconds"+'\n')
    flog.write(str(h.__round__(2))+"mb sent via all interfaces"+'\n')
    flog.write(str(j.__round__(2))+"mb received via all interfaces"+'\n')
    flog.write('\n')
    flog.close()


def log2():
    global snapshotn
    snapshotn += 1
    timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    snapshot = {
        '% of CPU load': psutil.cpu_percent(interval=0.2, percpu=False),
        'mb of total memory count': (psutil.virtual_memory().total/(1024*1024)).__round__(2),
        'mb available memory': (psutil.virtual_memory().available/(1024*1024)).__round__(2),
        'mb used RAM': (psutil.virtual_memory().used/(1024*1024)).__round__(2),
        'used memory, %': psutil.virtual_memory().percent,
        'mb swap memory total': (psutil.swap_memory().total/(1024*1024)).__round__(2),
        '% swap memory usage': psutil.swap_memory().percent,
        'disk time usage in milliseconds': psutil.disk_io_counters()[8],
        'mb sent via all interfaces': (psutil.net_io_counters(pernic=False)[0]/(1024*1024)).__round__(2),
        'mb received via all interfaces': (psutil.net_io_counters(pernic=False)[1]/(1024*1024)).__round__(2)
            }
    data = ['SNAPSHOT' + str(snapshotn) + ": " + str(timestamp) + ": ", snapshot]
    with open("log.json", "a") as f:
        json.dump(data, f, indent=3, sort_keys=True)


def shedule():
    global intervalt
    if output == 'txt':
        schedule.every(int(intervalt)).seconds.do(log)
    elif output == 'json':
        schedule.every(int(intervalt)).seconds.do(log2)
    while True:
        schedule.run_pending()
        time.sleep(1)
shedule()

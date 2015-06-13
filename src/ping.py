import sys
from datetime import datetime, timedelta
from random import randint
from scapy.all import *
import numpy
import time

class Ping:
    def __init__(self, ip, alpha, timeout): 
        self.ip = ip
        self.alpha = alpha
        self.icmp_id = random.randint(0,65535)
        self.timeout = timeout

    def times(self, an_amount):
        statistics = Statistics(self.ip, self.alpha)

        for i in range(1, an_amount+1):
            packet = IP(dst=self.ip) / ICMP(id=self.icmp_id, seq=i)
            response = sr1(packet, timeout = self.timeout, verbose=False)

            print 'Ping: ' + str(i)

            if response is None:
                statistics.ping_failed()
            else:
                ellapsed = response.time - packet.time
                statistics.ping_succeeded(ellapsed)

            self.icmp_id = (self.icmp_id + 1) % 65535
    
        return statistics

class Statistics:
    def __init__(self, ip, alpha):
        self.ip = ip
        self.alpha = alpha
        self.failed_count = 0
        self.succeeded_count = 0
        self.ertt = -1

    def ping_failed(self):
        self.failed_count += 1

    def ping_succeeded(self, ellapsed):
        self.succeeded_count += 1
        self.update_ertt(ellapsed)

    def update_ertt(self, ellapsed):
        if self.succeeded_count > 1:
            self.ertt = self.alpha * self.ertt + (1 - self.alpha) * ellapsed
        else:
            self.ertt = ellapsed

    def loss_probability(self):
        return float(self.failed_count) / float(self.total()) 
    
    def total(self):
        return self.succeeded_count + self.failed_count

    def output(self):
        print 'ip: ' + str(self.ip)
        print '\talpha: ' + str(self.alpha) + '\ttotal: '  + str(self.total())
        print '\tfailed: ' + str(self.failed_count) + '\tsucceeded: ' + str(self.succeeded_count) + '\tlossProbability ' + str(self.loss_probability())
        print '\testimated rtt: ' + str(self.ertt)

if (len(sys.argv) < 4):
    print 'Usage: python ej3.py [ip] [alpha] [count] [timeout]'
else:
    ip_dst = (sys.argv[1])
    alpha = float(sys.argv[2])
    count = int(sys.argv[3])
    timeout = float(sys.argv[4])
    ping = Ping(ip_dst, alpha, timeout)
    statistics = ping.times(count)
    statistics.output()


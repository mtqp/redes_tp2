import sys
from datetime import datetime, timedelta
import math
from random import randint
from scapy.all import *
import numpy
import time

class Ping:
    def __init__(self, ip, alpha_pace, count_pace, timeout): 
        self.ip = ip
        self.icmp_id = random.randint(0,65535)
        self.timeout = timeout
        self.statistics = self.create_statistics(alpha_pace, count_pace)

    def do(self):
        for i in range(1, 151):
            packet = IP(dst=self.ip) / ICMP(id=self.icmp_id, seq=i)
            response = sr1(packet, timeout = self.timeout, verbose=False)

            if response is None:
                self.ping_failed(i)                
            else:
                ellapsed = response.time - packet.time
                self.ping_succeeded(ellapsed, i)

            self.icmp_id = (self.icmp_id + 1) % 65535
    
        return self.statistics

    def ping_failed(self, i):
        for statistic in self.statistics:
            statistic.ping_failed(i)

    def ping_succeeded(self, ellapsed, i):
        for statistic in self.statistics:
            statistic.ping_succeeded(ellapsed, i)

    def create_statistics(self, alpha_pace, count_pace):
        statistics = []
        alphas = self.alphas(alpha_pace)
        counts = self.counts(count_pace)
        for alpha in alphas:
            for count in counts:
                statistics.append(Statistic(self.ip, alpha, count))
        return statistics

    def alphas(self, alpha_pace):
        return numbers(0.8, 1.0, alpha_pace)

    def counts(self, count_pace):
        return numbers(10,150, count_pace)

class Statistic:
    def __init__(self, ip, alpha, max_count):
        self.ip = ip
        self.alpha = alpha
        self.max_count = max_count
        self.failed_count = 0
        self.succeeded_count = 0
        self.ertt = -1
        self.two_thirds = 2.0/3.0

    def ping_failed(self, i):
        if i < self.max_count:
            self.failed_count += 1

    def ping_succeeded(self, ellapsed, i):
        if i < self.max_count:
            self.succeeded_count += 1
            self.update_ertt(ellapsed)

    def update_ertt(self, ellapsed):
        if self.succeeded_count > 1:
            self.ertt = self.alpha * self.ertt + (1.0 - self.alpha) * ellapsed
        else:
            self.ertt = ellapsed

    def loss_probability(self):
        return float(self.failed_count) / float(self.total()) 
    
    def total(self):
        return self.succeeded_count + self.failed_count

    def throughtput(self):
        den = self.ertt * math.sqrt(self.two_thirds * self.loss_probability())
        if den == 0.0:
            return 'No se han perdido paquetes, no se puede calcular el throughput'
        if self.loss_probability() == 1.0:
            return 'No se puede estimar el RTT ya que se han perdido todos los paquetes'
        return 1.0/den

    def output(self):
        print str(self.ip) + ',' + str(self.alpha) + ',' + str(self.total()) + ',' + str(self.failed_count) + ',' + str(self.succeeded_count)  + ',' + str(self.loss_probability()) + ',' + str(self.ertt) + ',' + str(self.throughtput())

def numbers(left, right, pace):
    numbers = []
    number = left
    while number <= right:
        numbers.append(number)
        number += pace
    return numbers

if (len(sys.argv) < 4):
    print 'Usage: python ping.py [ip] [alpha_pace] [count_pace] [timeout]'
else:
    ip_dst = (sys.argv[1])
    alpha_pace = float(sys.argv[2])
    count_pace = int(sys.argv[3])
    timeout = float(sys.argv[4])
    ping = Ping(ip_dst, alpha_pace, count_pace, timeout)
    statistics = ping.do()
    print 'ip,alpha,total,failed,succeeded,lossProbability,ertt,throughput'
    for statistic in statistics:
        statistic.output()


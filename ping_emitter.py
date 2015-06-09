import sys
from datetime import datetime, timedelta
from scapy.all import *
import numpy
import time

#print packet.summary()

class TraceRoute:
    def __init__(self, ip_dst):
        self.ip_dst = ip_dst
        total_avg_rtt = 0
        total_std_rtt = 0
        
    def trace_and_process(self, time_to_live, times_repeat):
        steps = self.trace(time_to_live, times_repeat)
        self.process(steps)
        for step in steps:
            step.print(self.total_avg_rtt, self.total_std_rtt)

    def process(self, steps):
        all_rtts = [ step.rtt() for step in steps if step.rtt() != 'Unkwown']
        self.total_avg_rtt = sum(all_rtts) / float(len(all_rtts)) 
        self.total_std_rtt = numpy.std(all_rtts)
        #complete steps with route_rtt
        for step in steps:
            step.avg_route_rtt(total_avg_rtt)

    def trace(self, time_to_live, times_repeat):
        responses = []
        general_counter = 1
        acumulated_time = 0
        for i in range(1, time_to_live + 1):
            print 'Tracing with TTL: ' + str(i)
            step = Step(i)
            ip = '*'

            for j in range(0, times_repeat):
                packet = IP(dst=self.ip_dst, ttl=i)/ ICMP(seq=general_counter)
                general_counter += 1
                time_before = time.clock()
                answered, unanswered = sr(packet, timeout=1, verbose=False)
                time_after = time.clock()
                ellapsed = time_after - time_before - acumulated_time
                if len(answered) == 1:
                    ip = answered[ICMP][0][1].src #arreglar estos magics numbers
                    step.append(ip, ellapsed)

            responses.append(step)
            acumulated_time += step.avg()
        return responses

   
class Step:
    def __init__(self, ttl):
        self.ttl = ttl
        self.ip_ellapsed = dict()

    def append(self, ip, ellapsed):
        if self.ip_ellapsed.has_key(ip):
            self.ip_ellapsed[ip].append(ellapsed)
        else:
            self.ip_ellapsed[ip] = [ellapsed]

    def rtt(self): #es el RTT entre su nodo anterior y el, NO es el RTT desde el comienzo!
        if self._is_uknown_ip():
            return 'Unkwown'

        ellapsed = self._ellapsed()
        return float(sum(ellapsed)) / len(ellapsed)

    def std(self):
        if self._is_uknown_ip():
            return 'Unkwown'
        return numpy.std(self._ellapsed())

    def zrtt(self,total_avg_rtt, total_std_rtt):
        if self._is_uknown_ip():
            return 'Unkwown'            
        return (self.rtt() - total_avg_rtt) / total_std_rtt

    def print(self,total_avg_rtt,total_std_rtt):
        ttl = str(self.ttl)
        rtt = str(self.rtt())
        zrtt = str(self.zrtt(total_avg_rtt,total_std_rtt))
        ips = self.ip_ellapsed.keys()
        print "TTL: {0}\tAVG: {1}\tZRTT: {2}\tIPs: {3}".format(ttl, rtt, zrtt, ips)

    def _ellapsed(self):
        ellapsed = []
        for key in self.ip_ellapsed.keys():
            if key != '*':
                ellapsed = ellapsed + self.ip_ellapsed[key]
        return ellapsed
    def _is_uknown_ip(self):
        ellapsed = self._ellapsed()
        return len(ellapsed) == 0

if (len(sys.argv) < 4):
    print 'Usage: python ping_emiter.py [ip] [time to live] [times repeat]'
else:
    ip_dst = (sys.argv[1])
    time_to_live = int(sys.argv[2])
    times_repeat = int(sys.argv[3])
    trace_route = TraceRoute(ip_dst)
    trace_route.trace_and_process(time_to_live, times_repeat)


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
            step.print_me(self.total_avg_rtt, self.total_std_rtt)
        print "Total AVG: " + str(self.total_avg_rtt)
        print "Total STD: " + str(self.total_std_rtt)

    def process(self, steps):
        all_rtts = [ step.rtt() for step in steps if step.rtt() != 'Unknown']
        self.total_avg_rtt = sum(all_rtts) / float(len(all_rtts)) 
        self.total_std_rtt = numpy.std(all_rtts)
        
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
                answered, unanswered = sr(packet, timeout=1, verbose=False)
                if len(answered) == 1:
                    ip = answered[ICMP][0][1].src #arreglar estos magics numbers
                    sent_icmp = answered[0][0]
                    received_icmp = answered[0][1]
                    ellapsed = received_icmp.time - sent_icmp.sent_time - acumulated_time  # ACUMULADO
                    step.append(ip, ellapsed)
                    step.type = received_icmp.type
                else:
                    break
            responses.append(step)
            if step.rtt() != 'Unknown':
                acumulated_time = acumulated_time + step.rtt()
            if step.is_echo_reply():
                break
        return responses

   
class Step:
    def __init__(self, ttl):
        self.ttl = ttl
        self.ip_ellapsed = dict()
        self.type = None

    def append(self, ip, ellapsed):
        if self.ip_ellapsed.has_key(ip):
            self.ip_ellapsed[ip].append(ellapsed)
        else:
            self.ip_ellapsed[ip] = [ellapsed]

    def rtt(self): #es el RTT entre su nodo anterior y el, NO es el RTT desde el comienzo!
        if self._is_uknown_ip():
            return 'Unknown'

        ellapsed = self._ellapsed()
        return float(sum(ellapsed)) / len(ellapsed)

    def std(self):
        if self._is_uknown_ip():
            return 'Unknown'
        return numpy.std(self._ellapsed())

    def zrtt(self,total_avg_rtt, total_std_rtt):
        if self._is_uknown_ip():
            return 'Unknown'            
        return (self.rtt() - total_avg_rtt) / total_std_rtt

    def print_me(self,total_avg_rtt,total_std_rtt):
        ttl = str(self.ttl)
        rtt = str(self.rtt())
        zrtt = str(self.zrtt(total_avg_rtt,total_std_rtt))
        ips = self.ip_ellapsed.keys()
        print "TTL: {0}\tAVG: {1}\tZRTT: {2}\tIPs: {3}".format(ttl, rtt, zrtt, ips)

    def is_echo_reply(self):
        return str(self.type) == str(0)

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


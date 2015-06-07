import sys
from datetime import datetime, timedelta
from scapy.all import *
import time

#print packet.summary()

def trace_route(ip_dst, time_to_live, times_repeat):
    for i in range(0, time_to_live):
        ans_ellapsed = []
        ip = '*'
        for j in range(0, times_repeat):
            packet = IP(dst=ip_dst, ttl=i)/ ICMP()

            time_before = time.clock()
            answered, unanswered = sr(packet, timeout=1, verbose=False)
            time_after = time.clock()
            ellapsed = time_after - time_before

            if len(answered) == 1:
                ip = answered[ICMP][0][1].src #arreglar estos magics numbers
                ans_ellapsed.append(ellapsed)

        if len(ans_ellapsed) > 0:
            avg = sum(ans_ellapsed) / len(ans_ellapsed)
            print str(i) + ' Answered. ' + ip + ' ' + str(avg)
        else:
            print str(i) + ' Unanswered. ' + ip


ip_dst = (sys.argv[1])
time_to_live = int(sys.argv[2])
times_repeat = int(sys.argv[3])
trace_route(ip_dst, time_to_live, times_repeat)
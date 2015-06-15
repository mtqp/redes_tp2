import sys
from datetime import datetime, timedelta
import math
from random import randint
from scapy.all import *
import numpy
import time

def seq(start, stop, step=1):
    n = int(round((stop - start)/float(step)))
    if n > 1:
        return([start + step*i for i in range(n+1)])
    else:
        return([])


print seq(0.8,1,0.2)

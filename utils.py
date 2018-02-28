#!/usr/bin/env python3

from multiping import MultiPing
from socket import gethostbyname

def DoPing(targets):
    ips = []
    for i in  targets:
        ips.append(gethostbyname(i))

    mp = MultiPing(ips)
    mp.send()
    responses, no_reponses = mp.receive(2)

    result = {}

    time = 0

    # while(time < 10 or (not no_reponses)):
    #     mp.send()
    #     responses, no_reponses = mp.receive(2)
    #     time += 1

    for addr, rtt in responses.items():
        print(addr)
        ips.remove(addr)
        result[addr] = rtt
    for addr in ips:
        result[addr] = 0
    
    print(result)
    return result
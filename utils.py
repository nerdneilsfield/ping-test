#!/usr/bin/env python3

# from multiping import multi_ping
# from pyping import ping
from socket import gethostbyname
from time import sleep

import pexpect
import re



def ping(requests_address, ping_times=4, timeout_set=5):
    ping_result = pexpect.spawn("ping -c%s %s" % (str(ping_times), requests_address),timeout=timeout_set)
    results = []
    ping_status = "OK"
    try:
        for line in ping_result:
            perline = line.decode('utf-8')
            if "Usage" in perline:
                ping_status = "Need address"
            if "unknown" in perline or "not known" in perline or "Cannot assign" in perline:
                ping_status = "Unknow server"
            if "Permission" in perline:
                ping_status = "Need Permission"
            if "time" in perline:
                # print(perline)
                results.append(float(re.findall(r"time.([\d\.]+).ms", perline)[0]))
    except pexpect.exceptions.TIMEOUT:
        ping_status = "Time out"
        pass
    finally:
        # RETURN -> ('ping_status', ['min', 'avg', 'max', 'mdev'])
        return ping_status, results


# def DoPing(targets):
#     ips = []
#     for i in  targets:
#         ips.append(gethostbyname(i))

#     # # mp = MultiPing(ips)
#     # # mp.send()
#     # responses, no_reponses = mp.receive(2)
#     responses, no_reponses = multi_ping(ips, timeout=10, retry=10)

#     result = {}

#     time = 0

#     # while(time < 10 or (not no_reponses)):
#     #     mp.send()
#     #     responses, no_reponses = mp.receive(2)
#     #     time += 1
#     temp = ips
#     for addr, rtt in responses.items():
#         print(addr)
#         temp.remove(addr)
#         result[addr] = []
#         result[addr].append(rtt)
#     for addr in temp:
#         result[addr] = []
#         result[addr].append(0)

#     # for i in range(2):
#     #     # mp2 = MultiPing(ips)
#     #     # mp2.send()
#     #     responses, no_reponses = multi_ping(ips, timeout=3, retry=3)
#     #     temp = ips
#     #     for addr, rtt in responses.items():
#     #         print(addr)
#     #         temp.remove(addr)
#     #         result[addr].append(rtt)
#     #     for addr in temp:
#     #         result[addr].append(0)
#     #     sleep(2)

#     results = {}
#     for addr, rtt in result.items():
#         print(addr, rtt)
#         results[addr] = sum(rtt)/len(rtt)
#     return results

# def DoPing(targets):
#     results = {}
#     for target in targets:
#         r = ping(target)
#         if r.ret_code == 0:
#             results[target] = r.avg_rtt
#         else:
#             results[target] = 0
#     return results

def do_ping(host):
    status, delay = ping(gethostbyname(host), timeout_set=1000, ping_times= 4)
    if status == "OK":
        if len(delay) != 0:
            return sum(delay)/len(delay)
        else:
            return 0
    else:
        return 0

def DoPing(targets):
    results = {}
    for target in targets:
        r = do_ping(target)
        results[target] = r
    return results

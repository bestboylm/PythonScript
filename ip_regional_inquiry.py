#!/usr/bin/env python
# coding:utf-8
# Description: Python 3.x环境执行，安装依赖模块pip3 install requests

import traceback
import requests,json,time
from concurrent.futures import ThreadPoolExecutor

data = {}
# ip地址库,'http://ip.taobao.com/service/getIpInfo.php' 为淘宝IP地址库
# 其他参考ip地址库 https://www.ipip.net/support/api.html
ip_address_database='http://ip.taobao.com/service/getIpInfo.php'
# 需要分析的nginx日志文件
log_file_path = 'access.log'
america_ip_details_file = '美国IP详细信息_{}.txt'.format(time.time())
ip_query_fail_file = '查询失败IP_{}.txt'.format(time.time())
country = '美国'


def parseLog(log_path):
    """
    解析日志提取IP
    :param log_path:
    :return: set{'192.168.1.15','45.44.84.64',}
    """
    ip_list = set()
    with open(log_path) as fd:
        for line in fd:
            ip = line.strip().split()[0]
            ip_list.add(ip)
    return ip_list


def queryIpAddress(ip):
    """
    通过指定IP地址库查询IP信息,帮助信息 http://ip.taobao.com/instructions.html
    :param ip:
    :return:
    """
    ret = {'code':1,'data':''}
    try:
        ip = {'ip':ip}
        result = requests.get(url='http://ip.taobao.com/service/getIpInfo.php',params=ip)
        ret = json.loads(result.text)
    except Exception as e:
        print(traceback.format_exc())

    return ret


def getSpecialIp(ip):
    ret = queryIpAddress(ip)
    if not ret['code']:
        ip_info = ret['data']
        if ip_info['country'] == country:
            if ip_info['ip'] not in data:
                data[ip_info['ip']] = {}
                data[ip_info['ip']]['地区'] = ip_info['region']
                data[ip_info['ip']]['城市'] = ip_info['city']
                data[ip_info['ip']]['运营商'] = ip_info['isp']
    else:
        with open(ip_query_fail_file, 'w') as fd:
            fd.write(ip)

    return data


    
if __name__ == "__main__":
    start_time = time.time()
    ip_list = parseLog(log_file_path)
    print(ip_list)
    pool = ThreadPoolExecutor(100)
    for ip in ip_list:
        pool.submit(getSpecialIp,ip)
    pool.shutdown(wait=True)
    print('耗时:{}'.format(time.time() - start_time))

    print(data)
    print("归属地为美国的IP有：{}个".format(len(data)))
    with open(america_ip_details_file, 'w') as fd:
        for ip in data:
            print('{}\t地区：{}\t城市：{}\t运营商：{}'.format(ip, data[ip]['地区'], data[ip]['城市'], data[ip]['运营商']))
            fd.write('{}\t地区：{}\t城市：{}\t运营商：{}\n'.format(ip, data[ip]['地区'], data[ip]['城市'], data[ip]['运营商']))

#!/usr/bin/env python
#-*-encoding:utf-8-*-
# Author: Aaron
# Email: 1121914451@qq.com
# Time: 2018/3/16 10:42

dic = {}
with open('1.log') as fd:
    for line in fd:
        date = line.split()[1].split('[')[1]
        url = line.split()[3]
        ip = line.split()[0]
    
        if date not in dic:
            dic[date] = {}
            if url not in dic[date]:
                dic[date][url] = []
            dic[date][url].append(ip)
        else:
            if url not in dic[date]:
                dic[date][url] = []
            dic[date][url].append(ip)

tmp = []
for item in dic:
    tmp += ["{0:<22}{1:<15}{2:>9}个IP".format(item, i, len(dic[item][i])) for i in dic[item]]


print("{0:<20}{1:<15}{2:>10}".format("日期","url","数量"))
for m in tmp:
    print(m)
#!/usr/bin/env python
#-*-encoding:utf-8-*-
# Author: Aaron
# Email: 1121914451@qq.com
# Time: 2018/3/16 10:42

# 读取文件后可以得到一下列表
s = ["192.168.1.100 [2017/1/12 08:09:10] www.baidu.com/ ",
     "192.168.1.101 [2017/1/12 08:09:10] www.baidu.com/ ",
     "192.168.1.101 [2017/1/12 09:09:10] www.sohu.com/ ",
     "192.168.1.101 [2017/1/13 09:09:10] www.sohu.com/ "
    ]

import re
ret = {}

for line in s:
    tmp = re.findall("([0-9.]+).*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2}).*\s+(.*.)",line)
    access_date = tmp[0][1]
    access_IP = tmp[0][0]
    access_url = tmp[0][2]

    if access_date not in ret:
        ret[access_date]={}
        if access_url not in ret[access_date]:
            ret[access_date][access_url] = []
        ret[access_date][access_url].append(access_IP)
    else:
        if access_url not in ret[access_date]:
            ret[access_date][access_url] = []
        ret[access_date][access_url].append(access_IP)

tmp = []
for item in ret:
    tmp += ["{0:<22}{1:<15}{2:>9}个IP".format(item, i, len(ret[item][i])) for i in ret[item]]


print("{0:<20}{1:<15}{2:>10}".format("日期","url","数量"))
for m in tmp:
    print(m)

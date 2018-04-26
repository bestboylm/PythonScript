#!/usr/bin/env python
# -*-encoding:utf-8-*-
# Author: Aaron
# Email: 1121914451@qq.com
# Time: 2018/4/26 11:22
import re
import traceback
import requests
from pypinyin import lazy_pinyin

class Parse(object):
    def __init__(self):
        self.parse_list = ['phone_list', 'idcard', 'phone']

    def idcard_parse(self, content):
        """
        解析爬取的身份证信息网页
        :return:{id:'',name:'',city:'',sex:''}
        """
        pass

    def phone_list_parse(self, content):
        """
        解析爬取的区域号码网页
        :param content:
        :return: []
        """
        if not content:
            return False

        region_phone_list = []
        phone_list = []
        for line in content.split('\r\n'):
            expr = r'^<li.*\d{7}</a></li>'
            temp_list = re.findall(expr, line.strip(), re.S | re.M)
            if temp_list:
                region_phone_list.append(temp_list[0])

        with open('phone.txt', 'w') as fd:
            for line in region_phone_list:
                num = line.split()[2].split('/')[3].split('.htm')[0] + self.part_number[-4:]
                phone_list.append(num)
                fd.write(num + '\n')

        # print(len(region_phone_list), region_phone_list)
        # print(len(phone),phone)
        for i in phone_list:
            print(i)
        print("一共有{}个号码".format(len(phone_list)))

        return phone_list

    def phone_parse(self):
        """
        精确分析出号码
        :return:
        """
        pass

    
class UserInfo(Parse):
    jhb_url = 'http://www.jihaoba.com/haoduan/'
    idcard_url = 'http://qq.ip138.com/idsearch/index.asp?action=idcard&userid='

    def __init__(self, name, part_number, idcard):
        """
        :param part_number: 手机号前三位后四位
        :param idcard: 身份证号码
        """
        super(UserInfo,self).__init__()
        self.name = name
        self.part_number = part_number
        self.idcard = idcard

    def query_idcard_info(self, idcard_url=idcard_url):
        """
        身份证号码归属市等信息查询
        :param idcard_url:
        :return:
        """
        url = '{}{}'.format(idcard_url,self.idcard)
        response = requests.get(url).text.encode().decode()
        idcard_info = self.idcard_parse(response)
        return idcard_info

    def query_phone_list(self, city, jhb_url=jhb_url):
        """
        区域号码列表查询
        :param city:  号码归属市
        :param jhb_url:
        :return:
        """
        city = ''.join(lazy_pinyin(city))
        if len(self.part_number) != 7:
            print("你电话号码输错了，只要输前三位后四位!")
            return False
        phone_top_three = ''.join(self.part_number[:3])
        try:
            url = '{}{}/{}.htm'.format(jhb_url, phone_top_three, city)
            print(url)
            response = requests.get(url).text.encode().decode()
            # print(response)
        except Exception as e:
            print("出现错误:\n", traceback.format_exc())
            return False

        self.phone_list_parse(response)

    def query_phone(self, name, phone_list):
        pass

    def process(self):
        # idcard_info = self.query_idcard_info()
        city = '深圳'
        self.query_phone_list(city)


if __name__ == "__main__":
    name = input("请输入真实姓名: ").strip()
    part_number = input("请输入号码前三位后四位: ").strip()
    idcard = input("请输入身份证号码: ").strip()
    u = UserInfo(name,part_number, idcard)
    u.process()
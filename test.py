# -*- coding: utf-8 -*-
# @Time    : 2021/8/11 1:41
# @Author  : 陈玉辉
# @File    : test.py
import json
import os
import random
import time

import execjs
import requests
import aiohttp
import re
from google_trans_new import google_translator
from lxml import etree

msg = '擦汗一下2021-09-03的课表'
date = ''.join(re.findall('[\d-]', msg))

week = time.strptime(date, '%Y-%m-%d').tm_wday+1

def get_timetable(week, Time=time.strftime("%Y-%m-%d", time.localtime())):
    print(Time)
    jsText = """
            var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
            function encodeInp(input) {
                var output = "";
                var chr1, chr2, chr3 = "";
                var enc1, enc2, enc3, enc4 = "";
                var i = 0;
                do {
                    chr1 = input.charCodeAt(i++);
                    chr2 = input.charCodeAt(i++);
                    chr3 = input.charCodeAt(i++);
                    enc1 = chr1 >> 2;
                    enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
                    enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
                    enc4 = chr3 & 63;
                    if (isNaN(chr2)) {
                        enc3 = enc4 = 64
                    } else if (isNaN(chr3)) {
                        enc4 = 64
                    }
                    output = output + keyStr.charAt(enc1) + keyStr.charAt(enc2) + keyStr.charAt(enc3) + keyStr.charAt(enc4);
                    chr1 = chr2 = chr3 = "";
                    enc1 = enc2 = enc3 = enc4 = ""
                } while (i < input.length);
                return output
            }

            function encryptPass(user, password){

                return encodeInp(user) + "%%%" + encodeInp(password);

            }
            """
    data = {
        'userAccount': '202027550202',
        'userPassword': 'cyh011029158118',
        'encoded': execjs.compile(jsText).call("encryptPass", '202027550202', 'cyh011029158118')
    }
    url = 'http://61.186.97.37:8081/jsxsd/xk/LoginToXk'
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }
    session = requests.session()
    print(session.post(url, data=data, headers=headers).text)
    url1 = f'http://61.186.97.37:8081/jsxsd/framework/main_index_loadkb.jsp?rq={Time}&sjmsValue='
    response = session.get(url1, headers=headers)
    print(response.text)
    print(response)
    html = etree.HTML(response.text)
    trs = html.xpath(f"//tbody//tr")
    timetable = {}
    table = []
    for i in range(2, 9):
        for td in trs:
            td = td.xpath(f'./td[{i}]')
            for p in td:
                ta = []
                j = str(p.xpath('.//p/@title')).strip("['']").replace('<br/>', '\n')
                table.append(j)
    timetable[1] = table[0:6]
    timetable[2] = table[7:13]
    timetable[3] = table[13:19]
    timetable[4] = table[19:25]
    timetable[5] = table[25:31]
    timetable[6] = table[31:37]
    timetable[7] = table[37:43]
    tables = ['第一节:', '第二节:', '第三节:', '第四节:', '晚一:', '晚二:']
    timetable_str = ''
    index = 0
    for tb in timetable[week + 1]:
        if tb == '':
            timetable_str += f'{tables[index]}没有课哟\n\n'
        else:
            res = re.search(r'课程名称：(?P<table>.*?)上课时间', tb, re.S)
            table = res.group('table').replace('\n', '')
            cla = tb.split('\n')[-1].replace('\n', '')
            timetable_str += f'{tables[index]} {table}\n{cla}\n\n'
        index += 1
    print(timetable)
    return timetable_str


timetable = get_timetable(week, '2021-07-10')
print(timetable)
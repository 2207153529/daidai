from pathlib import Path

# import nonebot
import nonebot
from nonebot import get_driver

from .config import Config


###########################
import json
import os
import random
import re
import time
import execjs
import nonebot
import requests
from lxml import etree
from nonebot import on_command, on_message, on_startswith
from nonebot.permission import SUPERUSER
from nonebot.plugin import on, on_regex, require
from nonebot.rule import to_me, keyword
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event, Message
from nonebot.adapters.cqhttp import message, MessageSegment
from nonebot.config import Config
import aiohttp
from .config import STATIC_VAL


#####################

global_config = get_driver().config
config = Config(**global_config.dict())

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").
    resolve()))





#############################API#################################
# 实时疫情数据API
provinceAPI = 'https://lab.isaaclin.cn//nCoV/api/provinceName'      # 可以查看省份及国家的API
cityAPI = 'https://lab.isaaclin.cn/nCoV/api/area?latest=1&province='    # 查看省份疫情实时数据API
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
scheduler = require('nonebot_plugin_apscheduler').scheduler



######################################################################

#################################获取群成员列表#####################################

async def get_group_number_info(grout_id: int) -> dict:
    """
    说明:获取群成员信息
    :param grout_id: 群ID
    :return: 返回字典
    """
    bot = nonebot.get_bots()['2207153529']
    r = await bot.call_api('get_group_member_list', group_id=grout_id)
    return r



#################################查天气功能#####################################################

weather = on_regex('.*天气.*', priority=8)
@weather.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = re.sub('[看一下查的得地滴天气]', '', str(event.get_message()))
    if args:
        state["city"] = args  # 如果用户发送了参数则直接赋值


@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city(bot: Bot, event: Event, state: T_State):
    city = state["city"]
    parameters_now = {'key': 'c92ef915f460e53be4550e246e3d0318',  #
                      'city': city,  #
                      'extensions': 'base',  #
                      'output': 'json'  #
                      }  #
    r_now = requests.get("https://restapi.amap.com/v3/weather/weatherInfo?parameters", params=parameters_now)  #
    List_City = len(r_now.json()['lives'])
    if List_City != 0:
        await weather.send("正在查询中.....")
        try:  #
            weater = r_now.json()['lives'][0]['weather']  #
            temp = r_now.json()['lives'][0]['temperature']  #
            winddirection = r_now.json()['lives'][0]['winddirection']  #
            windpow = r_now.json()['lives'][0]['windpower']  #
            humidity = r_now.json()['lives'][0]['humidity']  #
            result_now = '当前' + city + '的天气为：' + weater + '，' + temp + '℃，空气湿度：' + humidity + '，刮' + winddirection + '风，风力' + windpow + '级！' + '\n'  #
            # 预报                                                                                                                                                           #
            parameters_next = {'key': 'c92ef915f460e53be4550e246e3d0318',  #
                               'city': city,  #
                               'extensions': 'all',  #
                               'output': 'json'  #
                               }  #
            r_next = requests.get("https://restapi.amap.com/v3/weather/weatherInfo?parameters",
                                  params=parameters_next)  #
            # 当日                                                                                                                                                           #
            data0_data = r_next.json()['forecasts'][0]['casts'][0]['date']  #
            data0_week = r_next.json()['forecasts'][0]['casts'][0]['week']  #
            data0_weather = r_next.json()['forecasts'][0]['casts'][0]['dayweather']  #
            data0_tempmin = r_next.json()['forecasts'][0]['casts'][0]['nighttemp']  #
            data0_tempmax = r_next.json()['forecasts'][0]['casts'][0]['daytemp']  #
            data0_dic = r_next.json()['forecasts'][0]['casts'][0]['daywind']  #
            data0_pow = r_next.json()['forecasts'][0]['casts'][0]['daypower']  #
            result0 = data0_data + '周' + data0_week + '：' + data0_weather + '，' + data0_tempmin + '℃~' + \
                      data0_tempmax + '℃，' + data0_dic + '风' + data0_pow + '级' + '\n'
            # 次日                                                                                                                                                           #
            data1_data = r_next.json()['forecasts'][0]['casts'][1]['date']  #
            data1_week = r_next.json()['forecasts'][0]['casts'][1]['week']  #
            data1_weather = r_next.json()['forecasts'][0]['casts'][1]['dayweather']  #
            data1_tempmin = r_next.json()['forecasts'][0]['casts'][1]['nighttemp']  #
            data1_tempmax = r_next.json()['forecasts'][0]['casts'][1]['daytemp']  #
            data1_dic = r_next.json()['forecasts'][0]['casts'][1]['daywind']  #
            data1_pow = r_next.json()['forecasts'][0]['casts'][1]['daypower']  #
            result1 = data1_data + '周' + data1_week + '：' + data1_weather + '，' + data1_tempmin + '℃~' + \
                      data1_tempmax + '℃，' + data1_dic + '风' + data1_pow + '级' + '\n'
            # 后日                                                                                                                                                           #
            data2_data = r_next.json()['forecasts'][0]['casts'][2]['date']  #
            data2_week = r_next.json()['forecasts'][0]['casts'][2]['week']  #
            data2_weather = r_next.json()['forecasts'][0]['casts'][2]['dayweather']  #
            data2_tempmin = r_next.json()['forecasts'][0]['casts'][2]['nighttemp']  #
            data2_tempmax = r_next.json()['forecasts'][0]['casts'][2]['daytemp']  #
            data2_dic = r_next.json()['forecasts'][0]['casts'][2]['daywind']  #
            data2_pow = r_next.json()['forecasts'][0]['casts'][2]['daypower']  #
            result2 = data2_data + '周' + data2_week + '：' + data2_weather + '，' + data2_tempmin + '℃~' + \
                      data2_tempmax + '℃，' + data2_dic + '风' + data2_pow + '级' + '\n'
            # 大后日                                                                                                                                                         #
            data3_data = r_next.json()['forecasts'][0]['casts'][3]['date']  #
            data3_week = r_next.json()['forecasts'][0]['casts'][3]['week']  #
            data3_weather = r_next.json()['forecasts'][0]['casts'][3]['dayweather']  #
            data3_tempmin = r_next.json()['forecasts'][0]['casts'][3]['nighttemp']  #
            data3_tempmax = r_next.json()['forecasts'][0]['casts'][3]['daytemp']  #
            data3_dic = r_next.json()['forecasts'][0]['casts'][3]['daywind']  #
            data3_pow = r_next.json()['forecasts'][0]['casts'][3]['daypower']  #
            result3 = data3_data + '周' + data3_week + '：' + data3_weather + '，' + data3_tempmin + '℃~' + \
                      data3_tempmax + '℃，' + data3_dic + '风' + data3_pow + '级' + '\n'
            result_all = result_now + result0 + result1 + result2 + result3  #
        except:
            result_all = '我似乎有点问题...换个说法试试吧~'  #
    else:
        result_all = '[错误]格式为：天气 + 城市'
    await weather.send(result_all)


##################################################################################################################


#################################帮助功能#####################################################


help = on_command('help', rule=to_me(), aliases={'帮助', '需要帮助', '你会啥', '你会什么功能', '你有什么功能'}, priority=4)
@help.handle()
async def get_help(bot: Bot, event: Event, state: T_State):
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), 'plugins/help.png')
    await help.send(message.Message('下面的我都能做到哦！\n[CQ:image,file=http://a1.qpic.cn/psc?/V52atmOK2u5JUK3FVE611ZbulV4a4WS4/ruAMsa53pVQWN7FLK88i5mmwErYxDlIaFLkEt769pXwZLYCAKlC19BIaP0obEkfyi42y249jjMV6lvOi7LQTBISqOKyvsxqfu80pzhlWB04!/c&ek=1&kp=1&pt=0&bo=gAK9CwAAAAABJzQ!&tl=3&vuin=3362045101&tm=1629057600&sce=60-2-2&rf=0-0,id=40000]\n注意：所有命令均采用re正则匹配哦，所以只要包含关键字就会触发功能。'))

######################################################################################



#################################查课表功能#####################################################

time_table = on_regex('.*课表.*', priority=5)

@time_table.handle()
async def get_time_table(bot: Bot, event: Event, state: T_State):
    message = str(event.get_message())
    year, month = time.localtime().tm_year, time.localtime().tm_mon
    if re.search('.*明天.*', message):
        day = time.localtime().tm_mday + 1
    elif re.search('.*大后天.*', message):
        day = time.localtime().tm_mday + 3
    elif re.search('.*后天.*', message):
        day = time.localtime().tm_mday + 2
    else:
        day = time.localtime().tm_mday
    week_list = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    week = time.strptime(f"{year}-{month}-{day}", '%Y-%m-%d').tm_wday
    timetable = await get_timetable(f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}")
    table_list = timetable.split('\n\n')
    table = [table.split(':') for table in table_list]
    jsonContent = {
            "app": "com.tencent.miniapp",
            "desc": "",
            "view": "notification",
            "ver": "0.0.0.1",
            "prompt": "课表",
            "appID": "",
            "sourceName": "",
            "actionData": "",
            "actionData_A": "",
            "sourceUrl": "",
            "meta": {
                "notification": {
                    "appInfo": {
                        "appName": "大数据2002",
                        "appType": 4,
                        "appid": 1109659848,
                        "iconUrl": "http://a1.qpic.cn/psc?/V52atmOK2u5JUK3FVE611ZbulV4a4WS4/ruAMsa53pVQWN7FLK88i5jqhYX6WhoAG88M3iRVZPNbcrVclVw9Fd5ssKP6HF6oyC89DQ3cI6po4l6BrsIYSmXS4XthMzvGks2TFMtzJeok!/c&ek=1&kp=1&pt=0&bo=gAKAAgAAAAABFzA!&tl=3&vuin=3362045101&tm=1629046800&sce=60-2-2&rf=0-0"
                    },
                    "data": [
                        {
                            "title": "第一节课",
                            "value": f"{table[0][1].replace('上课地点：', '')}"
                        },
                        {
                            "title": "第二节课",
                            "value": f"{table[1][1].replace('上课地点：', '')}"
                        },
                        {
                            "title": "第三节课",
                            "value": f"{table[2][1].replace('上课地点：', '')}"
                        },
                        {
                            "title": "第四节课",
                            "value": f"{table[3][1].replace('上课地点：', '')}"
                        },
                        {
                            "title": "晚一",
                            "value": f"{table[4][1].replace('上课地点：', '')}"
                        },
                        {
                            "title": "晚二",
                            "value": f"{table[5][1].replace('上课地点：', '')}"
                        },
                    ],
                    "title": f"{week_list[week]}课表",
                    "button": [
                        {
                            "name": "湖南信息职业技术学院",
                            "action": ""
                        }
                    ],
                    "emphasis_keyword": ""
                }
            },
            "text": "",
            "sourceAd": ""
        }
    await time_table.send(MessageSegment.json(json.dumps(jsonContent)))


async def get_timetable(Time=time.strftime("%Y-%m-%d", time.localtime())):
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
        'encoded': execjs.compile(jsText).call("encryptPass", STATIC_VAL.JW_USER, STATIC_VAL.JW_PASSWORD)
    }
    week = time.strptime(Time, '%Y-%m-%d').tm_wday
    url = 'http://61.186.97.37:8081/jsxsd/xk/LoginToXk'
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }
    session = requests.session()
    session.post(url, data=data, headers=headers)
    url1 = f'http://61.186.97.37:8081/jsxsd/framework/main_index_loadkb.jsp?rq={Time}&sjmsValue='
    response = session.get(url1, headers=headers)
    html = etree.HTML(response.text)
    trs = html.xpath(f"//tbody//tr")
    timetable = {}
    table = []
    for i in range(2, 9):
        for td in trs:
            td = td.xpath(f'./td[{i}]')
            for p in td:
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
    return timetable_str


######################################################################################




#################################呼叫主人功能#####################################################


master = on_regex(r'(.*)主人(.*)', priority=98)

@master.handle()
async def Owener(bot: Bot, event: Event, state: T_State):
    a = random.randint(1, 5)
    if a == 1:
        await master.send(message.Message('你在哪[CQ:face,id=32]有人找你哇~[CQ:at,qq=2207153529]'))
    elif a == 2:
        await master.send(message.Message('他一直这样，把我扔进来就不管我了[CQ:face,id=107][CQ:at,qq=2207153529]'))
    elif a == 3:
        await master.send(message.Message('你TM在哪[CQ:face,id=11]又去隔壁找小姐姐去了？[CQ:at,qq=2207153529]'))
    else:
        await master.send(message.Message('……主人鸽了，知道他在哪儿摸鱼的话请把他拖回来~[CQ:at,qq=2207153529]'))


############################################################################################################################



###############################青年大学习##################################################################################################


qinnian = on_regex('.*[查看].*青年大学习.*', rule=to_me(), priority=5)

@qinnian.handle()
async def get_qinnian(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()



@qinnian.got('url', prompt='请发送查询的网址:')
async def get_qin(bot: Bot, event: Event, state: T_State):
    url = state['url'].strip()
    if len(re.compile('vity=(.*?)').findall(url)) == 0:
        await qinnian.reject('输入的网址有误，请重新输入！！')
    await qinnian.send(message.Message('正在努力查询中[CQ:face,id=30]，请稍后.....'))
    students = {'曹智杰': '202027550201', '陈玉辉': '202027550202', '邓鸿飞': '202027550203', '邓宇伸': '202027550204',
                '付桂': '202027550205', '何东凯': '202027550206', '胡佳彬': '202027550207', '兰宇': '202027550208',
                '李东清': '202027550209', '李家武': '202027550210', '廖瑞辉': '202027550211',
                '刘潘': '202027550213', '刘伟': '202027550214', '龙庆林': '202027550215', '卢军': '202027550216',
                '罗剑锋': '202027550217', '彭蔚': '202027550218', '孙超': '202027550220',
                '孙万成': '202027550221', '唐程': '202027550222', '王康华': '202027550223', '王胜豪': '202027550224',
                '吴超': '202027550225', '徐博涵': '202027550226', '阳梦缘': '202027550227', '杨楷': '202027550228',
                '杨磊': '202027550229', '袁鑫铭': '202027550230', '张京磊': '202027550231', '张子豪': '202027550232',
                '朱飞': '202027550233', '资睿': '202027550234', '董玉瑾': '202027550235', '蒋昭艳': '202027550236',
                '黎雨婷': '202027550237', '刘娟': '202027550238', '毛巧慧': '202027550239', '宋宇': '202027550240',
                '唐美华': '202027550241', '伍子敏': '202027550242', '杨宇轩': '202027550243', '钟佳慧': '202027550244'}


    data = {
        '__VIEWSTATE': '/wEPDwUKLTMyMTU0MzYyMWRkoZHOgHhOO40wPVTu80nPaxWntfA=',
        '__VIEWSTATEGENERATOR': 'A51944F2',
        '__EVENTVALIDATION': '/wEdAANqoayMaMx71jCjDamf+CNGfxLSikTZqx6XzQUk71djD7A88eHGsukWIJIFOXmn8ii6Ozzw4oLFEVXf9/4fMxtQ0oVJ5w==',
        'hfPostType': '1',
        'hfQuery': '10000|大数据2002'
    }
    activity = str(url).split('=')[-1]
    session = requests.session()
    response = session.post(url, headers=headers, data=data)
    html = etree.HTML(response.text)
    div_list = html.xpath("//div[@class='query__copies']")
    url_list = []
    for ifo in div_list:
        ts = ifo.xpath(".//div[@class='query__inner']/@ts")
        joinid = ifo.xpath(".//div[@class='query__inner']/@joinid")
        sign = ifo.xpath(".//div[@class='query__inner']/@partersign")
        index = ifo.xpath(".//div[@class='query__inner']/@index")
        url = f'https://www.wjx.cn/handler/JoinDetail.ashx?activityid={activity}&joinid={joinid[0]}&ts={ts[0]}&sign={sign[0]}&index={index[0]}&oq=1'
        url_list.append(url)
    ID = []
    stu_Name = []
    for url1 in url_list:
        response = session.get(url1, headers=headers)
        re1 = re.compile(r'<div>2020275502(.*?)</div>', re.S)
        id = re1.findall(response.text)
        infoHtml = etree.HTML(response.text)
        stuName = infoHtml.xpath("//div[@class='data__key']//text()")[1]
        stu_Name.append(stuName)
        ID.append('2020275502' + str(id).strip("['']"))
    not_ok = []
    for stu in students.values():
        if stu in ID:
            continue
        else:
            not_ok.append(str([k for k, v in students.items() if v == stu]).strip("['']"))
    
    writeError = []
    for name in not_ok:
        if name in stu_Name:
            writeError.append(name)
    msg = f"""青年大学习共提交了{len(url_list)}份，以下同学已提交：\n{' '.join(stu_Name)}\n\n未完成青年大学习的有{len(not_ok)}份，有如下同学未完成：\n{' '.join(not_ok)}\n\n其中学号填写错误的可能有：\n{' '.join(writeError)}"""
    await qinnian.finish(message.Message(msg))


####################################################################################


########################################实时疫情数据########################################


yiqin = on_regex('.*疫情.*', priority=3)

@yiqin.handle()
async def get_yiqin(bot: Bot, event: Event, state: T_State):
    args = re.sub(r"[看一下疫情查的]", "", str(event.get_message()))
    if args:
        state['city'] = args


@yiqin.got('city', prompt='请发送你想查询的省份+城市')
async def get_yiq(bot: Bot, event: Event, state: T_State):
    global city
    global province
    citys = state['city']
    if re.findall('(.*)省(.*)', citys):
        try:
            strin = str(citys).split('省', 1)
            province = strin[0] + '省'
            city = strin[1]
        except:
            await yiqin.reject('发送的格式有误，请重新发送(某省+某城市)')
    else:
        resp = json.loads(requests.get(provinceAPI, headers=headers).text)
        for pro in resp['results']:
            if citys[:2] == pro[:2]:
                try:
                    stri = str(pro[:-1])
                    province = pro
                    city = re.findall(f'{stri}(.*)', citys)[0]
                except:
                    await yiqin.reject('发送的格式有误，请重新发送(某省+某城市)')
                break
            else:
                province = 'None'
        if province not in resp['results']:
            await yiqin.reject(message.Message('在我的印象中好像没有这个省[CQ:face,id=32]'))
    url = cityAPI + province
    response = json.loads(requests.get(url, headers=headers).text)
    try:
        new_time = response['results'][0]['updateTime'] / 1000
        new_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(new_time))
        city_list = [cit['cityName'] for cit in response['results'][0]['cities']]
        if city not in city_list:
            await yiqin.reject(message.Message(f'你确定{province}有这个城市[CQ:face,id=32]'))
        for cit in response['results'][0]['cities']:
            cityName = cit['cityName']
            if city == cityName:
                # 现存确诊人数
                currentConfirmedCount = cit['currentConfirmedCount']
                # 累计确诊人数
                confirmedCount = cit['confirmedCount']
                # 疑似感染人数
                suspectedCount = cit['suspectedCount']
                # 治愈人数
                curedCount = cit['curedCount']
                # 死亡人数
                deadCount = cit['deadCount']
                # 治愈率
                cure = "%.2f%%" % (curedCount / confirmedCount * 100)
                # 死亡率
                dead = "%.2f%%" % (deadCount / confirmedCount * 100)
                await yiqin.send(f"{city} 疫情数据:\n        目前确诊:\n            确诊人数:{currentConfirmedCount}\n            疑似人数:{suspectedCount}\n  {'=' * 22}\n        累计数据:\n            确诊人数:{confirmedCount}\n"
                                 f"            治愈人数:{curedCount}\n            死亡人数:{deadCount}\n        治愈率:{cure}\n        死亡率:{dead}\n更新日期:{new_time}\n"
                                 f"数据来源于https://github.com/BlankerL/DXY-COVID-19-Data")
    except:
        await yiqin.send('真抱歉，人家内部出问题了')
#########################################################################################


####################################定时发送课表###########################################################
"""
@scheduler.scheduled_job("cron", minute='*/1', id='call_timetable')
async def run_every_2_hour():
     day_hour, day_min = time.localtime().tm_hour, time.localtime().tm_min
    msg = ''
    bot = nonebot.get_bots()['3362045101']
    print(time.localtime().tm_hour, time.localtime().tm_min)
    if day_hour == 8 and day_min == 10:
        timetable = await get_timetable()
        timetable_list = timetable.split('\n\n')
        if not re.findall('(.*)没有课哟(.*)', timetable_list[0]):
            msg = timetable_list[0]
    elif day_hour == 10 and day_min == 0:
        timetable = await get_timetable()
        timetable_list = timetable.split('\n\n')
        if not re.findall('(.*)没有课哟(.*)', timetable_list[1]):
            msg = timetable_list[1]
    elif day_hour == 13 and day_min == 40:
        timetable = await get_timetable()
        timetable_list = timetable.split('\n\n')
        if not re.findall('(.*)没有课哟(.*)', timetable_list[2]):
            msg = timetable_list[2]
    elif day_hour == 15 and day_min == 30:
        timetable = await get_timetable()
        timetable_list = timetable.split('\n\n')
        if not re.findall('(.*)没有课哟(.*)', timetable_list[3]):
            msg = timetable_list[3]
    elif day_hour == 19 and day_min == 0:
        timetable = await get_timetable()
        timetable_list = timetable.split('\n\n')
        if not re.findall('(.*)没有课哟(.*)', timetable_list[4]):
            msg = timetable_list[4]
    elif day_hour == 20 and day_min == 30:
        timetable = await get_timetable()
        timetable_list = timetable.split('\n\n')
        if not re.findall('(.*)没有课哟(.*)', timetable_list[5]):
            msg = timetable_list[5]
    if len(msg) > 0:
        tableName = re.findall(': (.*)\n', msg)[0]
        addres = msg.split('上课地点：', 1)[1]
        msg = message.Message(f'下节课为:\n{tableName}\n请同学们按时前往 {addres} 上课, 千万别迟到哦{"[CQ:face,id=30]" * 3}')
        await bot.call_api('send_group_msg', **{
            'group_id': f'{STATIC_VAL.GROUP_ID}',
            'message': msg
        })
"""

########################################翻译功能#############################################################################







##############################################################################################################################






####################################祖安模式#################################################################

zuan = on_regex('.*[打开关闭].*祖安模式.*', rule=to_me(), priority=8)

@zuan.handle()
async def on_zuan(bot: Bot, event: Event, state: T_State):
    if STATIC_VAL.ZUAN_ON == '1':
        msg = str(event.get_message())
        args = re.sub('[祖安模式]', '', msg)
        if re.search('.*开.*', args):
            STATIC_VAL.MODE_ZUAN = '1'
            await zuan.send('设置完成！\n注:此模式回复较慢且异常暴躁！骂你不带重样的！请做好心理准备！\n')
        elif re.search('.*关.*', args):
            STATIC_VAL.MODE_ZUAN = '0'
            await zuan.send('祖安模式已关闭')
        else:
            await zuan.reject('格式错误，请回复：开启or关闭')

    else:
        await zuan.send('抱歉，该功能已被我大哥关闭，若想使用请联系我大哥')



###################################回复模式###################################

mssage_send = on_message(priority=50, block=False)

@mssage_send.handle()
async def send_zuan(bot: Bot, event: Event, state: T_State):
    if STATIC_VAL.MODE_ZUAN == '1':
        msg = await get_zuanmsg()
        await mssage_send.send(msg)

    if STATIC_VAL.CAI_HONG == '1':
        fn = os.path.join(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), 'plugins/caihon.text')
        with open(fn, 'r', encoding='utf-8') as f:
            msg_list = f.read().split('\n')
            await mssage_send.send(random.choice(msg_list))



######################################################################



async def get_zuanmsg():
    url = 'https://nmsl.shadiao.app/api.php?level=min'
    response = requests.get(url).text
    if not re.search('服务器', response):
        return response
    else:
        fn = os.path.join(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), 'plugins/zuan.text')
        with open(fn, 'r', encoding='utf-8') as f:
            zuan_list = f.read().split('\n')
            return random.choice(zuan_list)



######################################################################################################




###########################################彩虹屁###########################################################

zuan = on_regex('.*[打开关闭].*彩虹屁.*', rule=to_me(), priority=9)

@zuan.handle()
async def on_zuan(bot: Bot, event: Event, state: T_State):
    if STATIC_VAL.CAIHONG_ON == '1':
        msg = str(event.get_message())
        args = re.sub('[彩虹屁]', '', msg)
        if re.search('.*开.*', args):
            STATIC_VAL.CAI_HONG = '1'
            await zuan.send('设置完成！\n注意: 别被夸上头哦[CQ:face,id=4]\n')
        elif re.search('.*关.*', args):
            STATIC_VAL.CAI_HONG = '0'
            await zuan.send('彩虹屁模式已关闭')
        else:
            await zuan.reject('格式错误，请回复：开启or关闭')
    else:
        await zuan.send('抱歉，该功能已被我大哥关闭，若想使用请联系我大哥')




batter = on_regex(r'.*[骂喷].*', rule=to_me(), priority=30)

@batter.handle()
async def send_batter(bot: Bot, event: Event, state: T_State):
    messageinfo = str(event.get_message()).strip()
    user_id = ''.join(re.findall('\d', messageinfo))
    send_user_id = str(event.get_user_id())
    if re.search('.*[他她它].*', messageinfo):
        if user_id == '':
            await batter.send('[格式错误]: 后面请添加群成员QQ')
        else:
            user_id = int(user_id)
            zuan = await get_zuanmsg()
            if user_id == 2207153529:
                await batter.send('就你这大猪蹄子还想骂我大哥？？？？')
                msg = message.Message(f'[CQ:at,qq={send_user_id}] {zuan}')
            else:
                msg = message.Message(f'[CQ:at,qq={user_id}] {zuan}')
                await batter.send(msg)



kuauser = on_regex(r'.*[夸表扬].*', rule=to_me(), priority=31)

@kuauser.handle()
async def send_batter(bot: Bot, event: Event, state: T_State):
    messageinfo = str(event.get_message()).strip()
    get_user_id = ''.join(re.findall('\d', messageinfo))
    get_send_user_id = str(event.get_user_id())
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), 'plugins/caihon.text')
    with open(fn, 'r', encoding='utf-8') as f:
        caihon_list = f.read().split('\n')
    caihonMsg = random.choice(caihon_list)
    if len(get_user_id) > 0 and re.search('[她它他]', messageinfo):
        get_user_id = int(get_user_id)
        msg = message.Message(f'[CQ:at,qq={get_user_id}] {caihonMsg}')
        await kuauser.send(msg)
    else:
        msg = message.Message(f'[CQ:at,qq={get_send_user_id}] {caihonMsg}')
        await kuauser.send(msg)


#######################################SUPER_USER#######################################

super_user = on_regex('.*[关闭打开].*功能.*', rule=to_me(), permission=SUPERUSER, priority=1)

@super_user.handle()
async def get_superuser_message(bot: Bot, event: Event, state:T_State):
    msg = str(event.get_message())
    if re.search('.*关.*祖安.*', msg):
        STATIC_VAL.ZUAN_ON = '0'
        await super_user.send('祖安功能已成功关闭')
    elif re.search('.*开.*祖安.*', msg):
        STATIC_VAL.ZUAN_ON = '1'
        await super_user.send('祖安功能已打开，回复:\ncall小呆+祖安模式or开启祖安模式or关闭祖安模式即可使用该功能')
    elif re.search('.*关.*彩虹屁.*', msg):
        STATIC_VAL.CAIHONG_ON = '0'
        await super_user.send('彩虹屁模式已成功关闭')
    elif re.search('.*开.*彩虹屁.*', msg):
        STATIC_VAL.CAIHONG_ON = '1'
        await super_user.send('彩虹屁功能已打开，回复:\ncall小呆+彩虹屁模式or开启彩虹屁模式or关闭彩虹屁模式即可使用该功能')


score = on_command('查成绩', priority=10)


@score.handle()
async def get_score(bot: Bot, event: Event, state: T_State):
    # fn = os.path.join(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), 'plugins/weixin.jpg')
    msg = message.Message(f'抱歉，俺暂时还未开发这个功能，若想查成绩可扫下方二维码关注公众号进行查询\n[CQ:image,file=http://a1.qpic.cn/psc?/V52atmOK2u5JUK3FVE611ZbulV4a4WS4/ruAMsa53pVQWN7FLK88i5mmwErYxDlIaFLkEt769pXzA5jhTSQu4irIiLsL5SbueXHuwS5lr.QQ*LiinNPHXuMeHslx2QcJiHRa4bfK5H5I!/m&ek=1&kp=1&pt=0&bo=AgECAQAAAAABFzA!&tl=3&vuin=3362045101&tm=1629057600&sce=60-3-3&rf=0-0,id=40000]')
    await score.send(msg)


self = on_regex('.*自我介绍.*', rule=to_me(), priority=15)

@self.handle()
async def get_self(bot: Bot, event: Event, state: T_State):
    await self.send('我叫呆呆，你们也可以叫我小呆，我是一个基于nonebot2跟cqhttp的QQ机器人，'
                    '我能帮你们查课表，查成绩，查青年大学习，查天气，查疫情实况，还可以定时发送课表，可以点歌.....你也可以@我回复‘帮助’既可以查看我的所有功能')



###########################################点歌########################################################


dinshiTable = on_regex('.*号课表.*', priority=4, block=True)

@dinshiTable.handle()
async def get_dinshiTable(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    date = ''.join(re.findall(r'[\d-]', msg))
    week = time.strptime(date, '%Y-%m-%d').tm_wday
    week_list = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    timetable = await get_timetable(date)
    table_list = timetable.split('\n\n')
    table = [table.split(':') for table in table_list]
    jsonContent = {
        "app": "com.tencent.miniapp",
        "desc": "",
        "view": "notification",
        "ver": "0.0.0.2",
        "prompt": "课表",
        "appID": "",
        "sourceName": "",
        "actionData": "",
        "actionData_A": "",
        "sourceUrl": "",
        "meta": {
            "notification": {
                "appInfo": {
                    "appName": "大数据2002",
                    "appType": 4,
                    "appid": 1109659848,
                    "iconUrl": "http://a1.qpic.cn/psc?/V52atmOK2u5JUK3FVE611ZbulV4a4WS4/ruAMsa53pVQWN7FLK88i5jqhYX6WhoAG88M3iRVZPNbcrVclVw9Fd5ssKP6HF6oyC89DQ3cI6po4l6BrsIYSmXS4XthMzvGks2TFMtzJeok!/c&ek=1&kp=1&pt=0&bo=gAKAAgAAAAABFzA!&tl=3&vuin=3362045101&tm=1629046800&sce=60-2-2&rf=0-0"
                },
                "data": [
                    {
                        "title": "第一节课",
                        "value": f"{table[0][1].replace('上课地点：', '')}"
                    },
                    {
                        "title": "第二节课",
                        "value": f"{table[1][1].replace('上课地点：', '')}"
                    },
                    {
                        "title": "第三节课",
                        "value": f"{table[2][1].replace('上课地点：', '')}"
                    },
                    {
                        "title": "第四节课",
                        "value": f"{table[3][1].replace('上课地点：', '')}"
                    },
                    {
                        "title": "晚一",
                        "value": f"{table[4][1].replace('上课地点：', '')}"
                    },
                    {
                        "title": "晚二",
                        "value": f"{table[5][1].replace('上课地点：', '')}"
                    },
                ],
                "title": f"{week_list[week]}课表",
                "button": [
                    {
                        "name": "湖南信息职业技术学院",
                        "action": ""
                    }
                ],
                "emphasis_keyword": ""
            }
        },
        "text": "",
        "sourceAd": ""
    }
    await time_table.send(MessageSegment.json(json.dumps(jsonContent)))



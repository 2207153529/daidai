import os
import re
from pathlib import Path

# import nonebot
from typing import Union

import nonebot
from nonebot import get_driver
from nonebot import on_command, on_message, on_startswith
from nonebot.permission import SUPERUSER
from nonebot.plugin import on, on_regex, require
from nonebot.rule import to_me, keyword
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event, Message
from nonebot.adapters.cqhttp import message, MessageSegment
from nonebot.config import Config
# from aiocqhttp import MessageSegment

# import bot
from .config import Config
import execjs
import requests
from PIL import Image, ImageFont, ImageDraw
from lxml import etree
# from data_source import image


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

BASE_PATH = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
IMG_PATH = os.path.join(BASE_PATH, 'plugins/image/table_pic.jpg')
fontPath = os.path.join(BASE_PATH, 'plugins/ZhengXinGeYingBiKaiShuJian-2.ttf')




async def image(
    img_name: Union[str, Path] = None, path: str = None, abspath: str = None, b64: str = None
) -> Union[MessageSegment, str]:
    """
    说明：
        生成一个 MessageSegment.image 消息
        生成顺序：绝对路径(abspath) > base64(b64) > img_name
    参数：
        :param img_name: 图片文件名称，默认在 resource/img 目录下
        :param path: 图片所在路径，默认在 resource/img 目录下
        :param abspath: 图片绝对路径
        :param b64: 图片base64
    """
    IMAGE_PATH = os.path.join(os.path.abspath(__file__).replace('\\', '/'), "plugins/image/")
    if abspath:
        return (
            MessageSegment.image("file:///" + abspath)
            if os.path.exists(abspath)
            else ""
        )
    elif isinstance(img_name, Path):
        if img_name.exists():
            return MessageSegment.image(f"file:///{img_name.absolute()}")
        return ""
    elif b64:
        return MessageSegment.image(b64 if "base64://" in b64 else "base64://" + b64)
    else:
        if "http" in img_name:
            return MessageSegment.image(img_name)
        if len(img_name.split(".")) == 1:
            img_name += ".jpg"
        file = (
            Path(IMAGE_PATH) / path / img_name if path else Path(IMAGE_PATH) / img_name
        )
        print(file)
        if file.exists():
            return MessageSegment.image(f"file:///{file.absolute()}")





async def get_margin(boxWidth, boxHeight, margin):
    """
    返回盒子内四个点的坐标
    """
    if len(margin) == 4:
        top, right, bottom, left = margin[0], margin[1], margin[2], margin[3]
    elif len(margin) == 2:
        top, right, bottom, left = margin[0], margin[1], margin[0], margin[1]
    elif len(margin) == 1:
        top, right, bottom, left = margin[0], margin[0], margin[0], margin[0]
    else:
        top, right, bottom, left = 50, 50, 50, 50
    a1 = (left, top)
    a2 = (boxWidth - right, top)
    a3 = (boxWidth - right, boxHeight - bottom)
    a4 = (left, boxHeight - bottom)
    return a1, a2, a3, a4



async def get_Table(week):
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
        'encoded': execjs.compile(jsText).call("encryptPass", '202027550202', 'Cyh@011029158118')
    }
    url = 'http://61.186.97.37:8081/jsxsd/xk/LoginToXk'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    session = requests.session()
    session.post(url, data=data, headers=headers)
    tableUrl = 'http://61.186.97.37:8081/jsxsd/xskb/xskb_list.do'
    tableData = {
        'zc': week,
        'xnxq01id': '2021-2022-1',
        'sfFD': 1,
        'wkbkc': 1,
        'kbjcmsid': '67FB3A89FDC146ADA865DCC81B9EC143'
    }
    response = session.post(tableUrl, headers=headers, data=tableData)
    if response.status_code == 200:
        html = etree.HTML(response.text)
        trList = html.xpath("//div[@class='content_box']//table[1]//tr")
        tableList = []
        for tr in trList[1:len(trList) - 1]:
            tdList = tr.xpath(".//td")
            tr_tableList = []
            for td in tdList:
                tableName = str(td.xpath(".//div[@class='kbcontent']/text()")).replace("\\xa0", "").strip("['']").split("与", 1)[0]
                teacherName = str(td.xpath(".//div[@class='kbcontent']//font[@title='教师']/text()")).replace("\\xa0", "").strip("['']").replace("其他", "")

                className = str(td.xpath(".//div[@class='kbcontent']//font[@title='教室']/text()")).replace("\\xa0", "").strip("['']").split("-", 2)
                if len(className) == 3:
                    className.pop()
                className = '-'.join(className)
                if className[-1:] != "M" and len(className) > 3:
                    className += 'M'
                tr_tableList.append(f"{tableName}\n{teacherName} \n{className}")
            tableList.append(tr_tableList)
        imageWidth = 3400
        imageHeight = 1400
        image = Image.new("RGB", (imageWidth, imageHeight), (255, 255, 255))
        font = ImageFont.truetype(fontPath, 50)
        bigFont = ImageFont.truetype(fontPath, 70)
        draw = ImageDraw.Draw(image)
        margin = 50
        # 绘制课表外框
        getmargin = await get_margin(imageWidth, imageHeight, [margin])
        draw.line(getmargin, fill='black', width=3)
        a1, a2, a3, a4 = await get_margin(imageWidth, imageHeight, [margin])
        draw.line([a4, a1], fill='black', width=3)
        # 绘制竖轴
        X_xAxis = [i * (imageWidth - margin * 2) / 8 + margin for i in range(1, 8)]

        # 绘制横轴
        Y_xAxis = [i * (imageHeight - margin * 2) / 7 + margin for i in range(1, 7)]

        table_X = [(margin + 50, i + 60) for i in Y_xAxis]
        table_Y = [(i + 40, margin + 50) for i in X_xAxis]

        week = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"]
        table_taggle = ['第一节', '第二节', '第三节', '第四节', '第五节', '第六节']
        # 绘制第一竖列
        for Axis in table_X:
            index = table_X.index(Axis)
            draw.text(Axis, table_taggle[index], fill='black', font=bigFont)
        # 绘制第一横列
        for Axis in table_Y:
            index = table_Y.index(Axis)
            draw.text(Axis, week[index], fill='black', font=bigFont)
        # 绘制斜线，写文本
        draw.line([(margin, margin), (X_xAxis[0], Y_xAxis[0])], fill='black', width=2)
        draw.text((150 + margin, 20 + margin), '星期', fill='black', font=font)
        draw.text((50 + margin, 100 + margin), '课次', fill='black', font=font)
        minBox_width = (imageWidth - margin * 2) / 8
        minBox_height = (imageHeight - margin * 2) / 7
        writeFont = ImageFont.truetype(fontPath, 50)
        for y in Y_xAxis:
            Yindex = Y_xAxis.index(y)
            for x in X_xAxis:
                Xindex = X_xAxis.index(x)
                if len(tableList[Yindex][Xindex]) > 10:
                    draw.polygon(
                        [(x + 1, y - 1), (x + 1 + minBox_width, y - 1), (x + 1 + minBox_width, y - 1 + minBox_height),
                         (x + 1, y - 1 + minBox_height)], fill=(212, 213, 216))
                draw.text((x + 20, y + 20), tableList[Yindex][Xindex], fill='black', font=writeFont)
        for i in range(7):
            draw.line([(X_xAxis[i], margin), (X_xAxis[i], imageHeight - margin)], fill='black', width=2)
        for i in range(6):
            draw.line([(margin, Y_xAxis[i]), (imageWidth - margin, Y_xAxis[i])], fill='black', width=2)
        filePath = os.path.join(BASE_PATH, 'table_pic.jpg')
        image.save(filePath)
        return filePath

table_pic = on_regex(r".*第.*周课表.*", priority=3, block=True)

@table_pic.handle()
async def send_table(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    week = int(re.findall(".*第(.*)周课表", msg)[0])
    if week < 1 or week > 30:
        await table_pic.send('参数有误')
    else:
        filePath = await get_Table(week)
        await table_pic.send(message.Message(MessageSegment.image(f'file:///{filePath}')))


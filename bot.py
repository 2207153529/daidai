#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from os import path
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot    # 需要自己导入
# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter('cqhttp', CQHTTPBot)    # 需要添加的配置
nonebot.load_builtin_plugins()
nonebot.load_from_toml("pyproject.toml")
nonebot.load_plugins('src/plugins/message/', 'src/plugins/table_pic/',  'src/plugins/check_update', 'src/pluginsnonebot_plugin_wordbank', 'src/plugins/nonebot_plugin_songpicker2', 'src/plugins/nonebot_plugin_status','src/plugins/nonebot_plugin_youthstudy/')


# Modify some config / config depends on loaded configs
#
# config = driver.config
# do something...
nonebot.init(apscheduler_autostart=True)
nonebot.init(apscheduler_config={
    "apscheduler.timezone": "Asia/Shanghai"
})





if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")

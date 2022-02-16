from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot import on_command
from pathlib import Path
from nonebot.rule import to_me
import platform
import os
import nonebot

update_zhenxun = on_command('检查更新小呆', permission=SUPERUSER, priority=1, block=True)

restart = on_command('重启', aliases={'restart'}, permission=SUPERUSER, rule=to_me(), priority=1, block=True)

driver = nonebot.get_driver()




@restart.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if str(platform.system()).lower() == 'windows':
        await restart.finish('暂无windows重启脚本...')


@restart.got('flag', prompt='确定是否重启小呆？（重启失败咱们将失去联系，请谨慎！）')
async def _(bot: Bot, event: MessageEvent, state: T_State):
    flag = state['flag']
    if flag.lower() in ['true', '是', '好']:
        await restart.send('开始重启小呆..请稍等...')
        open('is_restart', 'w')
        os.system('./restart.sh')
    else:
        await restart.send('已取消操作...')

@driver.on_bot_connect
async def remind(bot: Bot):
    is_restart_file = Path() / 'is_restart'
    if is_restart_file.exists():
        await bot.send_private_msg(
            user_id=int(list(bot.config.superusers)[0]),
            message=f"小呆重启完毕...",
        )
        is_restart_file.unlink()


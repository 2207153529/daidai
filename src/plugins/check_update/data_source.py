from aiohttp.client_exceptions import ClientConnectorError
from nonebot.adapters.cqhttp import Bot
from pathlib import Path
import ujson as json
import nonebot
import asyncio
import aiofiles
import aiohttp
import platform
import tarfile
import shutil
import os

if str(platform.system()).lower() == "windows":
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)


driver = nonebot.get_driver()

version_url = "https://github.com/HibiKier/zhenxun_bot/releases"
main_url = "https://github.com/HibiKier/zhenxun_bot"

_version_file = Path() / "__version__"
zhenxun_latest_tar_gz = Path() / "zhenxun_latest_file.tar.gz"
temp_dir = Path() / "temp"
backup_dir = Path() / "backup"


@driver.on_startup
def init():
    if str(platform.system()).lower() != "windows":
        restart = Path() / "restart.sh"
        if not restart.exists():
            with open(restart, "w", encoding="utf8") as f:
                f.write(
                    "pid=$(netstat -tunlp | grep " + "8080" + " | awk '{print $7}')\n"
                    "pid=${pid%/*}\n"
                    "kill -9 $pid\n"
                    "sleep 3\n"
                    "python3 bot.py"
                )
            os.system("chmod +x ./restart.sh")


# @driver.on_bot_connect
# async def remind(bot: Bot):
#     is_restart_file = Path() / 'is_restart'
#     if is_restart_file.exists():
#         await bot.send_private_msg(
#             user_id=int(list(bot.config.superusers)[0]),
#             message=f"小呆重启完毕...",
#         )
#         is_restart_file.unlink()



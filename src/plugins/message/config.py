from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here

    plugin_setting: str = "default"
    class Config:
        extra = "ignore"

class STATIC_VAL(object):
    # 祖安模式 1 打开 0 关闭
    MODE_ZUAN = '0'

    # 祖安功能 1 打开 0 关闭
    ZUAN_ON = '1'


    # 彩虹屁模式 1 打开 0 关闭
    CAI_HONG = '0'

    # 彩虹屁功能 1 打开 0 关闭
    CAIHONG_ON = '1'

    # QQ群号
    GROUP_ID = 808287102

    # 教务系统账号
    JW_USER = '202027550202'

    # 教务系统密码
    JW_PASSWORD = 'Cyh@011029158118'

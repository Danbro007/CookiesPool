from cookiepool.settings import ACCOUNTFILE
from cookiepool.db import RedisClient

conn = RedisClient("accounts", "weibo")


def account_set():
    with open(ACCOUNTFILE, "r", encoding="utf-8") as f:
        account_list = f.read().split("\n")
        for item in account_list:
            data = item.split("----")
            username = data[0]
            password = data[1]
            print("正在把账号%s存入redis数据库中" % username)
            conn.set(username, password)
if __name__ == '__main__':
    account_set()

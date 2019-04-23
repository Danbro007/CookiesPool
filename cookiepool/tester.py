import json

import requests

from cookiepool.settings import *
from cookiepool.db import RedisClient


class ValidTester:
    def __init__(self, website="default"):
        self.website = website
        self.account_db = RedisClient("accounts", self.website)
        self.cookies_db = RedisClient("cookies", self.website)

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookies_grpup = self.cookies_db.all()
        for username, cookies in cookies_grpup.items():
            self.test(username, cookies)


class WeiboValidTester(ValidTester):
    def __init__(self, website="weibo"):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print("正在测试用户%s的cookies" % username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print("用户%s的cookies不合法" % username)
            self.cookies_db.delete(username)
            print("删除用户%s的cookies！" % username)
            return
        try:
            test_url = TEST_URL_MAP["weibo"]
            response = requests.get(url=test_url, timeout=5, cookies=cookies, allow_redirects=False)
            if response.status_code == 200:
                print("用户%s的cookies有效")
            else:
                print("用户%s的cookies无效")
                print("删除用户%s的cookies！" % username)
                self.cookies_db.delete(username)
        except ConnectionError as e:
            print("发生异常！", e.args)


if __name__ == '__main__':
    tester = WeiboValidTester()
    tester.run()



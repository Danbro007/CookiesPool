from cookiepool.cookie_getters.weibo.weibo import WeiboCookie
from cookiepool.db import RedisClient
import json
from selenium import webdriver
from cookiepool.settings import *


class CookieGenderator:
    def __init__(self, website="default"):
        self.website = website
        self.cookie_db = RedisClient("cookies", self.website)
        self.account_db = RedisClient("accounts", self.website)
        self.init_browser()

    def init_browser(self):
        if BROWSER_TYPE == "Firefox":
            print("浏览器初始化")
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument('--headless')
            self.browser = webdriver.Firefox(firefox_options=firefox_options)
            # self.browser = webdriver.Firefox()
            self.browser.maximize_window()

    def new_cookies(self, username, password):
        raise NotImplementedError

    def process_cookies(self, cookies):
        dict = {}
        for cookie in cookies:
            if cookie["name"] == "SUB":
                dict["SUB"] = cookie["value"]
        return dict

    def run(self):
        account_usernames = self.account_db.usernames()
        cookies_usernames = self.cookie_db.usernames()
        for username in account_usernames:
            if username not in cookies_usernames:
                password = self.account_db.get(username)
                print("正在获取cookies,账号:%s,密码:%s" % (username, password))
                result = self.new_cookies(username, password)
                if result["status"] == 1:
                    cookies = self.process_cookies(result["content"])
                    print("成功获取到用户%s的cookies" % username)
                    self.cookie_db.set(username, json.dumps(cookies))
                    print("保存用户%s的cookies成功!" % username)
                elif result["status"] == 2:
                    if self.account_db.delete(username):
                        print("账号%s删除成功" % username)
                else:
                    print(result["content"])

    def close(self):
        self.browser.close()

    def __del__(self):
        try:
            print("正在关闭浏览器...")
            self.close()
            del self.browser
        except TypeError:
            print("浏览器未打开")


class WeiboCookieGenderator(CookieGenderator):
    def __init__(self, website="weibo"):
        CookieGenderator.__init__(self, website)
        self.website = website

    def new_cookies(self, username, password):
        return WeiboCookie(username, password, self.browser).main()


if __name__ == '__main__':
    weibo = WeiboCookieGenderator()
    weibo.run()

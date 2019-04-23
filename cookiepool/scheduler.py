import time
from multiprocessing import Process
from cookiepool.tester import WeiboValidTester
from cookiepool.settings import *
from cookiepool.tester import *
from cookiepool.generator import *
from cookiepool.api import app


class Scheduler:
    @staticmethod
    def valid_cookies(cycle=COOKIES_TESTER_CYCLE):
        while True:
            print("cookies测试器开启")
            try:
                for website, cls in TESTER_MAP.items():
                    tester = eval("{cls}(website='{website}')".format(cls=cls, website=website))
                    tester.run()
                    print("检测完成")
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def generate_cookies(cycle=COOKIES_GETTER_CYCLE):
        while True:
            print("cookies获取器开始")
            try:
                for website, cls in GETTER_MAP.items():
                    getter = eval("{cls}(website='{website}')".format(cls=cls, website=website))
                    getter.run()
                    print("cookies生成完成")
                    del getter
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        app.run(API_HOST, API_PORT)

    def run(self):
        if COOKIES_GETTER_ENABLE:
            getter_process = Process(target=Scheduler.generate_cookies)
            getter_process.start()
        if COOKIES_TESTER_ENABLE:
            tester_process = Process(target=Scheduler.valid_cookies)
            tester_process.start()
        if API_ENABLE:
            api_process = Process(target=Scheduler.api)
            api_process.run()


if __name__ == '__main__':
    s = Scheduler()
    s.run()

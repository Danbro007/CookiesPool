import os

# 登录url映射#
LOGIN_URL_MAP = {
    'weibo': 'http://my.sina.com.cn/profile/unlogin/'
}
# cookies测试url映射#
TEST_URL_MAP = {'weibo': 'https://m.weibo.cn/'}
# cookies测试组件#
TESTER_MAP = {"weibo": "WeiboValidTester"}
# cookies获取组件#
GETTER_MAP = {"weibo": "WeiboCookieGenderator"}
# 根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 账号列表路径
ACCOUNTFILE = os.path.join(BASE_DIR, "account_info.txt")
# Redis数据配置#
REDIS_PORT = 6379
REDIS_HOST = "localhost"
REDIS_PASSWORD = None
# 验证码下载地址
CAPTCHA_DIR = os.path.join(BASE_DIR, "cookiepool", "cookie_getters", "weibo", "captcha.png")
CAPTCHA_CODETYPE = 1005
PARSE_CAPTCHA_TIMEOUT = 60
# 云打码账号密码配置#

# selenium浏览器#
BROWSER_TYPE = "Firefox"
# cookies测试开关#
COOKIES_TESTER_ENABLE = True
# cookies测试周期#
COOKIES_TESTER_CYCLE = 3600
# cookies获取开关#
COOKIES_GETTER_ENABLE = True
# cookies获取周期#
COOKIES_GETTER_CYCLE = 120
#API配置#
API_HOST = "127.0.0.1"
API_PORT = 3300
API_ENABLE = True
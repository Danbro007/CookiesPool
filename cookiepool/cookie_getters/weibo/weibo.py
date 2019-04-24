import time
from io import BytesIO
from PIL import Image
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from cookiepool.settings import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from cookiepool.YMD import YDMHttp
from selenium.common.exceptions import ElementNotInteractableException, StaleElementReferenceException


class WeiboCookie:
    def __init__(self, username, password, browser):
        self.username = username
        self.password = password
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.url = LOGIN_URL_MAP["weibo"]
        self.yundama = YDMHttp(YDM_USERNAME, YDM_PASSWORD, YDM_APPID, YDM_APPKEY)

    def open(self):
        self.browser.get(self.url)
        self.browser.delete_all_cookies()
        try:
            login_button = self.wait.until(EC.element_to_be_clickable((By.ID, "hd_login")))
            login_button.click()
            time.sleep(1)
            username = self.wait.until(EC.presence_of_element_located((By.NAME, "loginname")))
            password = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            username.send_keys(self.username)
            time.sleep(1)
            password.send_keys(self.password)
            time.sleep(1)
        except Exception:
            self.open()
        try:
            submit_button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "login_btn")))
            captcha_input_box = self.wait.until(EC.presence_of_element_located((By.NAME, "door")))
            # time.sleep(10)
            captcha_num = self.parse_captcha()
            print(captcha_num)
            captcha_input_box.send_keys(captcha_num)
            submit_button.click()
        except (TimeoutException, StaleElementReferenceException):
            self.open()
        except Exception as e:
            print(e)
            pass
        if self.is_captcha_error():
            print("验证码解析错误,重新登录。")
            self.open()

    def get_screenshot(self):  # 获得验证码的截图
        screenshot = self.browser.get_screenshot_as_png()  # 截图用png截取
        screenshot = Image.open(BytesIO(screenshot))  # 用bytes打开图片
        return screenshot

    def get_position(self):  # 获取验证码图片的位置
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "yzm")))  # 出现验证码图片的html标签
        location = img.location  # 获取验证码图片的位置
        size = img.size  # 验证码图片的大小
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']  # 验证码图片的坐标
        return top, bottom, left, right

    def get_image(self):  # 获取验证码截图
        top, bottom, left, right = self.get_position()
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))  # 截取的图片
        captcha.save(CAPTCHA_DIR)
        print("成功获取到验证码图片")

    def parse_captcha(self):
        self.get_image()
        print("开始用云打码解析验证码")
        self.yundama.login()
        cid, result = self.yundama.decode(CAPTCHA_DIR, CAPTCHA_CODETYPE, PARSE_CAPTCHA_TIMEOUT)
        return result

    def is_switch_successful(self):
        try:
            bool(self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pms"))))
        except TimeoutException:
            return False

    def is_captcha_error(self):
        try:
            return bool(WebDriverWait(self.browser, 5).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "login_error_tips"), "输入的验证码不正确")))
        except TimeoutException:
            return False

    def get_cookie(self):
        return self.browser.get_cookies()

    def is_password_error(self):
        try:
            return WebDriverWait(self.browser, 5).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "login_error_tips"), "登录名或密码错误"))
        except TimeoutException:
            return False

    def login_successful(self):
        try:
            return bool(
                WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.ID, "search_input"))))
        except TimeoutException:
            print("登录失败")
            return False

    def main(self):
        self.open()
        if self.is_password_error():
            return {
                "status": 2,
                "content": "用户名或者密码错误"
            }
        if self.login_successful():
            self.browser.get("https://weibo.cn/")
            if self.is_switch_successful:
                cookies = self.get_cookie()
                self.browser.delete_all_cookies()
                return {
                    "status": 1,
                    "content": cookies
                }
            else:
                self.main()

        else:
            return {
                "status": 3,
                "content": "登录失败"
            }


if __name__ == '__main__':
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--headless')
    browser = webdriver.Firefox(firefox_options=firefox_options)
    # browser = webdriver.Firefox()
    browser.maximize_window()
    weibo = WeiboCookie("vdqj93649753@vip.sina.com", "dtn778frx", browser)
    res = weibo.main()
    print(res)

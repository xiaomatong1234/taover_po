import allure
import yaml
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from taover_po.base.error_popups import black_wrapper
from taover_po.utils.log_util import logger
from taover_po.utils.util import Util


class BasePage:
    def __init__(self, driver: WebDriver=None):
        if driver:
            self.driver = driver
        else:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")  # 容器环境必须参数
            options.add_argument("--disable-dev-shm-usage")  # 容器环境必须参数
            
            # 使用检测到的正确路径
            service = Service(executable_path="/usr/bin/chromedriver")
            self.driver = webdriver.Chrome(options=options, service=service)
            self.driver.implicitly_wait(10)
            self.driver.maximize_window()
            try:
                # 添加cookies信息
                self.driver.get('http://wxorder.taover.com/dashboard')
                cookies = yaml.safe_load(open('../data/cookies.yaml'))
                for c in cookies:
                    self.driver.add_cookie(c)
                logger.info('添加cookies信息')
                self.driver.get('http://wxorder.taover.com/dashboard')
                logger.info('开始调用......')
            except FileNotFoundError:
                # 如果cookies文件不存在，先获取cookies
                self._get_cookie()

    def _get_cookie(self):
        # 获取cookies并保存
        try:
            self.driver.get('http://wxorder.taover.com/login?redirect=%2Fgoods%2Fgoods-list')
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//span[text()="首页"]'))
            )
            cookie = self.driver.get_cookies()
            with open('../data/cookies.yaml', 'w', encoding='utf-8') as f:
                yaml.safe_dump(cookie, f)
            # 重新加载页面并添加cookies
            self.driver.get('http://wxorder.taover.com/dashboard')
            for c in cookie:
                self.driver.add_cookie(c)
            self.driver.get('http://wxorder.taover.com/dashboard')
        except TimeoutException:
            print('登录超时，请检查登录流程')

    @black_wrapper
    def find_ele(self,by,value):
        ele = self.driver.find_element(by, value)
        return ele

    @black_wrapper
    def find_eles(self,by,value):
        eles = self.driver.find_elements(by, value)
        return eles

    @black_wrapper
    def find_ele_click(self,by,value):
        self.find_ele(by,value).click()

    @black_wrapper
    def find_ele_input(self,by,value,text):
        self.find_ele(by,value).clear()
        self.find_ele(by,value).send_keys(text)

    @black_wrapper
    def find_eles_input(self,by,value,text,index):
        eles = self.find_eles(by, value)
        if index > len(eles):
            raise IndexError
        eles[index].clear()
        eles[index].send_keys(text)

    def scroll_to_end(self):
        ActionChains(self.driver).send_keys(Keys.END).perform()
        return self


    def switch_to_win(self,win_index):
        handles = self.driver.window_handles
        if win_index < len(handles):
            self.driver.switch_to.window(handles[win_index])
        else:
            raise IndexError(f'窗口索引超出{win_index}范围，当前只有{len(handles)}个窗口')
        return self

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
        return self

    def set_imp_wait(self,time=20):
        self.driver.implicitly_wait(time)

    def set_web_wait_located(self,by,value):
        WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((by, value)))

    def set_web_wait_visible(self,by,value):
        WebDriverWait(self.driver,10).until(
            EC.visibility_of_element_located((by, value))
        )

    def set_web_wait_text(self,by,value,text):
        WebDriverWait(self.driver,10).until(
            EC.text_to_be_present_in_element((by, value),text_=text)
        )

    def set_web_wait_click(self,by,value):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by,value))
        )

    def save_screenshot(self):
        image_path = Util.save_source_data("images")
        self.driver.save_screenshot(image_path)
        return image_path # 返回截图路径

    def save_pagesource(self):
        pagesource_path = Util.save_source_data("pagesource")
        with open(pagesource_path, "w") as f:
            f.write(self.driver.page_source)
        return pagesource_path

    def quit(self):
        self.driver.quit()
        logger.info('结束调用........')


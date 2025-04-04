import time

import yaml
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestGoodManage:
    def setup_method(self):
        option =Options()
        service = Service('/usr/local/bin/chromedriver')
        self.driver = webdriver.Chrome(options=option,service=service)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        try:
            # 添加cookies信息
            self.driver.get('http://wxorder.taover.com/dashboard')
            cookies = yaml.safe_load(open('data/cookies.yaml'))
            for c in cookies:
                self.driver.add_cookie(c)
            self.driver.get('http://wxorder.taover.com/dashboard')
            # # 点击商品管理
            # self.driver.find_element(By.XPATH, '//span[text()="商品管理"]').click()
            # # 点击商品列表
            # self.driver.find_element(By.XPATH, '//span[text()="商品列表"]').click()
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
            with open('data/cookies.yaml', 'w', encoding='utf-8') as f:
                yaml.safe_dump(cookie, f)
            # 重新加载页面并添加cookies
            self.driver.get('http://wxorder.taover.com/dashboard')
            for c in cookie:
                self.driver.add_cookie(c)
            self.driver.get('http://wxorder.taover.com/dashboard')
        except TimeoutException:
            print('登录超时，请检查登录流程')

    def teardown_method(self):
        self.driver.quit()

    def test_add_good(self):
        # 点击添加按钮
        self.driver.find_element(By.XPATH,'(//span[text()="添加"])[1]').click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'//label[@for="goodsName"]'))
        )
        self.driver.find_element(By.XPATH,'//label[@for="goodsName"]/following-sibling::*/*/*').send_keys('rt3')

        # 选择所属仓库(供应商)
        self.driver.find_element(By.CSS_SELECTOR,'.el-select.inputWidth input').click()

        # 选择下拉框中的 测吧测试1八爪云仓库1
        self.driver.find_element(By.XPATH,'//span[text()="测吧测试1八爪云仓库1"]').click()


        # 滚动到页面底部
        ActionChains(self.driver).send_keys(Keys.END).perform()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'(//input[@class="el-input__inner"])[6]'))
        )
        # 添加规格名称
        eles = self.driver.find_elements(By.CSS_SELECTOR,'.el-input__inner')
        eles[6].send_keys('rt3')
        # self.driver.find_element(By.XPATH,'(//input[@class="el-input__inner"])[6]').send_keys('rt3')
        # 点击提交
        self.driver.find_element(By.XPATH,'//span[text()="提交"]').click()
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH,'//p[text()="创建成功"]'), '创建成功')
        )
        # 断言 创建成功
        res = self.driver.find_element(By.XPATH,'//p[text()="创建成功"]').text
        good_lst = self.driver.find_elements(By.CSS_SELECTOR,'.col-12>span')
        good = [good.text for good in good_lst]
        assert "创建成功" in res
        assert 'rt3' in good

    def test_search_good(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'.el-input>input.el-input__inner'))
        )
        # 查询商品
        self.driver.find_element(By.XPATH,'//input[@placeholder="请输入商品名称"]').send_keys('rt3')

        # 点击查询
        self.driver.find_element(By.XPATH,'//span[text()="查询"]').click()
        time.sleep(5)
        good_lst = self.driver.find_elements(By.CSS_SELECTOR,'.col-12')
        good = [good.text for good in good_lst]
        assert 'rt3' in good

    def test_modify_good(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.el-input>input.el-input__inner'))
        )
        # 查询商品
        self.driver.find_element(By.XPATH, '//input[@placeholder="请输入商品名称"]').send_keys('rt3')

        # 点击查询
        self.driver.find_element(By.XPATH, '//span[text()="查询"]').click()

        # 关闭常见问题
        self.driver.find_element(By.CSS_SELECTOR, '.el-icon-close.inline-block.absolute').click()

        # 点击修改按钮
        self.driver.find_element(By.XPATH, '//span[text()="修改"]').click()
        # 切换句柄
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])

        time.sleep(5)

        # 修改商品名称
        ele = self.driver.find_element(By.CSS_SELECTOR, '.el-form-item.mt3 div input')
        ele.clear()
        ele.send_keys('rt3_update')

        # 滚动到页面底部
        ActionChains(self.driver).send_keys(Keys.END).perform()
        # 点击提交
        self.driver.find_element(By.XPATH, '//span[text()="提交"]').click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'//span[text()="商品列表"]'))
        )
        # 返回至商品列表页
        self.driver.switch_to.default_content()
        res = self.driver.find_element(By.XPATH, '//p[text()="修改成功"]')
        time.sleep(2)
        assert '修改成功' in res.text

        # 断言修改的内容在列表中
        good_lst = self.driver.find_elements(By.CSS_SELECTOR, '.col-12')
        good = [good.text for good in good_lst]
        assert 'rt3_update' in good

    def test_delete_good(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.el-input>input.el-input__inner')))
        # 查询商品
        self.driver.find_element(By.XPATH, '//input[@placeholder="请输入商品名称"]').send_keys('rt3')
        # 点击查询
        self.driver.find_element(By.XPATH, '//span[text()="查询"]').click()

        # 点击查询
        time.sleep(5)
        good_lst = self.driver.find_elements(By.CSS_SELECTOR, '.col-12')
        good = [good.text for good in good_lst]
        if 'rt3_update' in good:
            # 关闭常见问题
            self.driver.find_element(By.CSS_SELECTOR, '.el-icon-close.inline-block.absolute').click()
            # 点击下架按钮
            self.driver.find_element(By.XPATH,'//span[text()="下架"]').click()
            # 默认页面，点击提交
            self.driver.find_element(By.XPATH,'//span[text()="提交"]').click()
            time.sleep(2)
            res = self.driver.find_element(By.XPATH, '//p[text()="操作成功"]')
            assert '操作成功' in res.text
        else:
            print('商品名称不存在')







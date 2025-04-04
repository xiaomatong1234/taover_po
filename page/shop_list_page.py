import time

from selenium.webdriver.common.by import By

from taover_po.base.base_page import BasePage
from taover_po.page.add_shop_page import AddShopPage
from taover_po.utils.log_util import logger


class ShopListPage(BasePage):
    _ADD_BT = (By.XPATH, '(//span[text()="添加"])[1]')
    _CREATE_SUCCESS_TEXT = (By.XPATH, '//p[text()="创建成功"]')
    _GOOD_NAME = (By.CSS_SELECTOR, '.el-input>input.el-input__inner')
    _INPUT_GOOD_NAME = (By.XPATH, '//input[@placeholder="请输入商品名称"]')
    _SEARCH_BT = (By.XPATH, '//span[text()="查询"]')
    _GOOD_LIST = (By.CSS_SELECTOR, '.col-12')
    _CLOSE_BT = (By.CSS_SELECTOR, '.el-icon-close.inline-block.absolute')
    _MODIFY_BT = (By.XPATH, '//span[text()="修改"]')
    _GOODS_LIST_NAME = (By.XPATH, '//span[text()="商品列表"]')
    _MODIFY_SUCCESS_TEXT = (By.XPATH, '//p[text()="修改成功"]')
    _SHELVES_BT = (By.XPATH, '//span[text()="下架"]')
    _SUBMIT_BT = (By.XPATH, '//span[text()="提交"]')
    _SHELVES_SUCCESS_TEXT = (By.XPATH, '//p[text()="操作成功"]')

    def go_add_shop_page(self):
        self.find_ele_click(*self._ADD_BT) # 点击添加按钮
        return AddShopPage(self.driver)


    def verify_add_shop_pass(self,text):
        self.set_web_wait_text(*self._CREATE_SUCCESS_TEXT,text=text) # '创建成功'

        # 断言 创建成功
        res = self.find_ele(*self._CREATE_SUCCESS_TEXT).text
        # good_lst = self.driver.find_elements(By.CSS_SELECTOR, '.col-12>span')
        # good = [good.text for good in good_lst]
        add_shop_pass_png = self.save_screenshot()
        logger.info(f'添加商品成功，截图路径：{add_shop_pass_png}')
        return res

    def search_good(self,good_name):
        self.set_web_wait_located(*self._GOOD_NAME)
        self.find_ele_input(*self._INPUT_GOOD_NAME,text=good_name) # 查询商品rt3
        self.find_ele_click(*self._SEARCH_BT) # 点击查询

        time.sleep(10)
        # self.set_web_wait_located(*self._GOOD_LIST)
        good_lst = self.find_eles(*self._GOOD_LIST)
        good = [good.text for good in good_lst]

        search_shop_pass_png = self.save_screenshot()
        logger.info(f'查询商品成功，截图路径：{search_shop_pass_png}')
        return good

    def search_good_name(self,good_name):
        self.set_web_wait_located(*self._GOOD_NAME)
        self.find_ele_input(*self._INPUT_GOOD_NAME, text=good_name)  # 查询商品
        self.find_ele_click(*self._SEARCH_BT)  # 点击查询
        time.sleep(5)
        return self


    def go_modify_shop_page(self):

        self.find_ele_click(*self._CLOSE_BT)  # 关闭常见问题
        self.find_ele_click(*self._MODIFY_BT)   # 点击修改按钮


        self.switch_to_win(1) # 切换句柄
        from taover_po.page.modify_shop_page import ModifyShopPage
        return ModifyShopPage(self.driver)


    def verify_modify_shop_pass(self,text):
        self.set_web_wait_located(*self._GOODS_LIST_NAME) # 返回至商品列表页
        self.switch_to_default_content()  # 切换回默认页面
        res = self.find_ele(*self._MODIFY_SUCCESS_TEXT).text
        self.set_web_wait_text(*self._MODIFY_SUCCESS_TEXT, text=text)  # '修改成功'
        # good_lst = self.driver.find_elements(By.CSS_SELECTOR, '.col-12')
        # good = [good.text for good in good_lst]

        modify_shop_pass_png = self.save_screenshot()
        logger.info(f'修改商品成功，截图路径：{modify_shop_pass_png}')
        return res

    def delete_good(self):
        self.find_ele_click(*self._SHELVES_BT) # 点击下架按钮
        self.find_ele_click(*self._SUBMIT_BT) # 默认页面，点击提交
        time.sleep(2)
        res = self.find_ele(*self._SHELVES_SUCCESS_TEXT).text

        delete_shop_pass_png = self.save_screenshot()
        logger.info(f'删除商品成功，截图路径：{delete_shop_pass_png}', )
        return res



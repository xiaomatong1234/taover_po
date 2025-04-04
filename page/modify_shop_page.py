import time

from selenium.webdriver.common.by import By

from taover_po.base.base_page import BasePage
from taover_po.page.shop_list_page import ShopListPage


class ModifyShopPage(BasePage):
    _SHOP_NAME = (By.CSS_SELECTOR, '.el-form-item.mt3 div input')
    _SUBMIT_BT = (By.XPATH, '//span[text()="提交"]')


    def modify(self,update_good_name):
        time.sleep(5)
        self.find_ele_input(*self._SHOP_NAME,text=update_good_name) # 修改商品名称
        self.scroll_to_end() # 滚动到页面底部
        self.find_ele_click(*self._SUBMIT_BT) # 点击提交
        return ShopListPage(self.driver)
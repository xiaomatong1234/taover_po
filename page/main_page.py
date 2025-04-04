from selenium.webdriver.common.by import By
from taover_po.base.base_page import BasePage
from taover_po.page.shop_list_page import ShopListPage


class MainPage(BasePage):
    _SHOP_MANAGER_BT = (By.XPATH, '//span[text()="商品管理"]')
    _SHOP_LIST_BT = (By.XPATH, '//span[text()="商品列表"]')


    def go_shop_list_page(self):
        self.find_ele_click(*self._SHOP_MANAGER_BT) # 点击商品管理
        self.find_ele_click(*self._SHOP_LIST_BT)  # 点击商品列表
        return ShopListPage(self.driver)

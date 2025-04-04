from selenium.webdriver.common.by import By
from taover_po.base.base_page import BasePage


class AddShopPage(BasePage):
    _GOODNAME = (By.XPATH, '//label[@for="goodsName"]')
    _INPUT_SHOP_NAME = (By.XPATH, '//label[@for="goodsName"]/following-sibling::*/*/*')
    _SELECT_WAREHOUSE = (By.CSS_SELECTOR, '.el-select.inputWidth input')
    _SELECT_WAREHOUSE_NAME = (By.XPATH, '//span[text()="测吧测试1八爪云仓库1"]') # 错误
    _SIZE_NAME = (By.CSS_SELECTOR, '.el-input__inner')
    _SUBMIT_BT = (By.XPATH, '//span[text()="提交"]')
    _DROP_PIC = (By.CSS_SELECTOR, '.el-upload.el-upload--picture-card')
    _ORDER_STATUS = (By.XPATH,"//span[text()='进入待审核']/preceding-sibling::*")  # 切换订单状态
    _COST_PRICE = (By.CSS_SELECTOR, '.el-input__inner')
    _AMOUNT = (By.CSS_SELECTOR, '.el-input__inner')

    def add(self,good_name,index,size_name):
        self.set_web_wait_located(*self._GOODNAME)
        self.find_ele_input(*self._INPUT_SHOP_NAME,text=good_name) # 输入商品名称'rt3'

        self.find_ele_click(*self._SELECT_WAREHOUSE)  # 选择所属仓库(供应商)
        self.find_ele_click(*self._SELECT_WAREHOUSE_NAME)   # 选择下拉框中的 测吧测试1八爪云仓库1

        self.scroll_to_end() # 滚动到页面底部
        self.set_web_wait_located(*self._SIZE_NAME)
        self.find_eles_input(*self._SIZE_NAME,index=index,text=size_name) # 添加规格名称'rt3' 索引6

        self.find_ele_click(*self._SUBMIT_BT) # 点击提交
        from taover_po.page.shop_list_page import ShopListPage
        return ShopListPage(self.driver)

    def add_all(self):
        self.set_web_wait_located(*self._GOODNAME)
        self.find_ele_input(*self._INPUT_SHOP_NAME, text='rt3')  # 输入商品名称'rt3'
        self.find_ele_click(*self._DROP_PIC) # 选择图片 这块有问题
        self.find_ele_click(*self._ORDER_STATUS) # 切换订单处理方式 待审核状态
        self.find_ele_click(*self._SELECT_WAREHOUSE)  # 选择所属仓库(供应商)
        self.scroll_to_end()  # 滚动到页面底部
        self.set_web_wait_located(*self._SIZE_NAME)
        self.find_eles_input(*self._SIZE_NAME, index=6, text='rt3')  # 添加规格名称'rt3' 索引6
        self.find_eles_input(*self._COST_PRICE, index=8, text=12)  #  索引8， 12
        self.find_eles_input(*self._AMOUNT, index=9, text=13)  #  索引9， 13
        self.find_ele_click(*self._SUBMIT_BT)  # 点击提交
        from taover_po.page.shop_list_page import ShopListPage
        return ShopListPage(self.driver)
import allure
import pytest

from taover_po.page.main_page import MainPage
from taover_po.utils.util import Util


@allure.feature('商品列表模块')
class TestGoodManage:
    def setup_method(self):
        main_page = MainPage()
        self.shop_list_page = main_page.go_shop_list_page()

    def teardown_method(self):
        self.shop_list_page.quit()

    # 添加商品
    add_case_pass = Util.get_yaml(Util.get_file_path('data/add_goods.yaml'))['add_goods'][0]
    @allure.story('添加商品功能')
    @allure.title('成功添加商品')
    @pytest.mark.parametrize(
        'good_name,index,size_name,text',
        [(add_case_pass['good_name'],add_case_pass['index'],add_case_pass['size_name'],add_case_pass['text'])],
        ids=[add_case_pass['good_name']]
    )
    def test_add_good(self,good_name,index,size_name,text):
        res = self.shop_list_page\
            .go_add_shop_page()\
            .add(good_name,index,size_name)\
            .verify_add_shop_pass(text)
        assert "创建成功" in res

    # 搜索商品
    search_case_pass = Util.get_yaml(Util.get_file_path('data/search_goods.yaml'))['search_goods'][0]
    @pytest.mark.parametrize(
        'good_name',[search_case_pass['good_name']],
        ids=[search_case_pass['good_name']]
    )
    @allure.story('查询商品功能')
    @allure.title('在列表中成功查询商品rt3')
    def test_search_good(self,good_name):
        res = self.shop_list_page\
            .search_good(good_name)
        assert good_name in res

    # 修改商品
    modify_case_pass = Util.get_yaml(Util.get_file_path('data/modify_goods.yaml'))['modify_goods_name'][0]
    @pytest.mark.parametrize(
        'good_name,update_good_name,text',
        [(modify_case_pass['good_name'],modify_case_pass['update_good_name'],modify_case_pass['text'])],
        ids=[modify_case_pass['good_name']]
    )
    @allure.story('修改商品功能')
    @allure.title('在列表中查询商品rt3,并修改为rt3_update')
    def test_modify_good(self,good_name,update_good_name,text):
        res = self.shop_list_page\
            .search_good_name(good_name)\
            .go_modify_shop_page()\
            .modify(update_good_name)\
            .verify_modify_shop_pass(text)
        assert '修改成功' in res

    # 删除商品
    delete_case_pass = Util.get_yaml(Util.get_file_path('data/delete_goods.yaml'))['delete_goods_name'][0]
    @pytest.mark.parametrize(
        'good_name',
        [delete_case_pass['good_name']],
        ids=[delete_case_pass['good_name']]
    )
    @allure.story('删除商品功能')
    @allure.title('在列表中查询商品rt3_update,并删除rt3_update')
    def test_delete_good(self,good_name):
        res = self.shop_list_page\
            .search_good_name(good_name)\
            .delete_good()
        assert '操作成功' in res


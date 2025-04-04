import allure

from taover_po.utils.log_util import logger

black_lst = []

def black_wrapper(fun):
    def run(*args, **kwargs):
        basepage = args[0]
        try:
            logger.info(f'查找元素定位方式: {args[1]}, 定位元素: {args[2]}')
            basepage.set_imp_wait(20)
            return fun(*args, **kwargs)
        except Exception as e:
            basepage.set_imp_wait(1)
            logger.warning(f'没有找到元素{e}，定位方式: {args[1]}, 定位元素: {args[2]}')

            image_path = basepage.save_screenshot()
            allure.attach.file(
                image_path,
                name='查找元素异常截图',
                attachment_type=allure.attachment_type.PNG
            )
            pagesource_path = basepage.save_pagesource()
            allure.attach.file(
                pagesource_path,
                name='查找元素异常页面源码',
                attachment_type=allure.attachment_type.HTML
            )

            for b in black_lst:
                eles = basepage.driver.find_elements(*b)
                if len(eles) > 0:
                    eles[0].click()
                    basepage.set_imp_wait(20)
            return fun(*args, **kwargs)
        finally:
            basepage.set_imp_wait(20)
    return run

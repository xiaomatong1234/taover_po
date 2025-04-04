import os
import time
import yaml
from taover_po.conftest import root_path
from taover_po.utils.log_util import logger


class Util:
    @classmethod
    def get_file_path(cls,path_name):
        path = os.sep.join([root_path, path_name])
        logger.info(f'文件的绝对路径是：{path}')
        return path

    @classmethod
    def get_yaml(cls,yaml_path):
        try:
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
            return data
        except Exception as e:
            logger.info(f'报错信息{e}')


    @classmethod
    def get_current_time(cls):
        return time.strftime('%Y%m%d%H%M%S')

    @classmethod
    def save_source_data(cls,source_type):
        if source_type == 'images':
            end='.png'
            path = 'images'
        elif source_type == 'pagesource':
            end = '.html'
            path = 'page_sources'

        else:
            return None

        source_name = Util.get_current_time() + end # 文件名称
        source_dir_path = os.sep.join([root_path, path]) # 文件路径
        if not os.path.exists(source_dir_path):
            os.mkdir(source_dir_path)
        source_path = os.sep.join([source_dir_path, source_name])  # 拼接资源保存的绝对路径
        logger.info(f'资源保存的绝对路径：{source_path}')
        return source_path

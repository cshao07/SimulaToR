# -*- coding: utf-8 -*-

import os
import shutil

"""
Created on Tue Nov 19 12:49:25 2019

@author: xiaozhutousan
"""

__all__ = ['check_dir', 'sort_dir']


def check_dir(Dir):
    if os.path.isdir(Dir):
        dir_path = os.path.abspath(Dir)
        if os.listdir(Dir):
            shutil.rmtree(dir_path)  # 删除文件夹
            os.mkdir(dir_path)  # 创建文件夹
    else:
        os.mkdir(Dir)  # 创建文件夹
        dir_path = os.path.abspath(Dir)
    return dir_path  # 返回文件绝对路径


def sort_dir(Dir):
    if os.path.isdir(Dir):
        Dir = os.path.abspath(Dir)
        if os.listdir(Dir):  # 检查目录是否为空
            for file in os.listdir(Dir):
                if os.path.isdir(file):  # 检查目录下是否包含子文件夹
                    print('%s目录中包含子文件夹' % Dir)
                    quit()
            mac_DS = '%s%s%s' % (Dir, '/', '.DS_Store')
            if os.path.exists(mac_DS):
                os.remove(mac_DS)
            Dir = sorted(os.listdir(Dir))
        else:
            print('%s是一个空文件夹！' % Dir)
            quit()
    else:
        print('%s文件夹不存在！' % Dir)
        quit()
    return Dir


__name__ = 'dir_func'

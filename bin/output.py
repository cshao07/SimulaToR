# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
Created on Tue Nov 19 12:49:25 2019

@author: xiaozhutousan
"""

__all__ = ['out_sample', 'out_combined']

import pandas as pd


def out_sample(list1, list2, list3, list4, outDir, sample_name):
    """
    产生个体输出到CSV格式文件
    """
    df = pd.DataFrame(None, columns=['Sample Name', 'Marker', 'Allele 1', 'Allele 2'], dtype=str)
    df.loc[:, 'Sample Name'] = list1
    df.loc[:, 'Marker'] = list2
    df.loc[:, 'Allele 1'] = list3
    df.loc[:, 'Allele 2'] = list4
    df.to_csv('%s%s%s' % (outDir, '/', sample_name), index=False, sep=",", encoding="utf-8")


def out_combined_nfs(list1, list2, outDir):
    """
    多个计算结果统计到单个文件
    """
    df = pd.DataFrame(None)
    df.loc[:, 'Name'] = list1
    df.loc[:, 'lgLR'] = list2
    df.to_csv(outDir, index=False, sep=",", encoding="utf-8")


def out_combined_fs(list1, list2, list3, outDir):
    """
    多个计算结果统计到单个文件
    """
    df = pd.DataFrame(None)
    df.loc[:, 'Name'] = list1
    df.loc[:, 'lgLR'] = list2
    df.loc[:, 'IBS'] = list3
    df.to_csv(outDir, index=False, sep=",", encoding="utf-8")
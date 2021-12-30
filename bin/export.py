# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
Usage:
    SimulaToR export [options] [-n NUMBER|-m MARKER_FILE] -r PATH

Options:
    -h --help                       Show help message.
    -v --version                    Show version.
    -r PATH --result_path=PATH      Providing dictionary contains calculation results.
    -n N --number_mode=N            Provide numbers of random markers for calculation.
    -m FILE --marker_mode=FILE      Provide list of markers for calculation. [default: marker_list.csv]
    -o OUT --output=OUT             Output directory. [default: PATH.csv]
    --FS                            For full sibling pairs, export ibs values as well. [default: FALSE]
"""

import pandas as pd
import os
import sys
import math
import random
from bin import logger, dir_func, output, sample

"""
Created on Tue Nov 19 13:08:43 2019

@author: xiaozhutousan
"""

__all__ = ['export']


@logger.logger
def export(options):
    if options['--FS']:
        if options['--number_mode']:
            try:
                n = int(options['--number_mode'])
                export_cal_random_fs(options['--result_path'], n, options['--output'])
            except ValueError:
                sys.exit('Error: Only integer parameter can be recognized in number mod')
        elif options['--marker_mode']:
            if os.path.exists(options['--marker_mode']):
                export_cal_marker_fs(options['--result_path'], options['--marker_mode'], options['--output'])
            else:
                sys.exit('Error: Marker list file for marker mode does NOT exist!')
    else:
        if options['--number_mode']:
            try:
                n = int(options['--number_mode'])
                export_cal_random_nfs(options['--result_path'], n, options['--output'])
            except ValueError:
                sys.exit('Error: Only integer parameter can be recognized in number mod')
        elif options['--marker_mode']:
            if os.path.exists(options['--marker_mode']):
                export_cal_marker_nfs(options['--result_path'], options['--marker_mode'], options['--output'])
            else:
                sys.exit('Error: Marker list file for marker mode does NOT exist!')


def export_cal_marker_fs(resultDir, marker_file, outFile):
    print('Exporting calculate results by marker list...')
    results = dir_func.sort_dir(resultDir)
    marker_df = pd.read_csv(marker_file, header=0, index_col=None, dtype=str)
    marker_list = list(marker_df.iloc[:, 0])
    name_list = []
    ITO_list = []
    IBS_list = []
    for i in results:
        ITO = 1
        IBS = 0
        for j in marker_list:
            a = sample.load_result_fs('%s%s%s' % (resultDir, '/', i), j)
            ITO = ITO * a.ito
            IBS = IBS + a.ibs
        name_list.append('%s%s%s' % (i, '_list_by_', marker_file))
        lg_ITO = math.log(ITO, 10)
        ITO_list.append(lg_ITO)
        IBS_list.append(IBS)
    output.out_combined_fs(name_list, ITO_list, IBS_list, outFile)


def export_cal_random_fs(resultDir, N, outFile):
    print('Exporting calculate results by random...')
    # 导出列表中随机数量位点的Combined ito/ibs
    results = dir_func.sort_dir(resultDir)
    name_list = []
    ITO_list = []
    IBS_list = []
    for i in results:
        ITO = 1
        IBS = 0
        df = pd.read_csv('%s%s%s' % (resultDir, '/', i), header=0, index_col='Marker',
                         dtype={'LR': float, 'ibs': int})
        marker_list = list(df.index)
        while N > len(marker_list):
            marker_list = list(marker_list + marker_list)
        for j in random.sample(marker_list, N):
            a = sample.load_result_fs('%s%s%s' % (resultDir, '/', i), j)
            ITO = ITO * a.ito
            IBS = IBS + a.ibs
        name_list.append('%s%s%s' % (i, '_random_', N))
        lg_ITO = math.log(ITO, 10)
        ITO_list.append(lg_ITO)
        IBS_list.append(IBS)
        output.out_combined_fs(name_list, ITO_list, IBS_list, outFile)


def export_cal_marker_nfs(resultDir, marker_file, outFile):
    print('Exporting calculate results by marker list...')
    results = dir_func.sort_dir(resultDir)
    marker_df = pd.read_csv(marker_file, header=0, index_col=None, dtype=str)
    marker_list = list(marker_df.iloc[:, 0])
    name_list = []
    ITO_list = []
    for i in results:
        ITO = 1
        for j in marker_list:
            a = sample.load_result_nfs('%s%s%s' % (resultDir, '/', i), j)
            ITO = ITO * a.ito
        name_list.append('%s%s%s' % (i, '_list_by_', marker_file))
        lg_ITO = math.log(ITO, 10)
        ITO_list.append(lg_ITO)
    output.out_combined_nfs(name_list, ITO_list, outFile)


def export_cal_random_nfs(resultDir, N, outFile):
    print('Exporting calculate results by random...')
    # 导出列表中随机数量位点的Combined ito/ibs
    results = dir_func.sort_dir(resultDir)
    name_list = []
    ITO_list = []
    for i in results:
        ITO = 1
        df = pd.read_csv('%s%s%s' % (resultDir, '/', i), header=0, index_col='Marker',
                         dtype={'LR': float, 'ibs': int})
        marker_list = list(df.index)
        while N > len(marker_list):
            marker_list = list(marker_list + marker_list)
        for j in random.sample(marker_list, N):
            a = sample.load_result_nfs('%s%s%s' % (resultDir, '/', i), j)
            ITO = ITO * a.ito
        name_list.append('%s%s%s' % (i, '_random_', N))
        lg_ITO = math.log(ITO, 10)
        ITO_list.append(lg_ITO)
        output.out_combined_nfs(name_list, ITO_list, outFile)
# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
Usage:
    SimulaToR kde [options] -0 RESULT0 -1 RESULT1 -o OUT

Options:
    -h --help                       Show help message.
    -v --version                    Show version.
    -0 RESULT0 --result0=RESULT0    Exported result file of sample pairs with negative relationship.
    -1 RESULT1 --result1=RESULT1    Exported result file of sample pairs with positive relationship.
    -m lgLR|IBS --mode=lgLR|IBS     Select type of calculation method. [default: lgLR]
    -c0 COLOR0 --color0=COLOR0      Set plot color for negative group. [default: green]
    -c1 COLOR1 --color1=COLOR1      Set plot color for positive group. [default: red]
    -o OUT --output=OUT             Output name.
"""

import pandas as pd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics
from bin import logger
from sklearn.neighbors import KernelDensity

__all__ = ['kde']


@logger.logger
def kde(options):
    try:
        os.path.abspath(options['--result0'])
        os.path.abspath(options['--result1'])
    except TypeError:
        sys.exit('Error: Result samples do NOT exist!')
    mode = ['lgLR', 'IBS']
    colors = [  'blue', 
                'cyan', 
                'goldenrod', 
                'gray', 
                'green', 
                'khaki', 
                'magenta', 
                'orange', 
                'orchid', 
                'red', 
                'salmon', 
                'seagreen', 
                'slateblue', 
                'slategray', 
                'turquoise', 
                'violet',
                ]
    if options['--mode'] not in mode:
        sys.exit('Error: Only lgLR or IBS mode can be chosen!')
    if options['--color0'] not in colors:
        sys.exit('Error: Unsupported color!')
    if options['--color1'] not in colors:
        sys.exit('Error: Unsupported color!')
    kde_func(options['--result0'], options['--result1'], options['--mode'], 
             options['--color0'], options['--color1'], options['--output'])


def kde_func(r0, r1, mode, c0, c1, output):
    df0 = pd.read_csv(r0, header=0)
    '''list_0 = []
    for i in range(len(df0)):
        list_0.append('0')'''
    sample0 = np.array(list(df0.loc[:, mode]))
    print(sample0)
    df1 = pd.read_csv(r1, header=0)
    '''list_1 = []
    for j in range(len(df1)):
        list_1.append('1')'''
    sample1 = np.array(list(df1.loc[:, mode]))
    print(sample1)
    x_src0 = sample0.reshape(-1, 1)
    x_src1 = sample1.reshape(-1, 1)
    if mode == 'IBS':
        grid_k = 1
    else:
        grid_k = 100
    x_grid = np.linspace(min(sample0), max(sample1), int((max(sample1) - min(sample0) + 1) * grid_k))
    log_dens0 = KernelDensity(kernel='gaussian').fit(x_src0).score_samples(x_grid[:, None])
    log_dens1 = KernelDensity(kernel='gaussian').fit(x_src1).score_samples(x_grid[:, None])
    plt.plot(x_grid, np.exp(log_dens0), color='drak' + c0, label=r0)
    plt.plot(x_grid, np.exp(log_dens1), color='drak' + c1, label=r1)
    plt.hist(sample0, bins=int(max(sample0) - min(sample0) + 1), color=c0, density=True, alpha=0.5)
    plt.hist(sample1, bins=int(max(sample1) - min(sample1) + 1), color=c1, density=True, alpha=0.5)
    if mode == 'IBS':
        plt.xlim(min(sample0) - 5, max(sample1) + 5)
    else:
        plt.xlim(min(sample0) - 1, max(sample1) + 1)
    plt.ylim(0, 0.2)
    plt.xlabel(mode)
    plt.legend(loc="best")
    plt.savefig('%s%s' % (output, '_kde.png'))

'''
Supported colors:
blue
cyan
goldenrod
gray
green
khaki
magenta
orange
orchid
red
salmon
seagreen
slateblue
slategray
turquoise
violet
'''
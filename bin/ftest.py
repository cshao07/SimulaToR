# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
Usage:
    SimulaToR ftest [options] -0 RESULT0 -1 RESULT1 -o OUT

Options:
    -h --help                       Show help message.
    -v --version                    Show version.
    -0 RESULT0 --result0=RESULT0    Exported result file of sample pairs with negative relationship.
    -1 RESULT1 --result1=RESULT1    Exported result file of sample pairs with positive relationship.
    -c COLOR --color=COLOR          Color of the points in ROC figure. [default: blue]
    -m lgLR|IBS --mode lgLR|IBS     Select type of calculation method. [default: lgLR]
    -o OUT --output=OUT             Output name.
"""

import pandas as pd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from bin import logger

__all__ = ['ftest']


@logger.logger
def ftest(options):
    try:
        os.path.abspath(options['--result0'])
        os.path.abspath(options['--result1'])
    except TypeError:
        sys.exit('Error: Result samples do NOT exist!')
    mode = ['lgLR', 'IBS']
    if options['--mode'] not in mode:
        sys.exit('Error: Only lgLR or IBS mode can be chosen!')
    else:
        ftest_func(options['--result0'], options['--result1'], options['--mode'], options['--color'], options['--output'])



def ftest_func(r0, r1, mode, color, output):
    df0 = pd.read_csv(r0, header=0)
    df1 = pd.read_csv(r1, header=0)
    list0 = df0.loc[:, mode]
    list1 = df1.loc[:, mode]
    hmin = round(min(list1), 1) -1
    hmax = round(max(list0), 1) +1
    print(hmin, hmax)
    h0 = hmin
    h1 = hmax
    df_out = pd.DataFrame(None, columns=('h0', 'h1', 'TN', 'FP', 'FN', 'TP', 'FPR', 'FDR', 
                                         'Recall', 'Accuracy', 'Precision', 'h_mean'), dtype=int)
    while h0 < hmax:
        while h1 > h0:
            tn = len([i for i in list0 if i < h0])
            fp = len([i for i in list1 if i < h0])
            fn = len([i for i in list0 if i > h1])
            tp = len([i for i in list1 if i > h1])
            tnr = tn / (tn + fp)
            fpr = fp / (tn + fp) #假真率
            fnr = fn / (tp + fn)
            tpr = tp / (tp + fn)
            fdr = (fp + fn) / (tn + fp + fn + tp) #错判率
            recall  = tp / (tp + fn) #召回率
            accuracy = (tn + tp) / (tn + fp + fn + tp) #准确率
            precision = tp / (fp + tp) #精确率
            h_mean = 2 * tp / (2 * tp + fp + fn) #F1 score
            efficency = (tn + fp + fn + tp) / (len(list0) + len(list1))
            print(tn, fp, fn, tn, tnr, fpr, fnr, tpr, fdr, recall, accuracy, precision, h_mean)
            dict_out = {'h0':h0, 'h1':h1, 'TN':tn, 'FP':fp, 'FN':fn, 'TP':tp, 'FPR':fpr, 'FDR':fdr, 
                        'Recall':recall, 'Accuracy':accuracy, 'Precision':precision, 'h_mean':h_mean, 'Efficency':efficency}
            df_out=df_out.append(dict_out,ignore_index=True)
            h1 = h1 - 0.1
        h1 = hmax 
        h0 = h0 + 0.1
        font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14) 
    xValue = df_out.loc[:,'FPR']
    yValue = df_out.loc[:,'Recall']
    plt.ylim(0.95, 1)
    plt.xlim(0, 0.05)
    plt.title(u'ROC值散点图', FontProperties=font)
    plt.legend(loc="best")
    plt.scatter(xValue, yValue, s=20, c=color, marker=',')
    plt.savefig('%s%s' % (output, '_roc.png'))
    df_out.to_csv('%s%s%s%s' % (output, '_', 'F1_score', '.csv'), index=False, header=True, sep=',')
#!/usr/bin/env python
# -*- coding: utf-8 -*-#
"""
Usage:
    SimulaToR transfre [options] -f FILE

Options:
    -h --help                           Show help message.
    --version                           Show version.
    -f FILE --pop_file=FILE             Input frequency file with xls format.
    -o OUT --output=OUT                 Output directory. [default: pop_fre]
    -r --rewrite                        Remove existed frequency files. [default: FALSE]
    --filter=FILTER_FILE                Only transfer loci in FILTER_FILE.
    --mode=STR                          [default: STR]
    -l MARKER_LIST --list=MARKER_LIST   Export list of markers to a single file. [default: marker_list.xlsx]
"""

import sys
import os
import pandas as pd
import numpy as np
from . import logger, dir_func

__all__ = ['transfre']


@logger.logger
def transfre(options):
    if not os.path.isdir(options['--output']):
        os.mkdir(options['--output'])
    out_dir = os.path.abspath(options['--output'])
    rewrite = True if options['--rewrite'] else False
    if rewrite:
        dir_func.check_dir(out_dir)
    mode = {'STR', 'SNP'}
    if options['--filter']:
        loci_list = list(pd.read_csv(options['--filter'])['Marker'])
    else:
        loci_list = list(pd.read_excel(options['--pop_file'], None).keys())
    print(loci_list)
    if options['--mode'] not in mode:
        sys.exit('Error: SimCal transfre only support STR or SNP markers!')
    '''elif options['--mode'] == 'SNP':
        snp_transfre(options['--pop_file'], out_dir)
        update_marker_list(out_dir, options['--list'])'''
    str_transfre(options['--pop_file'], loci_list, out_dir)
    update_marker_list(out_dir, options['--list'])


def str_transfre(fre_file, loci_list, out_dir):
    print('Start to transfer STR population frequency file to recognizable format...')
    for i in loci_list:
        df = pd.read_excel(fre_file, sheet_name=i, header=0, index_col=None,
                           dtype={'Allele_Call': str, 'Frequency': float})
        allele = []
        fre = []
        fre_c = []
        for j in range(len(df)):
            allele.append(df.iloc[j, 0])
            fre.append('%.4f' % (df.iloc[j, 1]))
            fre_c.append('%.4f' % (1 / df.iloc[j, 1] + 1))
        fre_ran = []
        a = 0
        for k in range(len(df) - 1):
            a = a + float(df.iloc[k, 1])
            fre_ran.append('%.4f' % (1 - a))
        fre_ran.append(0)
        df_new = pd.DataFrame(None, columns=None, dtype=str)
        df_new.insert(0, 'Fre_ran', fre_ran)
        df_new.insert(0, 'Fre_C', fre_c)
        df_new.insert(0, 'Frequency', fre)
        df_new.insert(0, 'Allele_Call', allele)
        df_new.to_csv('%s%s%s' % (out_dir, '/', i),
                      columns=['Allele_Call', 'Frequency', 'Fre_C', 'Fre_ran'],
                      index=False, sep=",", encoding="utf-8")


'''
def snp_transfre(fre_file, outDir):
    print('Start to transfer SNP population frequency file to recognizable format...')
    df = pd.read_excel(fre_file, sheet_name='Sheet1', header=0, index_col=None, dtype={'Marker': str,
                                                                                       ('Ref', 'Alt'): float})
    for i in range(len(df)):
        fre_df = pd.DataFrame(None, columns=None, dtype=str)
        allele = ["0", "1"]
        fre = [df.iloc[i, 1], df.iloc[i, 2]]
        freC = ['%.4f' % (1 / float(df.iloc[i, 1]) + 1), '%.4f' % (1 / float(df.iloc[i, 2]) + 1)]
        freRan = [df.iloc[i, 2], 0]
        fre_df.insert(0, 'Fre_ran', freRan)
        fre_df.insert(0, 'Fre_C', freC)
        fre_df.insert(0, 'Frequency', fre)
        fre_df.insert(0, 'Allele_Call', allele)
        fre_df.to_csv('%s%s%s' % (outDir, '/', df.iloc[i, 0]), columns=['Allele_Call', 'Frequency', 'Fre_C', 'Fre_ran'],
                      index=False, sep=",", encoding="utf-8")
'''


def update_marker_list(freDir, list_file):
    print('Start to export population frequency files to marker list...')
    xlsx = pd.ExcelWriter(list_file, engine='xlsxwriter')
    for freFile in os.listdir(freDir):
        print('%s%s%s' % (freDir, '/', freFile))
        df = pd.read_csv('%s%s%s' % (freDir, '/', freFile), header=0, index_col=None, sep=',')
        print(df)
        allele_list = df['Allele_Call'].values.tolist()
        allele_list.append('sum')
        print(allele_list)
        fre_list = df['Frequency'].values.tolist()
        fre_sum = float(0)
        for i in range(len(fre_list)):
            fre_sum = fre_sum + float(fre_list[i])
        print(fre_sum)
        fre_list.append(fre_sum)
        dict_new = {'Allele_Call': allele_list, 'Frequency': fre_list}
        df_new = pd.DataFrame(dict_new)
        print(df_new)
        df_new.to_excel(xlsx, sheet_name=freFile, index=0)
    xlsx.save()
    locus_list = os.listdir(freDir)
    locus_dict = {'Locus': locus_list, 'Power of Discrimination': ''}
    locus_df = pd.DataFrame(locus_dict)
    locus_df.to_csv('marker_list.csv', header=0, sep=',')

# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
Usage:
    SimulaToR cal_2person [options]-o OUT -r RELATION -c PATH_C -z PATH_Z

Options:
    -h --help                       Show help message.
    -v --version                    Show version.
    -r --relation=RELATION          The assumed relationship between two individuals.
                                    [supporting relationships: Parent-child (PC)
                                                               Full siblings (FS)
                                                               Half siblings (HS)
                                                               Grandparent-grandchild (GG)
                                                               Uncle-nephew (UN)
                                                               First cousins (FC)]
    -c PATH_C --C_path=PATH_C       Input file PATH_C.
    -z PATH_Z --Z_path=PATH_Z       Input file PATH_Z.(Suspect Z is related to C with a certain relationship.)
    -f PATH --frequency_file=PATH   Input directory contains population frequency files. [default: pop_fre]
    -o OUT --output=OUT             Output directory.
"""

import sys
import pandas as pd
from bin import logger, dir_func, sample, marker, relation

"""
Created on Tue Nov 19 12:49:25 2019

@author: xiaozhutousan
"""

__all__ = ['cal_2person']


@logger.logger
def cal_2person(options):
    print(options['--output'])
    dir_func.check_dir(options['--output'])
    relations = {'PC', 'FS', 'HS', 'GG', 'UN', 'FC','SHS'}
    if options['--relation'] not in relations:
        sys.exit('Error::Unsupported relationship!')
    else:
        print('Start calculating...')
        cal_2person_func(options['--frequency_file'], options['--output'],
                         options['--relation'], options['--C_path'], options['--Z_path'])


class cal_2person_class:
    def __init__(self, freDir, locus, k, C, Z):
        self.sample_name = C.sample_name + '&' + Z.sample_name + '_' + k
        df = pd.read_csv('%s%s%s' % (freDir, '/', locus), header=0, dtype=str)
        coefficient = relation.relation(k)
        p_i = marker.load_marker(freDir, locus)
        p_j = marker.load_marker(freDir, locus)
        for i in range(len(df)):
            if df.iloc[i, 0] == C.allele1:
                p_i = marker.load_allele(freDir, locus, i)
        for j in range(len(df)):
            if df.iloc[j, 0] == C.allele1:
                p_j = marker.load_allele(freDir, locus, j)
        if C.allele1 == C.allele2:
            if Z.allele1 == Z.allele2:
                if C.allele1 == Z.allele1:
                    ito = coefficient.k0 + \
                        2 * coefficient.k1 / p_i.fre + \
                        coefficient.k2 / (p_i.fre ** 2)
                    self.formula = 'k0 + 2k1 / pi + k2 / pi ^ 2'
                    self.lr = '%.4f' % ito
                    self.ibs = '2'
                    return
                elif C.allele1 != Z.allele1:
                    ito = coefficient.k0
                    self.formula = 'k0'
                    self.lr = '%.4f' % ito
                    self.ibs = '0'
                    return
                return
            elif Z.allele1 != Z.allele2:
                if Z.allele1 == C.allele1 or Z.allele2 == C.allele1:
                    ito = coefficient.k0 + \
                        coefficient.k1 / p_i.fre
                    self.formula = 'k0 + k1 / pi'
                    self.lr = '%.4f' % ito
                    self.ibs = '1'
                    return
                elif Z.allele1 != C.allele1 and Z.allele2 != C.allele1:
                    ito = coefficient.k0
                    self.formula = 'k0'
                    self.lr = '%.4f' % ito
                    self.ibs = '0'
                    return
                return
            return
        elif C.allele1 != C.allele2:
            if Z.allele1 == Z.allele2:
                if C.allele1 == Z.allele1:
                    ito = coefficient.k0 + \
                        coefficient.k1 / p_i.fre
                    self.formula = 'k0 + k1 / pi'
                    self.lr = '%.4f' % ito
                    self.ibs = '1'
                    return
                elif C.allele2 == Z.allele1:
                    ito = coefficient.k0 + \
                        coefficient.k1 / p_j.fre
                    self.formula = 'k0 + k1 / pj'
                    self.lr = '%.4f' % ito
                    self.ibs = '1'
                    return
                elif C.allele1 != Z.allele1 and C.allele2 != Z.allele1:
                    ito = coefficient.k0
                    self.formula = 'k0'
                    self.lr = '%.4f' % ito
                    self.ibs = '0'
                    return
                return
            elif Z.allele1 != Z.allele2:
                if (C.allele1 == Z.allele1 and C.allele2 == Z.allele2) or \
                        (C.allele2 == Z.allele1 and C.allele1 == Z.allele2):
                    ito = coefficient.k0 + \
                          coefficient.k1 * (p_i.fre + p_j.fre) / (2 * p_i.fre * p_j.fre) + \
                          coefficient.k2 / (2 * p_i.fre * p_j.fre)
                    self.formula = 'k0 + k1(pi + pj)/(2 * pi * pj) + k2/(2 * pi * pj)'
                    self.lr = '%.4f' % ito
                    self.ibs = '2'
                    return
                elif C.allele1 == Z.allele1 or C.allele1 == Z.allele2:
                    ito = coefficient.k0 + \
                          coefficient.k1 / (2 * p_i.fre)
                    self.formula = 'k0 + k1 / ( 2 * pi )'
                    self.lr = '%.4f' % ito
                    self.ibs = '1'
                    return
                elif C.allele2 == Z.allele1 or C.allele2 == Z.allele2:
                    ito = coefficient.k0 + \
                          coefficient.k1 / (2 * p_j.fre)
                    self.formula = 'k0 + k1 / ( 2 * pj )'
                    self.lr = '%.4f' % ito
                    self.ibs = '1'
                    return
                else: 
                    ito = coefficient.k0
                    self.formula = 'k0'
                    self.lr = '%.4f' % ito
                    self.ibs = '0'
                    return
                return
            return
        
def cal_2person_func(freDir, resultDir, k, C_path, Z_path):
    marker_list = dir_func.sort_dir(freDir)
    c_samples = len(dir_func.sort_dir(C_path))
    z_samples = len(dir_func.sort_dir(Z_path))
    if c_samples != z_samples:
        sys.exit('Error: Sample numbers do NOT match!')
    for m in range(c_samples):
        C_name_list = []
        C_a1_list = []
        C_a2_list = []
        Z_name_list = []
        Z_a1_list = []
        Z_a2_list = []
        formula_list = []
        lr_list = []
        ibs_list = []
        for i in marker_list:
            C = sample.load_sample('%s%s%s' % (C_path, '/', m), i)
            Z = sample.load_sample('%s%s%s' % (Z_path, '/', m), i)
            C_name_list.append(C.sample_name)
            C_a1_list.append(C.allele1)
            C_a2_list.append(C.allele2)
            Z_name_list.append(Z.sample_name)
            Z_a1_list.append(Z.allele1)
            Z_a2_list.append(Z.allele2)
            result = cal_2person_class(freDir, i, k, C, Z)
            formula_list.append(result.formula)
            lr_list.append(result.lr)
            ibs_list.append(result.ibs)
        df = pd.DataFrame(None, columns=('Sample Name C', 'Allele C 1', 'Allele C 2',
                                         'Sample Name Z', 'Allele Z 1', 'Allele Z 2',
                                         'Marker', 'Formula', 'LR'), dtype=str)
        df.loc[:, 'Sample Name C'] = C_name_list
        df.loc[:, 'Allele C 1'] = C_a1_list
        df.loc[:, 'Allele C 2'] = C_a2_list
        df.loc[:, 'Sample Name Z'] = Z_name_list
        df.loc[:, 'Allele Z 1'] = Z_a1_list
        df.loc[:, 'Allele Z 2'] = Z_a2_list
        df.loc[:, 'Marker'] = marker_list
        df.loc[:, 'Formula'] = formula_list
        df.loc[:, 'LR'] = lr_list
        if k == 'FS':
            df['ibs'] = ibs_list
        df.to_csv('%s%s%s' % (resultDir, '/', m), index=False, sep=",", encoding="utf-8")

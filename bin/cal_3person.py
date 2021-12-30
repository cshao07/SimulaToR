# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
Usage:
    SimulaToR cal_3person [options]-o OUT -r RELATION -c PATH_C -m PATH_M -z PATH_M

Options:
    -h --help                       Show help message.
    -v --version                    Show version.
    -r --relation=RELATION          The assumed relationship between two individuals.
                                    [supporting relationships: Parent-child (PC)
                                                               Half siblings (HS)
                                                               Grandparent-grandchild (GG)
                                                               Uncle-nephew (UN)
                                                               First cousins (FC)]
    -c PATH_C --C_path=PATH_C       Input file PATH_C.
    -m PATH_M --M_path=PATH_M       Input file PATH_M.(M is the known mother of sample C.
                                                       Also could be father of sample C in half sibling cases)
    -z PATH_Z --Z_path=PATH_Z       Input file PATH_Z.(Suspect Z is related to C with a certain relationship.)
    -f PATH --frequency_file=PATH   Input directory contains population frequency files. [default: pop_fre]
    -o OUT --output=OUT             Output directory.
"""

import sys
import pandas as pd
from . import dir_func, sample, marker, relation, logger

__all__ = ['cal_3person']


@logger.logger
def cal_3person(options):
    print(options['--output'])
    dir_func.check_dir(options['--output'])
    relations = {'PC', 'HS', 'GG', 'UN', 'FC'}
    if options['--relation'] not in relations:
        sys.exit('Error::Unsupported relationship!')
    else:
        print('Start calculating...')
        cal_3person_func(options['--frequency_file'], options['--output'],
                         options['--relation'], options['--C_path'], options['--M_path'], options['--Z_path'])


def cal_3person_func(freDir, resultDir, k, C_path, M_path, Z_path):
    marker_list = dir_func.sort_dir(freDir)
    c_samples = len(dir_func.sort_dir(C_path))
    m_samples = len(dir_func.sort_dir(M_path))
    z_samples = len(dir_func.sort_dir(Z_path))
    if c_samples != m_samples or m_samples != z_samples or z_samples != c_samples:
        sys.exit('Error: Sample numbers do NOT match!')
    for m in range(c_samples):
        C_name_list = []
        C_a1_list = []
        C_a2_list = []
        M_name_list = []
        M_a1_list = []
        M_a2_list = []
        Z_name_list = []
        Z_a1_list = []
        Z_a2_list = []
        lr_list = []
        for i in marker_list:
            C = sample.load_sample('%s%s%s' % (C_path, '/', m), i)
            M = sample.load_sample('%s%s%s' % (M_path, '/', m), i)
            Z = sample.load_sample('%s%s%s' % (Z_path, '/', m), i)
            C_name_list.append(C.sample_name)
            C_a1_list.append(C.allele1)
            C_a2_list.append(C.allele2)
            M_name_list.append(M.sample_name)
            M_a1_list.append(M.allele1)
            M_a2_list.append(M.allele2)
            Z_name_list.append(Z.sample_name)
            Z_a1_list.append(Z.allele1)
            Z_a2_list.append(Z.allele2)
            result = cal_3person_class(freDir, i, k, C, M, Z)
            lr_list.append(result.lr)
        df = pd.DataFrame(None, columns=('Sample Name C', 'Allele C 1', 'Allele C 2',
                                         'Sample Name M', 'Allele M 1', 'Allele M 2',
                                         'Sample Name Z', 'Allele Z 1', 'Allele Z 2',
                                         'Marker', 'LR'), dtype=str)
        df.loc[:, 'Sample Name C'] = C_name_list
        df.loc[:, 'Allele C 1'] = C_a1_list
        df.loc[:, 'Allele C 2'] = C_a2_list
        df.loc[:, 'Sample Name M'] = M_name_list
        df.loc[:, 'Allele M 1'] = M_a1_list
        df.loc[:, 'Allele M 2'] = M_a2_list
        df.loc[:, 'Sample Name Z'] = Z_name_list
        df.loc[:, 'Allele Z 1'] = Z_a1_list
        df.loc[:, 'Allele Z 2'] = Z_a2_list
        df.loc[:, 'Marker'] = marker_list
        df.loc[:, 'LR'] = lr_list
        df.to_csv('%s%s%s' % (resultDir, '/', m), index=False, sep=",", encoding="utf-8")


class cal_3person_class:
    def __init__(self, freDir, locus, k, C, M, Z):
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
        try:
            if C.allele1 == C.allele2:
                if Z.allele1 == Z.allele2:
                    if Z.allele1 == C.allele1:
                        self.pi = 1 / p_i.fre
                    else:
                        self.pi = 0
                elif Z.allele1 != Z.allele2:
                    if Z.allele1 == C.allele1 or Z.allele2 == C.allele1:
                        self.pi = 1 / (2 * p_i.fre)
                    else:
                        self.pi = 0
            elif C.allele1 != C.allele2:
                if M.allele1 == M.allele2:
                    if M.allele1 == C.allele1:
                        if Z.allele1 == Z.allele2 and Z.allele1 == C.allele2:
                            self.pi = 1 / p_j.fre
                        elif Z.allele1 != Z.allele2 and (Z.allele1 == C.allele2 or Z.allele2 == C.allele2):
                            self.pi = 1 / (2 * p_j.fre)
                        else:
                            self.pi = 0
                    elif M.allele1 == C.allele2:
                        if Z.allele1 == Z.allele2 and Z.allele1 == C.allele1:
                            self.pi = 1 / p_i.fre
                        elif Z.allele1 != Z.allele2 and (Z.allele1 == C.allele1 or Z.allele2 == C.allele1):
                            self.pi = 1 / (2 * p_i.fre)
                        else:
                            self.pi = 0
                elif M.allele1 != M.allele2:
                    if M.allele1 == C.allele1 and M.allele2 == C.allele2:
                        if Z.allele1 in [C.allele1, C.allele2] and Z.allele2 in [C.allele1, C.allele2]:
                            self.pi = 1 / (p_i.fre + p_j.fre)
                            self.lr = (1 - 2 * coefficient.k1) + 2 * coefficient.k1 * self.pi
                            return
                        elif Z.allele1 in [C.allele1, C.allele2] and Z.allele2 not in [C.allele1, C.allele2]:
                            self.pi = 1 / (2 * (p_i.fre + p_j.fre))
                            self.lr = (1 - 2 * coefficient.k1) + 2 * coefficient.k1 * self.pi
                            return
                        elif Z.allele2 in [C.allele1, C.allele2] and Z.allele1 not in [C.allele1, C.allele2]:
                            self.pi = 1 / (2 * (p_i.fre + p_j.fre))
                            self.lr = (1 - 2 * coefficient.k1) + 2 * coefficient.k1 * self.pi
                            return
                        else:
                            self.pi = 0
                            self.lr = (1 - 2 * coefficient.k1) + 2 * coefficient.k1 * self.pi
                            return
                    elif M.allele1 == C.allele1 or M.allele2 == C.allele1:
                        if Z.allele1 == Z.allele2 and Z.allele1 == C.allele2:
                            self.pi = 1 / p_j.fre
                        elif Z.allele1 != Z.allele2 and (Z.allele1 == C.allele2 or Z.allele2 == C.allele2):
                            self.pi = 1 / p_j.fre
                        else:
                            self.pi = 0
                    elif M.allele1 == C.allele2 or M.allele2 == C.allele2:
                        if Z.allele1 == Z.allele2 and Z.allele1 == C.allele1:
                            self.pi = 1 / p_i.fre
                        elif Z.allele1 != Z.allele2 and (Z.allele1 == C.allele1 or Z.allele2 == C.allele1):
                            self.pi = 1 / p_i.fre
                        else:
                            self.pi = 0
        except AttributeError:
            sys.exit('Error: Samples contain off-ladder allele!')
        self.lr = (1 - 2 * coefficient.k1) + 2 * coefficient.k1 * self.pi

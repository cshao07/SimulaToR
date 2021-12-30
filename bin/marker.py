#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:49:25 2019

@author: xiaozhutousan
"""

__all__ = ['load_marker', 'load_allele']

import pandas as pd


class load_marker:
    def __init__(self, freDir, marker):
        self.df = pd.read_csv('%s%s%s' % (freDir, '/', marker), header=0, dtype={'Allele_Call': str,
                                                                                 'Frequency': float})
        self.alleles = self.df.loc[:, 'Allele_Call']


class load_allele(load_marker):
    def __init__(self, freDir, marker, i):
        super().__init__(freDir, marker)
        self.allele = self.df.loc[i, 'Allele_Call']
        self.fre = self.df.loc[i, 'Frequency']
        self.C = self.df.loc[i, 'Fre_C']
        self.ran = self.df.loc[i, 'Fre_ran']



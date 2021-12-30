# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:49:25 2019

@author: xiaozhutousan
"""

__all__ = {'create_sample', 'load_sample', 'load_result'}

import pandas as pd
import re


class create_sample:
    def __init__(self, sample_file, marker):
        self.sample_name = sample_file
        self.locus = marker
        self.allele1 = None
        self.allele2 = None


class load_sample(create_sample):
    def __init__(self, sample_file, marker):
        super().__init__(sample_file, marker)
        self.df = pd.read_csv(sample_file, header=0, index_col='Marker', dtype=str)
        self.allele1 = self.df.at[marker, 'Allele 1']
        self.allele2 = self.df.at[marker, 'Allele 2']
        if float(self.allele1) > float(self.allele2):
            a = self.allele1
            self.allele1 = self.allele2
            self.allele2 = a


class load_result_fs(create_sample):
    def __init__(self, sample_file, marker):
        super().__init__(sample_file, marker)
        self.df = pd.read_csv(sample_file, header=0, index_col='Marker')
        self.ito = self.df.at[marker, 'LR']
        self.ibs = self.df.at[marker, 'ibs']


class load_result_nfs(create_sample):
    def __init__(self, sample_file, marker):
        super().__init__(sample_file, marker)
        self.df = pd.read_csv(sample_file, header=0, index_col='Marker')
        self.ito = self.df.at[marker, 'LR']

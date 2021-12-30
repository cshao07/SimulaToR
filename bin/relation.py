# -*- coding: utf-8 -*-
# !/usr/bin/python

__all__ = 'relation'


class relation:
    def __init__(self, relationship):
        if relationship == 'PC':
            self.k0 = 0
            self.k1 = 0.5
            self.k2 = 0
        if relationship == 'FS':
            self.k0 = 0.25
            self.k1 = 0.25
            self.k2 = 0.25
        if relationship in ['HS', 'GG', 'UN']:
            self.k0 = 0.5
            self.k1 = 0.25
            self.k2 = 0
        if relationship == 'FC':
            self.k0 = 0.75
            self.k1 = 0.125
            self.k2 = 0
        if relationship == 'SHS':
            self.k0 = 0.375
            self.k1 = 0.25
            self.k2 = 0.125

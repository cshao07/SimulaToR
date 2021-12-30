# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
Usage:
    SimulaToR create [options] -t N

Options:
    -h --help                      Show help message.
    -v --version                   Show version.
    -t N --times=N                 Simulation counts.
    -f PATH --frequency_file=PATH  Input directory contains population frequency files. [default: pop_fre]
    -m --manual                    Create a custom family. [default: FALSE]
    --frequency_mode               Create individuals according to population frequency.
    --parent_mode                  Create individuals according to two groups of individuals.
    --parent1=DIR1                 Provide one group of individuals for parent_mod.
    --parent2=DIR2                 Provide another group of individuals for parent_mod.
    --output=outDir                Output directory. [default: outDir]

for suffix in automatic mod:       GF=grand father
                                   GM=grand mother
                                   UW=uncle's wife
                                   U=uncle
                                   Co=cousin
                                   F=father
                                   M=mother
                                   C=child
                                   TOM=the other man
                                   HS=half sibling
      GF-----GM
          |
UW-----U-----F-----M-----TOM
    |           |     |
   Co           C     HS

for manual mod: SimCal create -m --name <NAME> --suffix <SUFFIX> \
--create_mode|(--parent_mode --parent1 <DIR> --parent2 <DIR2>) -t N

"""

import os
import random
import sys
from bin import sample, marker, logger, dir_func, output


"""
Created on Tue Nov 19 12:49:25 2019

@author: xiaozhutousan
"""

__all__ = ['create']


@logger.logger
def create(options):
    try:
        t = int(options['--times'])
    except ValueError:
        sys.exit('%s%s%s' % ('Error: You can NOT simulate \"', options['--times'], '\" times!'))
    else:
        manual = True if options['--manual'] else False
        if not manual:
            print('Start to create child samples...')
            individual(t, 'SimFam_C', options['--frequency_file'])
            print('Start to create uncle\'s wife samples...')
            individual(t, 'SimFam_UW', options['--frequency_file'])
            print('Start to create the other man samples...')
            individual(t, 'SimFam_TOM', options['--frequency_file'])
            print('Start to create father and mother samples...')
            parent(t, 'SimFam_C', 'SimFam_F', 'SimFam_M', options['--frequency_file'])
            print('Start to create grand father and grand mother samples...')
            parent(t, 'SimFam_F', 'SimFam_GF', 'SimFam_GM', options['--frequency_file'])
            print('Start to create uncle samples...')
            child(t, 'SimFam_U', 'SimFam_GF', 'SimFam_GM', options['--frequency_file'])
            print('Start to create half sibling samples...')
            child(t, 'SimFam_HS', 'SimFam_TOM', 'SimFam_M', options['--frequency_file'])
            print('Start to create cousin samples...')
            child(t, 'SimFam_Co', 'SimFam_U', 'SimFam_UW', options['--frequency_file'])
        else:
            if not options['--frequency_mode'] and not options['--parent_mode']:
                sys.exit('Error: MODE must be defined in manual creation!')
            elif options['--frequency_mode'] and options['--parent_mode']:
                sys.exit('Error: You MUST choose individual_mode or parent_mode!')
            elif options['--frequency_mode']:
                individual(t, options['--output'], options['--frequency_file'])
            elif options['--parent_mode']:
                if not options['--parent1'] or not options['--parent2']:
                    sys.exit('Error: Directories of both parent individuals are required for parent mode!')
                else:
                    child(t, options['--output'], options['--parent1'], options['--parent2'],
                          options['--frequency_file'])
            else:
                sys.exit('Error: UNKNOWN error!')


def individual(N, x, freDir):
    dir_func.check_dir(x)
    marker_list = dir_func.sort_dir(freDir)
    for m in range(N):
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        for l in marker_list:
            locus = marker.load_marker(freDir, l)
            s_x = sample.create_sample('%s%s%s' % (x, '/', m), l)
            r1 = random.random()
            for i in range(len(locus.alleles)):
                allele = marker.load_allele(freDir, l, i)
                if r1 >= float(allele.ran):
                    s_x.allele1 = str(allele.allele)
                    break
                i += 1
            r2 = random.random()
            for j in range(len(locus.alleles)):
                allele = marker.load_allele(freDir, l, j)
                if r2 >= float(allele.ran):
                    s_x.allele2 = str(allele.allele)
                    break
                j += 1
            list1.append(s_x.sample_name)
            list2.append(s_x.locus)
            list3.append(s_x.allele1)
            list4.append(s_x.allele2)
        output.out_sample(list1, list2, list3, list4,
                          x, m)


def parent(times, x, p1, p2, fre_dir):
    dir_func.check_dir(p1)
    dir_func.check_dir(p2)
    marker_list = os.listdir(fre_dir)
    for m in range(times):
        list1_1 = []
        list2_1 = []
        list3_1 = []
        list4_1 = []
        list1_2 = []
        list2_2 = []
        list3_2 = []
        list4_2 = []
        for l in marker_list:
            s_x = sample.load_sample('%s%s%s' % (x, '/', m), l)
            marker_info = marker.load_marker(fre_dir, l)
            s_p1 = sample.create_sample('%s%s%s' % (p1, '/', m), l)
            s_p2 = sample.create_sample('%s%s%s' % (p2, '/', m), l)
            r0 = random.random()
            if r0 >= 0.5:
                s_p1.allele1 = s_x.allele1
                s_p2.allele1 = s_x.allele2
            else:
                s_p1.allele1 = s_x.allele2
                s_p2.allele1 = s_x.allele1
            r1 = random.random()
            for i in range(len(marker_info.alleles)):
                allele = marker.load_allele(fre_dir, l, i)
                if r1 >= float(allele.ran):
                    s_p1.allele2 = str(allele.allele)
                    break
                i += 1
            r2 = random.random()
            for j in range(len(marker_info.alleles)):
                allele = marker.load_allele(fre_dir, l, j)
                if r2 >= float(allele.ran):
                    s_p2.allele2 = str(allele.allele)
                    break
                j += 1
            list1_1.append(s_p1.sample_name)
            list2_1.append(s_p1.locus)
            list3_1.append(s_p1.allele1)
            list4_1.append(s_p1.allele2)
            list1_2.append(s_p2.sample_name)
            list2_2.append(s_p2.locus)
            list3_2.append(s_p2.allele1)
            list4_2.append(s_p2.allele2)
        output.out_sample(list1_1, list2_1, list3_1, list4_1, p1, m)
        output.out_sample(list1_2, list2_2, list3_2, list4_2, p2, m)


def child(times, x, p1, p2, freDir):
    dir_func.check_dir(x)
    marker_list = dir_func.sort_dir(freDir)
    for m in range(times):
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        for l in marker_list:
            s_p1 = sample.load_sample('%s%s%s' % (p1, '/', m), l)
            s_p2 = sample.load_sample('%s%s%s' % (p2, '/', m), l)
            s_x = sample.create_sample('%s%s%s' % (x, '/', m), l)
            r1 = random.random()
            if r1 >= 0.5:
                s_x.allele1 = s_p1.allele1
            else:
                s_x.allele1 = s_p1.allele2
            r2 = random.random()
            if r2 >= 0.5:
                s_x.allele2 = s_p2.allele1
            else:
                s_x.allele2 = s_p2.allele2
            list1.append(s_x.sample_name)
            list2.append(s_x.locus)
            list3.append(s_x.allele1)
            list4.append(s_x.allele2)
        output.out_sample(list1, list2, list3, list4, x, m)
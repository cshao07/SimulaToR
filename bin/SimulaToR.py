#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: SimulaToR (<command> | --help | --version)
"""

from docopt import docopt
import sys
from bin.version import __version__

__author__ = ['Cheng-Chen Shao (cshao07@fudan.edu.cn)']

help_doc = '''
Usage: SimulaToR <command> [options]

Command:
    transfre         Transfer population frequency file to csv format 
    create           Create simulated individuals to construct a family
    cal_2person      Calculate LR and IBS score in kinship testing of two persons
    cal_3person      Calculate LR and IBS score in kinship testing of three persons
    export           Export the calculation results to a single file
    kde              Plot kde figure for two group of results
    ftest            F-test and plot roc figure for two group of results
'''


def main():
    command_log = 'SimulaToR ' + ' '.join(sys.argv[1:])
    if len(sys.argv) == 1:
        sys.exit(help_doc)
    elif sys.argv[1] == '--version' or sys.argv[1] == '-v':
        sys.exit(__version__)
    elif sys.argv[1] == 'transfre':
        from . import transfre
        transfre.transfre(docopt(transfre.__doc__, version=__version__),
                          command=command_log, name='transfre')
    elif sys.argv[1] == 'create':
        from . import create
        create.create(docopt(create.__doc__, version=__version__),
                      command=command_log, name='create')
    elif sys.argv[1] == 'cal_2person':
        from . import cal_2person
        cal_2person.cal_2person(docopt(cal_2person.__doc__, version=__version__),
                                command=command_log, name='cal_2person')
    elif sys.argv[1] == 'cal_3person':
        from . import cal_3person
        cal_3person.cal_3person(docopt(cal_3person.__doc__, version=__version__),
                                command=command_log, name='cal_3person')
    elif sys.argv[1] == 'export':
        from . import export
        export.export(docopt(export.__doc__, version=__version__),
                      command=command_log, name='export')
    elif sys.argv[1] == 'kde':
        from . import kde
        kde.kde(docopt(kde.__doc__, version=__version__),
                  command=command_log, name='kde')
    elif sys.argv[1] == 'ftest':
        from . import ftest
        ftest.ftest(docopt(ftest.__doc__, version=__version__),
                  command=command_log, name='ftest')
    else:
        sys.exit(help_doc)


if __name__ == '__main__':
    main()
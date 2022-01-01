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
    cal_kinship      Calculate LR and IBS score in kinship testing of two persons
    export           Export the calculation results to a single file
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
    elif sys.argv[1] == 'cal_kinship':
        from . import cal_kinship
        cal_kinship.cal_kinship(docopt(cal_kinship.__doc__, version=__version__),
                                command=command_log, name='cal_kinship')
    elif sys.argv[1] == 'export':
        from . import export
        export.export(docopt(export.__doc__, version=__version__),
                      command=command_log, name='export')
    else:
        sys.exit(help_doc)


if __name__ == '__main__':
    main()
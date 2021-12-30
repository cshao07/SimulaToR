# -*- coding: utf-8 -*-
import re
import pandas as pd
import sys
import os
import shutil


def main(auc_file, n, outDir):
    print(auc_file, n, outDir)
    auc_list= []
    for i in range(20, int(n)+1):
        df = pd.read_csv('%s%s%s' % (auc_file, i, '_auc.csv'), None, header=0, index_col=None)
        print(df)
        auc_list.append('%.8f' % float(df.iat[0, 2]))
    df_csv = pd.DataFrame(None, index=None, columns=None)
    df_csv.insert(0, 'auc', auc_list)
    df_csv.to_csv(outDir, index=False, sep=",", encoding="utf-8")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])

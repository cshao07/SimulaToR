# -*- coding: utf-8 -*-
import re
import pandas as pd
import sys
import os
import shutil


def main(fre_xlsx, list_csv, popDir):
    print(fre_xlsx, list_csv, popDir)
    if os.path.isdir(popDir):
        if os.listdir(popDir):
            shutil.rmtree(popDir)  # 删除文件夹
            os.mkdir(popDir)  # 创建文件夹
    else:
        os.mkdir(popDir)  # 创建文件夹
    freFile = os.path.abspath(fre_xlsx)
    df = pd.read_csv(list_csv, None, header=0, index_col=None)
    print(df)
    list0 = list(df['Marker'].values)
    list1 = []
    for a in range(len(list0)):
        list1.append('%s%s' % (df['Marker'].values[a], '_1'))
    list2 = []
    for a in range(len(list0)):
        list2.append('%s%s' % (df['Marker'].values[a], '_2'))
    list3 = []
    for a in range(len(list0)):
        list3.append('%s%s' % (df['Marker'].values[a], '_3'))
    list4 = []
    for a in range(len(list0)):
        list4.append('%s%s' % (df['Marker'].values[a], '_4'))
    print(list0, list1, list2, list3, list4)
    for i in list0:
        print(freFile, i)
        df = pd.read_excel(io=fre_xlsx, sheet_name=i, header=0, col_index=None)
        print(df)
        allele = []
        fre = []
        freC = []
        for j in range(len(df)):
            allele.append(df.iloc[j, 0])
            fre.append('%.4f' % (df.iloc[j, 1]))
            freC.append('%.4f' % (1 / df.iloc[j, 1] + 1))
        freRan = []
        a = 0
        for k in range(len(df) - 1):
            a = a + float(df.iloc[k, 1])
            freRan.append('%.4f' % (1 - a))
        freRan.append(0)
        df_new = pd.DataFrame(None, columns=None, dtype=str)
        df_new.insert(0, 'Fre_ran', freRan)
        df_new.insert(0, 'Fre_C', freC)
        df_new.insert(0, 'Frequency', fre)
        df_new.insert(0, 'Allele_Call', allele)
        df_new.to_csv('%s%s%s' % (popDir, '/', i),
                      columns=['Allele_Call', 'Frequency', 'Fre_C', 'Fre_ran'],
                      index=False, sep=",", encoding="utf-8")
        df_new.to_csv('%s%s%s%s' % (popDir, '/', i, '_1'),
                      columns=['Allele_Call', 'Frequency', 'Fre_C', 'Fre_ran'],
                      index=False, sep=",", encoding="utf-8")
        df_new.to_csv('%s%s%s%s' % (popDir, '/', i, '_2'),
                      columns=['Allele_Call', 'Frequency', 'Fre_C', 'Fre_ran'],
                      index=False, sep=",", encoding="utf-8")
        df_new.to_csv('%s%s%s%s' % (popDir, '/', i, '_3'),
                      columns=['Allele_Call', 'Frequency', 'Fre_C', 'Fre_ran'],
                      index=False, sep=",", encoding="utf-8")
        df_new.to_csv('%s%s%s%s' % (popDir, '/', i, '_4'),
                      columns=['Allele_Call', 'Frequency', 'Fre_C', 'Fre_ran'],
                      index=False, sep=",", encoding="utf-8")
    list_all = list0 + list1 + list2 + list3 + list4
    print(list_all)
    df_csv = pd.DataFrame(None, index=None, columns=None)
    df_csv.insert(0, 'Marker', list_all)
    print(df_csv)
    fre_csv = '%s%s' % (popDir, '.csv')
    print(fre_csv)
    df_csv.to_csv(fre_csv,index=False, sep=",", encoding="utf-8")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])

# -*- coding: utf-8 -*- 
'''
author: liyi
time:   2017.12.24 14:00

useage: xls2yaml.py myxls.xls myyaml.yaml
eg:
    python xls2yaml2.py /Users/liyi/Desktop/logfile.xls /Users/liyi/Desktop/document.yaml
'''

import yaml
import sys
import csv
import xlrd

#print sys.getdefaultencoding()# get the system default encoding


def xls2yaml(file_name_xls,file_name_yaml):

    res_fs_paths = dict()   # 输出的结果
    res_pattern = []
    #print fs_paths
    
    file_xls = xlrd.open_workbook(file_name_xls) # 打开xls文件 
    table = file_xls.sheets()[0]                 # 打开第一张表  
    nrows = table.nrows                      # 获取表的行数  
    for i in range(nrows):                   # 循环逐行打印 
      if i == 0:                             # 跳过第一行 
        continue
      #print table.row_values(i)
      if table.row_values(i)[1] is not None and table.row_values(i)[1]!='':
        if table.row_values(i)[1] in res_pattern:
          pass
        res_pattern.append(table.row_values(i)[1].encode('utf-8'))
    
      if table.row_values(i)[0] is not None and table.row_values(i)[0][0]=='/':
        path = table.row_values(i)[0]
        fs= '/' + table.row_values(i)[0].split('/',2)[1]
        secondary_path = ''
        if len(table.row_values(i)[0].split('/',2))>2:
          secondary_path = table.row_values(i)[0].split('/',2)[2]
          #print fs,secondary_path
        
        if res_fs_paths.has_key(fs) :
          res_fs_paths[fs].append(path.encode('utf-8'))
        else:
          res_fs_paths[fs.encode('utf-8')]=[path.encode('utf-8')]
      else:
        print '\''+ table.row_values(i)[0] + "\' is not a valid ptah"
    #print res_fs_paths

    res = {'pattern':res_pattern}
    res['paths']=res_fs_paths
    
    stream = file(file_name_yaml, 'wb')
    yaml.dump(res, stream,default_style='"') ##！！

if __name__ == '__main__':
    #print sys.argv
    #if len(sys.argv) < 3:
    #    print sys.argv
    #file_name_xls, file_name_yaml=  sys.argv[1],sys.argv[2]
    #xls2yaml(file_name_xls,file_name_yaml)
    xls2yaml('/Users/liyi/Desktop/logfile.xls','/Users/liyi/Desktop/document.yaml')
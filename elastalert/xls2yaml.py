# -*- coding: utf-8 -*- 
import yaml
import sys
import csv
import xlrd

#print sys.getdefaultencoding()# get the system default encoding

def main():
    f = open('/Users/liyi/Desktop/var.yaml','r')  
    print f
    print type(f)
    #print f.read()
    x=yaml.load(f.read())
    print x
    print type(x)
    print x['mysql_users']

    #stream = file('/Users/liyi/Desktop/document.yaml', 'w')
    #yaml.dump(x, stream)    # Write a YAML representation of data to 'document.yaml'.
    #print yaml.dump(x)      # Output the document to the screen.
    
    #with open("/Users/liyi/Desktop/logfile.xls",'rb') as xlsfile:
    #    data=csv.reader(xlsfile)
    #    print data
    #    for row in data:
    #       print row

    fs_paths = dict()
    #print fs_paths
    data = xlrd.open_workbook('/Users/liyi/Desktop/logfile.xls') # 打开xls文件 
    table = data.sheets()[0] # 打开第一张表  
    nrows = table.nrows # 获取表的行数  
    for i in range(nrows): # 循环逐行打印 
      if i == 0: # 跳过第一行 
        continue
      #print table.row_values(i)
      if table.row_values(i)[0] is not None and table.row_values(i)[0][0]=='/':
          path = table.row_values(i)[0]
          fs= '/' + table.row_values(i)[0].split('/',2)[1]
          secondary_path = ''
          if len(table.row_values(i)[0].split('/',2))>2:
            secondary_path = table.row_values(i)[0].split('/',2)[2]
          #print fs,secondary_path
          if fs_paths.has_key(fs) :
              fs_paths[fs].append(path.encode('utf-8'))
          else:
              fs_paths[fs.encode('utf-8')]=[path.encode('utf-8')]
      else:
          print '\''+ table.row_values(i)[0] + "\' is not a valid ptah"
    print fs_paths

    stream = file('/Users/liyi/Desktop/document.yaml', 'wb')
    x={'paths':fs_paths}
    yaml.dump(x, stream)
    
if __name__ == '__main__':
    main()
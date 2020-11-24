import arcpy
import math
import numpy as np
import pandas as pd
from collections import Counter

#获取工具框内工具栏中的数据
t_layer  = arcpy.GetParameterAsText(0)   # one所在图层
t_fv  = arcpy.GetParameterAsText(1) # 特征变量字段名称
c_layer  = arcpy.GetParameterAsText(2) # all的图层
s_layer  = arcpy.GetParameterAsText(3) # 结果图层

#读取工具栏中的数据
arcpy.AddMessage(t_layer)
arcpy.AddMessage(t_fv)
arcpy.AddMessage(c_layer)
arcpy.AddMessage(s_layer)

#获取原始属性表数据，用分号分割，作为初始特征变量数组
ovset = t_fv.split(';')

arcpy.AddMessage(ovset)

#将comparision layer复制一份作为similarity layer
arcpy.CopyFeatures_management(c_layer, s_layer)

#在similarity layer中添加一个新的字段，作为存放相似度计算结果的字段
arcpy.management.AddField(s_layer, "similarityIndex", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)

#建立t_layer的只读游标
rows = arcpy.SearchCursor(t_layer)

row = rows.next()

#建立中心城市的特征变量数组
#生成两份独立的vest数组，为算法中的排序部分做准备
vset1 = []
vset2 = []
for i in ovset:
    v = row.getValue(i)
    vset1.append(v)
    vset2.append(v)

arcpy.AddMessage(vset1)

#建立c_layer的只读游标
rows1 = arcpy.SearchCursor(c_layer)

row1 = rows1.next()


#建立存放结果的数组
resultSet = []

#建立对比城市的特征变量数组
cset1 = []
cset2 = []

while row1:
    cset1 = []
    cset2 = []
    for j in ovset:
        
        v = row1.getValue(j)
        cset1.append(v)
        cset2.append(v)

    #计算相关系数并存入结果数组
    
    n = len(vset1)
    vset1.sort()
    cset1.sort()

    #arcpy.AddMessage(vset1)

    pr = np.ones((1,n))
    ps = np.ones((1,n))
    
    for i in range(n):
        pr[0][i] = vset1.index(vset2[i])                 #获取秩统计量，此处因数据为列表形式，故用此方法，数组另有方法
        ps[0][i] = cset1.index(cset2[i])                 #列表对于重复元素，只能获取第一个出现元素的索引，而数组可以一次获取，但数组获取返回的是元组形式
    
    def findrank(x1,z):    
        repeat =[item for item, count in Counter(vset1).items() if count > 1]       # 找重复元素
        rcount = [count for item, count in Counter(vset1).items() if count > 1]     #找重复次数
        nr = len(repeat)      
        for j in range(nr):                          #处理重复元素的秩统计量
            a = vset1.index(repeat[j])
            m = rcount[j]
            b = (m*a+(m-1)*m/2)/m
            [d,c] = np.where(z==a)
            z[0][c] = b
    
    findrank(vset1,pr) 
    findrank(cset1,ps)
    qxy = 0
    for i in range(n):
        qxy = qxy + np.square(pr[0][i] - ps[0][i])                        #计算spearman
    qxy = 1 - 6/n/(np.square(n)-1)*qxy  
    #将相关系数调整至0-2之间
    r = 1-qxy
    if math.isnan(r):
        r = 2
    
    #将结果写入结果列表
    resultSet.append(r)

    #arcpy.AddMessage("-------------")
    #arcpy.AddMessage(r)                                        
    #arcpy.AddMessage("-------------")

    row1 = rows1.next()



#删除旧游标
del rows
del row
del rows1
del row1


#将计算结果写入similarity layer的新字段中
rows2= arcpy.UpdateCursor(s_layer)

row2 = rows2.next()

index = 0
while row2:
    row2.setValue("similarityIndex", resultSet[index])
    rows2.updateRow(row2)
    
    row2 = rows2.next()
    index = index + 1


del row2
del rows2
    
# arcpy.AddMessage(vset1)





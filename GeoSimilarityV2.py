import arcpy
import math
import numpy as np
import pandas as pd
from collections import Counter

#Get the data in the toolbar in the tool box
t_layer  = arcpy.GetParameterAsText(0)   # Origin city layer
t_fv  = arcpy.GetParameterAsText(1) # Characteristic variable field name
c_layer  = arcpy.GetParameterAsText(2) # Destination city layer
s_layer  = arcpy.GetParameterAsText(3) # Result layer

#Read the data in the toolbar
arcpy.AddMessage(t_layer)
arcpy.AddMessage(t_fv)
arcpy.AddMessage(c_layer)
arcpy.AddMessage(s_layer)

#Obtain the original attribute table data as the initial feature variable array
ovset = t_fv.split(';')

arcpy.AddMessage(ovset)

#Copy the comparison layer as a similarity layer
arcpy.CopyFeatures_management(c_layer, s_layer)

#Add a new field in the similarity layer as a field to store the similarity calculation results
arcpy.management.AddField(s_layer, "similarityIndex", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)

#Create a read-only cursor for t_layer
rows = arcpy.SearchCursor(t_layer)

row = rows.next()

#Establish the characteristic variable array of the origin city
#Generate two independent vest arrays to prepare for the sorting part of the algorithm
vset1 = []
vset2 = []
for i in ovset:
    v = row.getValue(i)
    vset1.append(v)
    vset2.append(v)

arcpy.AddMessage(vset1)

#Create a read-only cursor for c_layer
rows1 = arcpy.SearchCursor(c_layer)

row1 = rows1.next()


#Create an array to store the results
resultSet = []

#Establish an array of characteristic variables for comparing cities
cset1 = []
cset2 = []

while row1:
    cset1 = []
    cset2 = []
    for j in ovset:
        
        v = row1.getValue(j)
        cset1.append(v)
        cset2.append(v)

    #Calculate the correlation coefficient and store it in the result array
    n = len(vset1)
    vset1.sort()
    cset1.sort()


    pr = np.ones((1,n))
    ps = np.ones((1,n))
    
    for i in range(n):
        #Get the rank statistics
        #The data is in the form of a list so we use this method, the array has another method
        #For a list of repeated elements, only the index of the first appearing element can be obtained, while the array can be obtained at one time, but the return of the array is tuple form
        pr[0][i] = vset1.index(vset2[i])
        ps[0][i] = cset1.index(cset2[i])                 
    
    def findrank(x1,z):
        #Get repeated elements    
        repeat =[item for item, count in Counter(vset1).items() if count > 1]
        #Get repetitions
        rcount = [count for item, count in Counter(vset1).items() if count > 1]
        nr = len(repeat)
        #Deal with the rank statistics of repeated elements      
        for j in range(nr):                          
            a = vset1.index(repeat[j])
            m = rcount[j]
            b = (m*a+(m-1)*m/2)/m
            [d,c] = np.where(z==a)
            z[0][c] = b
    
    findrank(vset1,pr) 
    findrank(cset1,ps)
    qxy = 0
    #Calculate Spearman's correlation coefficient
    for i in range(n):
        qxy = qxy + np.square(pr[0][i] - ps[0][i])                        
    qxy = 1 - 6/n/(np.square(n)-1)*qxy
    """  
    #Adjust the correlation coefficient to between 0-2
    r = 1-qxy
    if math.isnan(r):
        r = 2
    """
    
    #Write the result to the result list
    resultSet.append(qxy)

    row1 = rows1.next()



#Delete old cursor
del rows
del row
del rows1
del row1


#Write the calculation result into the new field of the similarity layer
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
    






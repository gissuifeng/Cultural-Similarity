# Cultural-Similarity
Code description:

Users can use this algorithm to select the attributes of the layer attributes that need to be used as feature variables, and calculate the similarity between regions.

Toolbox description:

This is an ArcGIS Pro tool based on the python language. It is suitable for ArcGIS Pro 2.6 and above. It is used to calculate the cultural distance between regions and serves as the research basis for Cultural Semantic Similarity Flow.
The toolbox in ArcGIS pro is shown below.

![image](https://github.com/gissuifeng/Cultural-Similarity/blob/main/Toolbox%20Description.png)

There are four data frames in the tool, namely Target layer, Feature variables, Comparision layer, and Similarity layer.In the Target layer, you need to enter the layer of origin city, such as Origin_Layers that has been provided. In Feature variables, you need to select the feature variables involved in the calculation. In the original data, there are 9 characteristic variables that can participate in the calculation, as shown in the figure above.
What needs to be input in the Comparison layer data box is the data of Destination cities, where you can input the Dimension_Layers data.

In the end, we can use this tool to get the cultural distance of Origin city relative to all other cities in China, as shown below.

![image](https://github.com/gissuifeng/Cultural-Similarity/blob/main/Results.png)

The similarity calculation result is stored in the similarityIndex field of the attribute table.

![image](https://github.com/gissuifeng/Cultural-Similarity/blob/main/Result%20Attribute%20Table.png)



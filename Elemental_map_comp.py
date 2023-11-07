'''
Author: Marcin Szpytma
Date Created: 17/03/2022
Date Modified 23/05/2022

Description
Python script to generate heatmaps of element sensitive PIXE mapping on cancer tissues
'''
import sys
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.cbook as cbook
from matplotlib import pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from pathlib import Path


#Import of the file selected for analysis
file_name = input('Insert file name/path to the .csv  file:\n')

try:
    data = pd.read_csv(f'{file_name}', sep=';')
    if  not data.empty:
        print(f"File from path {file_name} has been succesfuly read")
except Exception as err:
    print("Wrong path to the ${file_name} or file is not existing")



#Checking the data     
print(data.head(5))

#List of measured elements
for element_names in data.columns[2:]:
    print (element_names)

#Select element for mapping
selected_element = input("Select specific element for mapping:\n")
#Based on measurement setup the dimensions of the output heatmap have to be provided
#In case of the files frovided as an example the dimensions 13x8 is sufficient
dimension1 = input("First dimension for reshape:\n")
dimension2 = input("Second dimension for reshape:\n")


elmnt = ((np.asarray(data[selected_element])).reshape(int(dimension1),int(dimension2)))
#print(elmnt)
wElmnt = data.pivot( index = 'row', columns ='column', values = selected_element)
#print(wElmnt)

fig = plt.figure(figsize = (16, 16))
sns.set(font_scale=4)
ax = sns.heatmap(elmnt, cbar_kws={"orientation": "vertical", "label": "counts [a.u]"}, cmap = "jet")
ax.set(xticklabels=[],yticklabels=[])
scalebar = ScaleBar (4.1, 'um')
plt.gca().add_artist(scalebar)
plt.tight_layout()
plt.show()

#If you schoose to save the output
try:
    save_confirm = input("If you want to save the picture, enter YES. Or NO if you do not wish to save it\n")
    if save_confirm == "YES" or save_confirm == "NO":
        if save_confirm == "YES":
            fig.savefig(f'{selected_element}Map.png', dpi = 300)
        elif save_confirm == "NO":
            print ("File won't be saved")    
except Exception as err:
    print("Wrong input, provide YES or NO")
    
#

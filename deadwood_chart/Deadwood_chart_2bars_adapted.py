import pandas
import os
import csv
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib as mpl
import seaborn as sns
import numpy as np


os.chdir('C:/Users/Klara/Documents/chart/ano')
#UNECE DEADWOOD DATA
#load the csv table a put first 2 rows into a single HEADER
UNECE_deadwood = pandas.read_csv('UNECE_deadwood.csv',encoding= 'unicode_escape', header=[0,1])
UNECE_deadwood.columns = UNECE_deadwood.columns.map('_'.join)
UNECE_deadwood.rename_axis('Date').reset_index()
#put the stats into dataframes
UNECE_deadwood = pandas.DataFrame(UNECE_deadwood)
#reame the first column as COUNTRY
UNECE_deadwood.rename(columns={UNECE_deadwood.columns[0]: "ENG_NAME"}, inplace = True)
#Choose relevant columns
UNECE_deadwood = UNECE_deadwood[['ENG_NAME', 'Forest - 2015 (m?/ha)_Total', 'Forest - 2010 (m?/ha)_Total']]

#load csv with Europe names and limit for the EU27
Europe = pandas.read_csv('Countries extended CODES_eea.csv')
EU27 = Europe[Europe["EU27"] == 1]
EU27 = EU27[['ISO3_CODE', 'ENG_NAME']]

#merge deadwood data with names
UNECE_deadwood_EU27 = EU27.merge(UNECE_deadwood, how='left', on="ENG_NAME")

#fill the missing values of 2015 with 2010
UNECE_deadwood_EU27['Forest - 2015 (m?/ha)_Total']= UNECE_deadwood_EU27['Forest - 2015 (m?/ha)_Total'].fillna(UNECE_deadwood_EU27['Forest - 2010 (m?/ha)_Total'])

#keep only 2015 column
UNECE_deadwood_EU27 = UNECE_deadwood_EU27[['ENG_NAME', 'Forest - 2015 (m?/ha)_Total']]

#rename column - Forest - 2015 (m?/ha)_Total
UNECE_deadwood_EU27 = UNECE_deadwood_EU27.rename(columns={'Forest - 2015 (m?/ha)_Total': 'Deadwood', 'ENG_NAME':'Country'})

#print(UNECE_deadwood_EU27.to_string())
#create UNECE lists for the charts
# Country = list(UNECE_deadwood_EU27["Country"])
# UNECE_deadwood = list(UNECE_deadwood_EU27["Deadwood"])
# print(Country)
# print(UNECE_deadwood)

#ICP DEADWOOD DATA
ICP_deadwood = pandas.read_csv('ICP_DW.csv')
ICP_deadwood = pandas.DataFrame(ICP_deadwood)
ICP_deadwood = ICP_deadwood[['Country', 'ICP']]

##DEADWOOD DATA FOR REF. SITES
REFSITES_deadwood = pandas.read_csv('deadwood_v10.csv',encoding= 'unicode_escape')
REFSITES_deadwood = pandas.DataFrame(REFSITES_deadwood)
REFSITES_deadwood = REFSITES_deadwood[['Bioregion', 'Country', 'Deadwood']]
REFSITES_deadwood = REFSITES_deadwood.dropna()
REFSITES_deadwood = REFSITES_deadwood.astype({'Deadwood':'float64'})

#REFSITES= (REFSITES_deadwood.groupby(['Country','Bioregion'])['Deadwood'])
         #.agg(['mean','min','max'])
         #.reset_index())
print(REFSITES_deadwood)

# Creating a DataFrame
df = pandas.DataFrame(REFSITES_deadwood)

def process_table_with_pandas(file_path):
    # Read the table into a DataFrame
    #df = pandas.read_csv(file_path, delimiter='\t')  # Adjust delimiter based on your actual separator

    # Combine Country and Bioregion to create a new 'Country_Bioregion' column
    df['Country_Bioregion'] = df['Country'] + '-' + df['Bioregion']

    # Group by the 'Country_Bioregion' column and aggregate 'Deadwood' values into a list
    result_df = df.groupby('Country_Bioregion')['Deadwood'].agg(list).reset_index()

    # Convert the result to a dictionary
    country_bioregion_dict = dict(zip(result_df['Country_Bioregion'], result_df['Deadwood']))

    return country_bioregion_dict

file_path = 'deadwood_v10.csv'  # Replace with the actual path to your table file
result_dict = process_table_with_pandas(file_path)

# Print the result
for key, value in result_dict.items():
    print(f"{key}: {value}")

#UNECE AND ICP
table = pandas.merge(UNECE_deadwood_EU27, ICP_deadwood, how='outer', on="Country")
print(table)


# #CHECK EVERY TIME AFTER CHANGING ENTRY DATA: drop countries where in both datasets are NA
table = table.loc[table["Country"] != "Croatia"]
table = table.loc[table["Country"] != "Cyprus"]
# table = table.loc[table["Country"] != "France"]
table = table.loc[table["Country"] != "Greece"]
table = table.loc[table["Country"] != "Luxembourg"]
table = table.loc[table["Country"] != "Malta"]
table = table.reset_index()
table = table.drop(['index'], axis=1)
table = table.fillna(0)
table['number'] = range(1, 1+len(table))
table.to_csv('C:/Users/Klara/Documents/chart/ano/table.csv')
print(table.to_string())
#
# # #create lists for the charts
Country = list(table["Country"])
Country = list(dict.fromkeys(Country)) #removes duplicates, keeps only one from several same values
# #Country = list(map(lambda x: x.replace('Czech Republic', 'Czech Rep.'), Country)) #replace: shortening czech rep.
# #Country = list(map(lambda x: x.replace('Netherlands', 'Netherl.'), Country)) #replace: shortening czech rep.
#
# # TABLE for mean, min_e, max_e without 0
# table2 = table.drop(table.loc[table['mean']==0].index, inplace=True)
# table2 = table.loc[table['mean']!= 0]
# print(table2)
# # # create error columns
# table2['min_e']= table2["mean"] - table2["min"]
# table2['max_e']= table2["max"] - table2["mean"]
# print(table2)
# # #create error lists for the charts
# y_error = list(table2["mean"])
# #y_error  = list(filter(lambda num: num != 0, y_error)) #correct
# yerr_min = list(table2["min_e"])
# #yerr_min  = list(filter(lambda num: num != 0, yerr_min)) #correct
# yerr_max = list(table2["max_e"])
# #yerr_max  = list(filter(lambda num: num != 0, yerr_max)) #correct
x_bar0=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21] #list(range(0, 22)) #correct
x_bar1= [-0.2,0.8,1.8,2.8,3.8,4.8,5.8,6.8,7.8,8.8,9.8,10.8,11.8,12.8,13.8,14.8,15.8,16.8,17.8,18.8,19.8,20.8]
x_bar2= [0.2,1.2,2.2,3.2,4.2,5.2,6.2,7.2,8.2,9.2,10.2,11.2,12.2,13.2,14.2,15.2,16.2,17.2,18.2,19.2,20.2,21.2]
# #CHECK EVERY TIME AFTER CHANGING ENTRY DATA: deadwood bar list change manualy deleting the duplicates (except 0)
y_bar1 = [21.8, 11.45, 0.0, 25.20, 4.92, 14.77, 6.0, 23, 20.6, 9.72, 10.11, 9.23, 23.55, 22.8, 13.2, 6.3, 2.33, 9.2, 28.0, 22.3, 4.76, 8.43]
y_bar2 = [23.7,
16.5,
0,
4.1,

6.2,
0,
4.7,

20.1,

23.8,
9,
1.6,


12.9,
25.2,
15.7,
0,

7.3,
0,

0,
22.5,

29.9,

4.6,
23.3,
]
# #CHECK EVERY TIME AFTER CHANGING ENTRY DATA: error bar mean list (y) and error bar numbers list(x)  change manualy deleting mean 0 and corresponding number at X numbers list
x_error = [0,
1,
2,
3,
3.9,
4.1,
5,
6,
6.9,
7.1,
7.9,
8.1,
9,
10.8,
11,
11.2,
12,
13,
14,
14.9,
15.1,
16.9,
17.1,
18,
18.9,
19.1,
19.9,
20.1,
21
] #correct
# #x_error = [1, 2, 3, 4, 4.9, 5.1, 6, 7, 7.9, 8.1, 8.9, 9.1, 10, 11.8, 12, 12.2, 13, 14, 15, 15.9, 16.1, 17.9, 18.1, 19, 19.9, 20.1, 22]
# #checking the list and the correct number of values in the lists
# print("y_bar1")
# print(y_bar1)
# print(len(y_bar1))
#
# print("y_bar2")
# print(y_bar2)
# print(len(y_bar2))
#
# print("x_bar1")
# print(x_bar1)
# print(len(x_bar1))
#
# print("x_bar2")
# print(x_bar2)
# print(len(x_bar2))
#
# print("y_error")
# print(y_error)
# print(len(y_error))
#
# print("x_error")
# print(x_error)
# print(len(x_error))
#
# print("yerr_max")
# print(yerr_max)
# print(len(yerr_max))
#
# print("yerr_min")
# print(yerr_min)
# print(len(yerr_min))
#
# print("Country")
# print(Country)
# print(len(Country))
# #  #CHART
#
# #loop for different markers
# def mscatter(x, y,ax=None, m=None, **kw):
#     import matplotlib.markers as mmarkers
#     if not ax: ax=plt.gca()
#     sc = ax.scatter(x,y,**kw)
#     if (m is not None) and (len(m)==len(x)):
#         paths = []
#         for marker in m:
#             if isinstance(marker, mmarkers.MarkerStyle):
#                 marker_obj = marker
#             else:
#                 marker_obj = mmarkers.MarkerStyle(marker)
#             path = marker_obj.get_path().transformed(
#                         marker_obj.get_transform())
#             paths.append(path)
#         sc.set_paths(paths)
#     return sc
# x=x_error
# y=y_error
# m = ["D","s","*","*","s","*","h","h","s","o","s","*","d","D","*","o","h","h","s","D","*","D","d","D","D","*","d","o","h"]
# c = ["blue","cyan","yellowgreen","yellowgreen","cyan","yellowgreen","green","green","cyan","gold","cyan","yellowgreen","orange","blue","yellowgreen","gold",
# "green","green","cyan","blue","yellowgreen","blue","orange","blue","blue","yellowgreen","red","gold","green"]
# s= [20,
# 25,
# 60,
# 60,
# 25,
# 60,
# 40,
# 40,
# 25,
# 30,
# 25,
# 60,
# 40,
#
# 20,
# 60,
# 30,
# 40,
# 40,
# 25,
# 20,
# 60,
#
# 20,
# 40,
# 20,
# 20,
# 60,
# 40,
# 30,
# 40,
#
#
#
# ]
#
fig, ax = plt.subplots()
ax.bar(x=x_bar0, height = 0, width=1, tick_label=Country)
ax.bar(x=x_bar1, height = y_bar1, width=0.4, color='lightsteelblue', edgecolor = 'black', zorder=0)
ax.bar(x=x_bar2, height = y_bar2, width=0.4, color='grey', edgecolor = 'black', zorder=0)


def plot_deadwood_values_scatter(country_bioregion_dict, x_error, dot_size=10):
    # Extract keys and values from the dictionary
    keys = list(country_bioregion_dict.keys())
    values = list(country_bioregion_dict.values())
    # Extract unique Bioregions and assign a unique color to each
    bioregions = set(bioregion.split('-')[1] for bioregion in keys)
    color_mapping = {bioregion: plt.cm.jet(i / len(bioregions)) for i, bioregion in enumerate(bioregions)}




    # Plot the scatter plot for each key with a unique color
    for i, (key, value) in enumerate(country_bioregion_dict.items()):
        bioregion = key.split('-')[1]
        color = color_mapping[bioregion]
        plt.scatter([x_error[i]] * len(value), value, label=key, color=color, s=dot_size)

        # Create a legend for Bioregions
    legend_handles = [plt.Line2D([0], [0], color='w', label=bioregion.capitalize(), markerfacecolor=color, markersize=5) for bioregion, color in color_mapping.items()]
    plt.legend(handles=legend_handles, title='Biogeoregions', fontsize='small')

    #plt.xlabel('Point')
    #plt.ylabel('Deadwood Values')
    #plt.title('Deadwood Values by Country and Bioregion (Scatter Plot)')
    #plt.legend()
    #plt.show()

# Example usage
file_path = 'deadwood_v10.csv'  # Replace with the actual path to your table file
result_dict = process_table_with_pandas(file_path)

# Plot the deadwood values as a scatter plot with unique colors for each key
plot_deadwood_values_scatter(result_dict, x_error, dot_size=7)

#
# #ax.set_xticks(x_bar1)
#
ax.margins(x=0)
# error = [yerr_min, yerr_max]
# ax.errorbar(x=x_error, y=y_error, yerr=error, fmt='none', linewidth=1, capsize=3, zorder=1)
# #plt.text(1,deadwood_errorbar_mean[1],"Text Label",va='top',fontsize=3,rotation=90)
# #ax.scatter(x=x_error, y=y_error, s=15)
# scatter = mscatter(x, y, c=c, s=s, m=m, ax=ax, zorder=2)
#
plt.xticks(fontsize=8, rotation=90)
# #fig.suptitle('Deadwood amount EU27', fontsize=10, weight = 'bold')
# #plt.xlabel('Country', fontsize=5)
plt.ylabel('Deadwood m3/ha', fontsize=10, weight = 'bold')
fig.subplots_adjust(bottom = 0.18, top = 0.98)
#
# boreal = mlines.Line2D([], [], color='green', marker='h', linestyle='None',
#                           markersize=5, label='Boreal')
# atlantic = mlines.Line2D([], [], color='cyan', marker='s', linestyle='None',
#                           markersize=5, label='Atlantic')
# alpine = mlines.Line2D([], [], color='blue', marker='D', linestyle='None',
#                           markersize=5, label='Alpine')
# continental = mlines.Line2D([], [], color='yellowgreen', marker='*', linestyle='None',
#                           markersize=5, label='Continental')
# mediterranean = mlines.Line2D([], [], color='gold', marker='o', linestyle='None',
#                           markersize=5, label='Mediterranean')
# pannonian = mlines.Line2D([], [], color='orange', marker='d', linestyle='None',
#                           markersize=5, label='Pannonian')
# macaronesian = mlines.Line2D([], [], color='red', marker='d', linestyle='None',
#                           markersize=5, label='Macaronesian')
# #blue_patch = mpatches.Patch(facecolor='lightsteelblue',edgecolor = 'black', label='UNECE Deadwood')
#
#
# plt.legend(handles=[boreal, atlantic, alpine, continental, mediterranean, pannonian, macaronesian],title='Biogeographical regions')
plt.show()
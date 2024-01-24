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

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x=x_bar0, height = 0, width=1, tick_label=Country)
ax.bar(x=x_bar1, height = y_bar1, width=0.4, color='lightsteelblue', edgecolor = 'black', zorder=0)
ax.bar(x=x_bar2, height = y_bar2, width=0.4, color='grey', edgecolor = 'black', zorder=0)


def plot_deadwood_values_scatter(country_bioregion_dict, x_error, bioregion_colors, dot_size=10):
    # Extract keys and values from the dictionary
    keys = list(country_bioregion_dict.keys())
    values = list(country_bioregion_dict.values())
    # Extract unique Bioregions and assign a unique color to each
    bioregions = set(bioregion.split('-')[1] for bioregion in keys)
    color_mapping = {bioregion: bioregion_colors.get(bioregion.upper(), 'black') for bioregion in bioregions}




    # Plot the scatter plot for each key with a unique color
    for i, (key, value) in enumerate(country_bioregion_dict.items()):
        bioregion = key.split('-')[1]
        color = color_mapping[bioregion]
        plt.scatter([x_error[i]] * len(value), value, label=key, s=dot_size,  color=color)

        # Create a legend for Bioregions
    legend_order = ['CONTINENTAL', 'PANNONIAN', 'ALPINE', 'ATLANTIC', 'MACARONESIAN', 'MEDITERANEAN', 'BOREAL']
    legend_handles = [plt.Line2D([0], [0], marker='o',color='w', label=bioregion.capitalize(), markerfacecolor=bioregion_colors[bioregion], markersize=5) for bioregion in legend_order]
    plt.legend(handles=legend_handles, title='Biogeoregions', fontsize='small')

    #plt.xlabel('Point')
    #plt.ylabel('Deadwood Values')
    #plt.title('Deadwood Values by Country and Bioregion (Scatter Plot)')
    #plt.legend()
    #plt.show()

# Example usage
file_path = 'deadwood_v10.csv'  # Replace with the actual path to your table file
result_dict = process_table_with_pandas(file_path)

# Define specific colors for each bioregion in a dictionary
# bioregion_colors = {
#     'Continental': 'navy',
#     'Pannonian': 'blue',
#     'Alpine': 'cornflowerblue',
#     'Atlantic': 'aquamarine',
#     'Macaronesian': 'lawngreen',
#     'Mediterranean': 'orange',
#     'Boreal': 'red',
# }
bioregion_colors = {
    'CONTINENTAL': 'navy',
    'PANNONIAN': 'blue',
    'ALPINE': 'cornflowerblue',
    'ATLANTIC': 'aquamarine',
    'MACARONESIAN': 'lawngreen',
    'MEDITERANEAN': 'orange',
    'BOREAL': 'red',

    # Add more bioregions and colors as needed
}

# Plot the deadwood values as a scatter plot with unique colors for each key
plot_deadwood_values_scatter(result_dict, x_error, bioregion_colors, dot_size=7)


ax.margins(x=0)

#
plt.xticks(fontsize=8, rotation=90)
# #fig.suptitle('Deadwood amount EU27', fontsize=10, weight = 'bold')
# #plt.xlabel('Country', fontsize=5)
plt.ylabel('Deadwood m3/ha', fontsize=10, weight = 'bold')
fig.subplots_adjust(bottom = 0.18, top = 0.98)

save_path = 'C:/Users/Klara/Desktop/deadwood_adapted.png'
plt.savefig(save_path, dpi=1200, bbox_inches='tight')
plt.show()

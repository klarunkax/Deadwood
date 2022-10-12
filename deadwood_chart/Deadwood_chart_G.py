import pandas
import os
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np


os.chdir('C:/Users/Klara/Documents/Prace/JRC/Teleworking/2022/forest_condition/deadwood/chart')
#UNECE DEADWOOD DATA
#load the csv table a put first 2 rows into a single HEADER
UNECE_deadwood = pandas.read_csv('UNECE_deadwood.csv',encoding= 'unicode_escape', header=[0,1])
UNECE_deadwood.columns = UNECE_deadwood.columns.map('_'.join)
UNECE_deadwood.rename_axis('Date').reset_index()
#put the stats into dataframes
UNECE_deadwood = pandas.DataFrame(UNECE_deadwood)
#reame the first column as COUNTRY
UNECE_deadwood.rename(columns={UNECE_deadwood.columns[0]: "ENG_NAME"}, inplace = True)
#Choose rrelevant columns
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

print(UNECE_deadwood_EU27.to_string())
#create UNECE lists for the charts
# Country = list(UNECE_deadwood_EU27["Country"])
# UNECE_deadwood = list(UNECE_deadwood_EU27["Deadwood"])
# print(Country)
# print(UNECE_deadwood)

##DEADWOOD DATA FOR REF. SITES
REFSITES_deadwood = pandas.read_csv('literature_review_deadwood_organized.csv')
REFSITES_deadwood = pandas.DataFrame(REFSITES_deadwood)
REFSITES_deadwood = REFSITES_deadwood[['Bioregion', 'Country', 'Deadwood']]
REFSITES_deadwood = REFSITES_deadwood.dropna()
REFSITES_deadwood = REFSITES_deadwood.astype({'Deadwood':'float64'})

REFSITES_min_max_avg= (REFSITES_deadwood.groupby(['Country','Bioregion'])['Deadwood']
         .agg(['mean','min','max'])
         .reset_index())
#print(REFSITES_min_max_avg)

table = pandas.merge(UNECE_deadwood_EU27, REFSITES_min_max_avg, how='outer', on="Country")
#print(table)
#CHECK EVERY TIME AFTER CHANGING ENTRY DATA: drop countries where in both datasets are NA
table = table.loc[table["Country"] != "Croatia"]
table = table.loc[table["Country"] != "Cyprus"]
table = table.loc[table["Country"] != "France"]
table = table.loc[table["Country"] != "Greece"]
table = table.loc[table["Country"] != "Luxembourg"]
table = table.loc[table["Country"] != "Malta"]
table = table.reset_index()
table = table.drop(['index'], axis=1)
table = table.fillna(0)
print(table)

# #create lists for the charts
Country = list(table["Country"])
Country = list(dict.fromkeys(Country)) #removes duplicates, keeps only one from several same values
Country = list(map(lambda x: x.replace('Czech Republic', 'Czech Rep.'), Country)) #replace: shortening czech rep.
Country = list(map(lambda x: x.replace('Netherlands', 'Netherl.'), Country)) #replace: shortening czech rep.
deadwood_errorbar_mean = list(table["mean"])
deadwood_errorbar_min = list(table["min"])
deadwood_errorbar_min  = list(filter(lambda num: num != 0, deadwood_errorbar_min))
deadwood_errorbar_max = list(table["max"])
deadwood_errorbar_max  = list(filter(lambda num: num != 0, deadwood_errorbar_max))
errorbar_list_1_to_25 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10.8, 11, 11.2, 12, 13, 14, 15, 16, 16.9, 17.1, 18, 19, 20, 21, 22]
barlist_1_to_22 = list(range(1, 23))
deadwood_bar_list = list(table["Deadwood"])
print(deadwood_bar_list)
#CHECK EVERY TIME AFTER CHANGING ENTRY DATA: deadwood bar list change manualy deleting the duplicates (except 0)
deadwood_bar_list = [21.8, 11.45, 0.0, 0.0, 4.92, 14.77, 6.0, 20.6, 9.72, 10.11, 9.23, 23.55, 22.8, 13.2, 6.3, 2.33, 9.2, 28.0, 22.3, 4.76, 8.43, 0.0]
#CHECK EVERY TIME AFTER CHANGING ENTRY DATA: error bar mean list (y) and error bar numbers list(x)  change manualy deleting mean 0 and corresponding number at X numbers list
deadwood_errorbar_mean=[60.714285714285715, 77.0, 28.825000000000003, 159.9, 181.0, 120.97999999999999, 102.66666666666667, 47.25, 65.3, 111.7, 92.0, 32.6, 155.0, 158.0, 135.0, 175.95454545454547, 205.66666666666666, 4.4, 60.675000000000004]
errorbar_list_1_to_25 = [1, 2, 3, 4, 5, 6,  9, 10.8, 11, 11.2, 12, 13, 15, 16.9, 17.1, 18, 19, 21, 22]
#checking the list and the correct number of values in the lists
print(deadwood_bar_list)
print(len(deadwood_bar_list))

print(barlist_1_to_22)
print(len(barlist_1_to_22))

print(deadwood_errorbar_mean)
print(len(deadwood_errorbar_mean))

print(errorbar_list_1_to_25)
print(len(errorbar_list_1_to_25))

print(Country)
print(len(Country))
 #CHART
fig, ax = plt.subplots()
ax.bar(x=barlist_1_to_22, height = deadwood_bar_list, width=1, tick_label=Country, color='lightsteelblue', edgecolor = 'black')
error = [deadwood_errorbar_min, deadwood_errorbar_max]
ax.errorbar(x=errorbar_list_1_to_25, y=deadwood_errorbar_mean, yerr=error, fmt='d', linewidth=1, capsize=3)
#plt.text(1,deadwood_errorbar_mean[1],"Text Label",va='top',fontsize=3,rotation=90)

plt.xticks(fontsize=8, rotation=60)
fig.suptitle('Deadwood amount EU27', fontsize=10, weight = 'bold')
plt.xlabel('Country', fontsize=5)
plt.ylabel('Deadwood m3/ha', fontsize=10, weight = 'bold')

plt.show()
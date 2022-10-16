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
REFSITES_deadwood = pandas.read_csv('literature_review_deadwood_organized_V2.csv')
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
# table = table.loc[table["Country"] != "France"]
table = table.loc[table["Country"] != "Greece"]
table = table.loc[table["Country"] != "Luxembourg"]
table = table.loc[table["Country"] != "Malta"]
table = table.reset_index()
table = table.drop(['index'], axis=1)
table = table.fillna(0)
table['number'] = range(1, 1+len(table))
print(table)
table.to_csv('C:/Users/Klara/Documents/Prace/JRC/Teleworking/2022/forest_condition/deadwood/chart/table.csv')

# #create lists for the charts
Country = list(table["Country"])
Country = list(dict.fromkeys(Country)) #removes duplicates, keeps only one from several same values
Country = list(map(lambda x: x.replace('Czech Republic', 'Czech Rep.'), Country)) #replace: shortening czech rep.
Country = list(map(lambda x: x.replace('Netherlands', 'Netherl.'), Country)) #replace: shortening czech rep.
y_error = list(table["mean"])
y_error  = list(filter(lambda num: num != 0, y_error)) #correct
yerr_min = list(table["min"])
yerr_min  = list(filter(lambda num: num != 0, yerr_min)) #correct
yerr_max = list(table["max"])
yerr_max  = list(filter(lambda num: num != 0, yerr_max)) #correct
x_bar= list(range(1, 23)) #correct
y_bar = list(table["Deadwood"])
print(y_bar)
#CHECK EVERY TIME AFTER CHANGING ENTRY DATA: deadwood bar list change manualy deleting the duplicates (except 0)
y_bar = [21.8, 11.45, 0.0, 0.0, 4.92, 14.77, 6.0, 0.0, 20.6, 9.72, 10.11, 9.23, 23.55, 22.8, 13.2, 6.3, 2.33, 9.2, 28.0, 22.3, 4.76, 8.43] #correct
#CHECK EVERY TIME AFTER CHANGING ENTRY DATA: error bar mean list (y) and error bar numbers list(x)  change manualy deleting mean 0 and corresponding number at X numbers list
x_error = [1, 2, 3, 4, 4.9, 5.1, 6, 7, 7.9, 8.1, 8.9, 9.1, 10, 11.8, 12, 12.2, 13, 14, 15, 15.9, 16.1, 17.9, 18.1, 19, 19.9, 20.1, 22] #correct
#checking the list and the correct number of values in the lists
print("y_bar")
print(y_bar)
print(len(y_bar))

print("x_bar")
print(x_bar)
print(len(x_bar))

print("y_error")
print(y_error)
print(len(y_error))

print("x_error")
print(x_error)
print(len(x_error))

print("yerr_max")
print(yerr_max)
print(len(yerr_max))

print("yerr_min")
print(yerr_min)
print(len(yerr_min))

print("Country")
print(Country)
print(len(Country))
#  #CHART
fig, ax = plt.subplots()
ax.bar(x=x_bar, height = y_bar, width=1, tick_label=Country, color='lightsteelblue', edgecolor = 'black')
error = [yerr_min, yerr_max]
ax.errorbar(x=x_error, y=y_error, yerr=error, fmt='d', linewidth=1, capsize=3)
#plt.text(1,deadwood_errorbar_mean[1],"Text Label",va='top',fontsize=3,rotation=90)

plt.xticks(fontsize=8, rotation=60)
fig.suptitle('Deadwood amount EU27', fontsize=10, weight = 'bold')
plt.xlabel('Country', fontsize=5)
plt.ylabel('Deadwood m3/ha', fontsize=10, weight = 'bold')

plt.show()
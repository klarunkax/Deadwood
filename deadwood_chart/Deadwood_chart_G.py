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

# #create REFSITES lists for the charts
#Country_errorbar = list(REFSITES_min_max_avg["Country"])
deadwood_errorbar_mean = list(table["mean"])
deadwood_errorbar_min = list(table["min"])
deadwood_errorbar_max = list(table["max"])
errorbar_list_1_to_21 = range(1, 25)
barlist_1_to_21 = range(1, 21)
deadwood_bar_list = list(table["Deadwood"])??? - how to delete values that occur more times
#
# print(Country_errorbar)
# print(deadwood_errorbar_mean)
# print
#
# #CHART
# fig, ax = plt.subplots()
# ax.bar(x=list_1_to_27, height = UNECE_deadwood, width=1, tick_label=Country, color='lightsteelblue', edgecolor = 'black')
# error = [deadwood_errorbar_min, deadwood_errorbar_max]
# ax.errorbar(x=list_1_to_19, y=deadwood_errorbar_mean, tick_label=Country_errorbar, yerr=error, fmt='o', linewidth=1, capsize=3)
#
# plt.xticks(fontsize=8, rotation=90)
# fig.suptitle('Deadwood amount EU27', fontsize=20)
# plt.xlabel('Country', fontsize=5)
# plt.ylabel('Deadwood m3/ha', fontsize=16)
#
# plt.show()
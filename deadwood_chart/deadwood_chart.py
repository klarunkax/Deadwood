import pandas
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
os.chdir('C:/Users/Klara/Documents/Prace/JRC/Teleworking/2022/forest_condition/deadwood/chart')

#load the csv table a put first 2 rows into a single HEADER
UNECE_deadwood = pandas.read_csv('UNECE_deadwood.csv',encoding= 'unicode_escape', header=[0,1])
UNECE_deadwood.columns = UNECE_deadwood.columns.map('_'.join)
UNECE_deadwood.rename_axis('Date').reset_index()
#TEST
#UNECE_deadwood.to_csv('C:/Users/Klara/Documents/Prace/JRC/Teleworking/2022/forest_condition/deadwood/chart/UNECE_deadwood_test.csv')

#put the stats into dataframes
UNECE_deadwood = pandas.DataFrame(UNECE_deadwood)
#reame the first column as COUNTRY
UNECE_deadwood.rename(columns={UNECE_deadwood.columns[0]: "ENG_NAME"}, inplace = True)
#Choose rrelevant columns
UNECE_deadwood = UNECE_deadwood[['ENG_NAME', 'Forest - 2015 (m?/ha)_Total', 'Forest - 2010 (m?/ha)_Total']]
#test
#UNECE_deadwood.to_csv('C:/Users/Klara/Documents/Prace/JRC/Teleworking/2022/forest_condition/deadwood/chart/UNECE_deadwood_test.csv')

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

#prepare dataframe for the chart - set index for country
UNECE_deadwood_EU27= UNECE_deadwood_EU27.set_index("Country")
print(UNECE_deadwood_EU27.to_string())

#plot bar chart for UNECE deadwood
UNECE_deadwood_EU27.plot.bar(
ylabel="Deadwood(m3/ha)", xlabel="Country", width=1, edgecolor = "black", color = 'lightsteelblue', title="Deadwood amount EU27", legend=None)
# plt.ylim(bottom=0, top=120)
# plt.savefig('C:/Users/Klara/Documents/Prace/JRC/Teleworking/2022/Forest area EU/Data/output_charts/CLC_EU24.png')
plt.show()
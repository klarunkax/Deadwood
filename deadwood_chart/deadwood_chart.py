import pandas
import os
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np


os.chdir('C:/Users/Klara/Documents/Prace/JRC/Teleworking/2022/forest_condition/deadwood/chart')
##UNECE DEADWOOD DATA
# #load the csv table a put first 2 rows into a single HEADER
# UNECE_deadwood = pandas.read_csv('UNECE_deadwood.csv',encoding= 'unicode_escape', header=[0,1])
# UNECE_deadwood.columns = UNECE_deadwood.columns.map('_'.join)
# UNECE_deadwood.rename_axis('Date').reset_index()
# #TEST
# #UNECE_deadwood.to_csv('C:/Users/Klara/Documents/Prace/JRC/Teleworking/2022/forest_condition/deadwood/chart/UNECE_deadwood_test.csv')
#
# #put the stats into dataframes
# UNECE_deadwood = pandas.DataFrame(UNECE_deadwood)
# #reame the first column as COUNTRY
# UNECE_deadwood.rename(columns={UNECE_deadwood.columns[0]: "ENG_NAME"}, inplace = True)
# #Choose rrelevant columns
# UNECE_deadwood = UNECE_deadwood[['ENG_NAME', 'Forest - 2015 (m?/ha)_Total', 'Forest - 2010 (m?/ha)_Total']]
# #test
# #UNECE_deadwood.to_csv('C:/Users/Klara/Documents/Prace/JRC/Teleworking/2022/forest_condition/deadwood/chart/UNECE_deadwood_test.csv')
#
# #load csv with Europe names and limit for the EU27
# Europe = pandas.read_csv('Countries extended CODES_eea.csv')
# EU27 = Europe[Europe["EU27"] == 1]
# EU27 = EU27[['ISO3_CODE', 'ENG_NAME']]
#
# #merge deadwood data with names
# UNECE_deadwood_EU27 = EU27.merge(UNECE_deadwood, how='left', on="ENG_NAME")
#
# #fill the missing values of 2015 with 2010
# UNECE_deadwood_EU27['Forest - 2015 (m?/ha)_Total']= UNECE_deadwood_EU27['Forest - 2015 (m?/ha)_Total'].fillna(UNECE_deadwood_EU27['Forest - 2010 (m?/ha)_Total'])
#
# #keep only 2015 column
# UNECE_deadwood_EU27 = UNECE_deadwood_EU27[['ENG_NAME', 'Forest - 2015 (m?/ha)_Total']]
#
# #rename column - Forest - 2015 (m?/ha)_Total
# UNECE_deadwood_EU27 = UNECE_deadwood_EU27.rename(columns={'Forest - 2015 (m?/ha)_Total': 'Deadwood', 'ENG_NAME':'Country'})
#
# #prepare dataframe for the chart - set index for country
# UNECE_deadwood_EU27= UNECE_deadwood_EU27.set_index("Country")
# print(UNECE_deadwood_EU27.to_string())
#
# #plot bar chart for UNECE deadwood
# UNECE_deadwood_EU27.plot.bar(
# ylabel="Deadwood(m3/ha)", xlabel="Country", width=1, edgecolor = "black", color = 'lightsteelblue', title="Deadwood amount EU27", legend=None)
# # plt.ylim(bottom=0, top=120)
# # plt.savefig('C:/Users/Klara/Documents/Prace/JRC/Teleworking/2022/Forest area EU/Data/output_charts/CLC_EU24.png')
# plt.show()

##DEADWOOD DATA FOR REF. SITES
REFSITES_deadwood = pandas.read_csv('literature_review_deadwood_organized.csv')
REFSITES_deadwood = pandas.DataFrame(REFSITES_deadwood)
REFSITES_deadwood = REFSITES_deadwood[['Bioregion', 'Country', 'Deadwood']]
REFSITES_deadwood = REFSITES_deadwood.dropna()
#REFSITES_deadwood["Bioregion_Country"] = REFSITES_deadwood["Bioregion"] + REFSITES_deadwood["Country"]
REFSITES_deadwood = REFSITES_deadwood.astype({'Deadwood':'float64'})
# bioregions = REFSITES_deadwood['Bioregion'].tolist()
# bioregions= tuple(bioregions)
# REFSITES_deadwood = pandas.pivot_table(REFSITES_deadwood, values='Deadwood', index=['Country'],
#                              aggfunc={
#                              bioregions: [min, max, np.mean]})


REFSITES_min_max_avg= (REFSITES_deadwood.groupby(['Country','Bioregion'])['Deadwood']
         .agg(['mean','min','max'])
         .reset_index())
REFSITES_min_max_avg.to_csv('C:/Users/Klara/Documents/Prace/JRC/Teleworking/2022/forest_condition/deadwood/chart/REFSITES_min_max_avg.csv')
print(REFSITES_min_max_avg)

#print(REFSITES_deadwood.to_string())
#
# # # Select jobs for which you want the salaries to be displayed on the graph
# Countries = min_max_avg['Country'].tolist()
# # def get_grp(x, min_max_avg, col_name, my_list):
# #     for c in my_list:
# #         if c in min_max_avg[col_name][x]:
# #             return c
# # #
# # selected = min_max_avg.loc[min_max_avg['Country'].isin(Countries)]
# # selected = selected.groupby(lambda x : get_grp(x, min_max_avg, 'Country', Countries))
# # table = selected.mean()
# # table.sort_values(['mean'], ascending=[True], inplace=True)
# # print(table)
# #
# min_max_avg = min_max_avg.set_index(['Country', 'Bioregion'])
# print(min_max_avg)
# # #1. Create subplots
# #First, set Seaborn styles with the chosen face color:
# sns.set(rc={'axes.facecolor':'#EBDCB2'})
# fig, ax = plt.subplots(figsize=(10,5), facecolor=(.94, .94, .94))
# plt.tight_layout()
# #
# # #2. Create bars
# means = min_max_avg['mean']
# mins = min_max_avg['min']
# maxes = min_max_avg['max']
#
# ax.errorbar(min_max_avg.index, means, [means - mins, maxes - means],
#             fmt='D',
#             mfc = '#C9A66B',
#             mec = '#662E1C',
#             ms = 16,
#             mew = 3,
#             ecolor='#AF4425',
#             lw=3,
#             ls = ':',
#             color='#AF4425')
# #
# # #3. Create ticks and labels
# font_color = '#525252'
#
# # # Create ticks and set their color
# plt.xticks(color=font_color)
# plt.yticks(color=font_color)
#
# # # Set ticks’ font size
# for label in (ax.get_xticklabels() + ax.get_yticklabels()):
#     label.set_fontsize(5)
# #
# # # Create y-axis label
# ax.set_ylabel('Deadwood amount m3/ha', color=font_color, fontsize=16)
#
# # # 4. Set title and subtitle
# # # Set the title and subtitle
# title = plt.title('Deadwood amount m3/ha EU countries', y=.95, fontsize=20, color=font_color)
# #
# # # Set title position
# title.set_position([.5, 1])
#
# # # Adjust subplots so that the title, subtitle, and labels would fit
# plt.subplots_adjust(top=0.8, bottom=0.2, left=0.1, right=0.9)
#
# # #5. Save the chart as a picture
# filename = 'mpl-errorbar'
# plt.savefig(filename+'.png', facecolor=(.94, .94, .94))


#%%

#importing libraries
import pandas as pd   
import altair as alt   
import altair_saver as alt_s
from altair import datum
import os
import numpy as np

#%%

#importing csv data to first data_set, japan_pop
japan_pop = pd.read_csv("CSVFILES/Japan_population_data.csv")


# %%

#check japan_pop data

japan_pop.head()

#%%
#year and population are both float, which would complicate calculations. I will convert them both to int

# converting 'Weight' from float to int
japan_pop['year'] = japan_pop['year'].astype(int)



#%%
# check whether datatypes are converted
display(japan_pop.dtypes)







#%%
# Import a different dataset into a new dataframe called japan_price. This was quite a challenge because there were 47 csv files for the dataset. I don't think I'll end up using it in this data analysis project because the timeframes are different. 


filesnames = os.listdir('CSVFILES/trade_prices')
filesnames = [f for f in filesnames if f.lower().endswith(".csv")]
print(filesnames)


japan_price = pd.read_csv(f'CSVFILES/01csv/01.csv')

for filename in filesnames:
     df = pd.read_csv(f'CSVFILES/trade_prices/{filename}')
     japan_price.append(df)





# %%

#check japan_price data

japan_price.head()
display(japan_price.dtypes)


# %%
#query japan's population in the year of 2015

twenty15 = japan_pop.query('year == 2015')

#%%
# sort all prefectures by population, in descending order
prefecture_pop_2015 = (twenty15
    .groupby(['prefecture']).sum()
    .filter(['population'])
    .sort_values('population',ascending=[False] ))

prefecture_pop_2015.to_markdown()

# %%
#sum japans population in the year of 2015
pop_2015 = twenty15['population'].sum()
pop_2015
# %%



# %%
# %%
#Create a new column called pct_pop_change that calculates the percentage change of population 
japan_pop['pct_pop_change'] = japan_pop['population'].pct_change()
japan_pop



 
# %%
island_groupby = japan_pop.groupby(['island'])
island_groupby.head()

# %%
#assign only the data with island == hokkaido
hokkaido = japan_pop.query('island=="Hokkaido"')
print(hokkaido)

#do the same for the other 3 largest islands
honshu = japan_pop.query('island=="Honshu"')



kyushu = japan_pop.query('island=="Kyushu"')


shikoku = japan_pop.query('island=="Shikoku"')

#Examine japan_pop with new hokkaido filter 

hokkaido_2015 = hokkaido.query('year==2015.0000')

hokkaido_2015.head()

# %%
#Create 4 bar charts in the map folder of the population of Japan from the 1870s to 2015 

chart = alt.Chart(hokkaido).properties(title="Hokkaido").encode(
    x=alt.X('year', title = "Year"),
    y=alt.Y('population',title = "Population"),
).mark_bar(size=1)
chart.save("MAPS/hokkaido.png")

chart2 = alt.Chart(honshu).properties(title="Honshu").encode(
    x=alt.X('year', title = "Year"),
    y=alt.Y('population',title = "Population"),
).mark_bar(size=1)
chart.save("MAPS/honshu.png")


chart3 = alt.Chart(kyushu).properties(title="Kyushu").encode(
    x=alt.X('year', title = "Year"),
    y=alt.Y('population',title = "Population"),
).mark_bar(size=1)
chart.save("MAPS/kyushu.png")


chart4 = alt.Chart(shikoku).properties(title="Shikoku").encode(
    x=alt.X('year', title = "Year"),
    y=alt.Y('population',title = "Population"),
).mark_bar(size=1)
chart.save("MAPS/shikoku.png")
# %%
# calculate the increase or decrease of the population of each major japanese island from 2000 to 2015

pop_2000 = (japan_pop[japan_pop.year==2000]
    .groupby(['island']).population.sum()
    .sort_index(ascending=[False] )).rename("pop2000")


pop_2015 =(japan_pop[japan_pop.year==2015]
    .groupby(['island']).population.sum()
    .sort_index(ascending=[False] )).rename("pop2015")

pop_2000.head()

a = pd.concat([pop_2015,pop_2000], axis=1)

a['island_pct_change'] = ((a.pop2015 - a.pop2000) / a.pop2000 * 100)


a.to_markdown(tablefmt="grid")


# %%

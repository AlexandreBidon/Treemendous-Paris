# import required packages
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set_theme(style="ticks", color_codes=True)
import geopandas as gpd
from geopandas import GeoDataFrame
import json
# load data
df = pd.read_csv(
    filepath_or_buffer='data/les-arbres-plantes.csv',
    sep=";")

df = df.drop('geo_shape', axis=1)
df = df.drop("Emplacement - Complément d'adresse", axis=1)
df = df.rename(columns={'Emplacement - Arrondissement': 'quartier'})

df[['Latitude', 'Longitude']] = df['geo_point_2d'].str.split(', ', n=1, expand=True)

df.Latitude = df.Latitude.astype(float)
df.Longitude = df.Longitude.astype(float)
df['quartier'] = df.quartier.astype('category')

print (df['quartier'].cat.categories)

df = df[~df['quartier'].isin(["SEINE-SAINT-DENIS", "HAUTS-DE-SEINE", "VAL-DE-MARNE"])]

df = df.drop('geo_point_2d', axis=1)

print(df.head())

df.to_csv("processed_data.csv")

paris_geojson = gpd.read_file("data/arrondissements.geojson")

fig, ax = plt.subplots(
        figsize = (10,8)
    )

paris_geojson.boundary.plot(ax = ax, edgecolor = 'black')

sns.scatterplot(
    x=df['Longitude'], 
    y=df['Latitude'], 
    marker = 'o', 
    hue = df['quartier'],
    ax = ax
    )
                
# move the legend to the right of the plot
ax.legend(loc = 'center right', bbox_to_anchor=(1.7, 0.5), ncol=1) 

ax.axis('off')
plt.show()

# def animate_map(time_col, data_df):
#     fig = px.scatter_mapbox(data_df,
#               lat="Latitude" ,
#               lon="Longitude",
#               hover_name="Emplacement - Arrondissement",
#               color="Emplacement - Arrondissement",
#               animation_frame=time_col,
#               mapbox_style='carto-positron',
#               category_orders={
#               time_col:list(np.sort(data_df[time_col].unique()))
#               },                  
#               zoom=10)
#     fig.show();

# animate_map(time_col='Arbre Exploitation - Planté le', data_df = df)


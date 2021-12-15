import pandas as pd             # data package
import matplotlib.pyplot as plt # graphics 
import datetime as dt
import numpy as np

# these are new 
import requests, io             # internet and input tools  
import zipfile as zf            # zip file tools 
import shutil                   # file management tools 
import os                       # operating system tools (check files)

from census import Census # This is new...

import geopandas as gpd # this is the main geopandas 
from shapely.geometry import Point, Polygon # also needed

import pyarrow as pa
import pyarrow.parquet as pq
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1 import make_axes_locatable

df = pd.read_csv("https://github.com/nytimes/covid-19-data/raw/master/us-counties.csv")
nyc = df.county == "New York City"
df.loc[nyc,"fips"] = 36061
df["date"] = pd.to_datetime(df["date"], format = "%Y-%m-%d")# Convert the date to a datetime object
latest_date = df.date.max()
latest_date = latest_date.strftime("%m/%d/%Y")
df.set_index("date", inplace = True)
dfall = df.loc[latest_date].copy()
dfall[dfall.county == "New York City"]
total = dfall.cases.sum()
print("Total US Covid-19 Cases", total, "as of", latest_date)
total_deaths = dfall.deaths.sum()
print("Total US Covid-19 Deaths", total_deaths, "as of", latest_date)
dfall[dfall["fips"] == 36061]

#get county shape and state shape
map_projection = "epsg:2163"
county_shape ="/Users/yananliu/Documents/5725/FinalProject/shapefiles-county/tl_2017_us_county.shx"
#county_shape = "shapefiles-county/tl_2017_us_county.shx"

us_map = gpd.read_file(county_shape)

us_map = us_map.to_crs({'init': map_projection })
us_map["geometry"] = us_map["geometry"].simplify(200)
# This was important. The geometry in the tigerline file si
# too fine, orginal map was 350mb. simply basicly simplifies the geometry,
# making the map take up less memory and load faster. Still not sure
# what the number exactly means.
us_map["area_fips"] = (us_map.STATEFP.astype(str) + us_map.COUNTYFP.astype(str)).astype(int)
us_map = us_map.merge(dfall, left_on='area_fips',
                      right_on = "fips", how = "left", indicator = True)
nyc_counties = [36081,36005,36085,36047]

us_map.loc[us_map.area_fips.isin(nyc_counties), "deaths"] = us_map.loc[us_map.area_fips == 36061,"deaths"].values[0]

us_map.loc[us_map.area_fips.isin(nyc_counties), "cases"] = us_map.loc[us_map.area_fips == 36061,"cases"].values[0]

us_map["Notes"] = ""

all_nyc_counties = [36081,36005,36085,36047,36061]

us_map.loc[us_map.area_fips.isin(all_nyc_counties), "Notes"] = "NYC counties are treated as one region"
all_nyc_counties = [36081,36005,36085,36047,36061]

us_map.loc[us_map.area_fips.isin(all_nyc_counties)]
us_map.set_index("STATEFP", inplace = True)

drop_list = ["02","15","72","78","69","66","60",]

us_map.drop(drop_list, inplace = True)
state_shape = "/Users/yananliu/Documents/5725/FinalProject/shapefiles-state/tl_2017_us_state.shx"

state_map = gpd.read_file(state_shape)

state_map = state_map.to_crs({'init': map_projection })

state_map["geometry"] = state_map["geometry"].simplify(200)
state_fp_dict = dict(zip(state_map.STATEFP, state_map.STUSPS))
state_map.set_index("STATEFP", inplace = True)

drop_list = ["02","15","72","78","69","66","60",]

state_map.drop(drop_list, inplace = True)
us_map.reset_index(inplace = True)
us_map["STSPS"] = us_map["STATEFP"].map(state_fp_dict)
us_map["NAME"] = us_map["NAME"] + ", " + us_map["STSPS"]
us_map.set_index("STATEFP", inplace = True)
us_map["cases_label"] = us_map["cases"].round(0)

us_map["cases_label"] = us_map["cases_label"].map('{:,.0f}'.format)

us_map["deaths_label"] = us_map["deaths"].round(0)

us_map["deaths_label"] = us_map["deaths_label"].map('{:,.0f}'.format)
my_api_key = '34e40301bda77077e24c859c6c6c0b721ad73fc7'
# This is my api_key, 

c = Census(my_api_key)
# This will create an object c which has methods associated with it.

code = ("NAME","B01001_001E") 
# Get more stuff from the cencuss if we want...

county_2017 = pd.DataFrame(c.acs5.get(code, 
                                         {'for': 'county:*'}, year=2017))
county_2017 = county_2017.rename(columns = {"B01001_001E":"2017_population"})

county_2017["GEOFIPS"] = (county_2017["state"] + county_2017["county"]).astype(int)

county_2017["2017_population"] = county_2017["2017_population"].astype(float)

county_2017.set_index(["GEOFIPS"], inplace = True)

us_map = us_map.merge(county_2017[["2017_population"]], 
                      left_on='area_fips', right_on = "GEOFIPS", how = "left")
us_map["pop_label"] = us_map["2017_population"].map('{:,.0f}'.format)
q_cases = [0,1,5,10,100,250,500,1000,5000,10000,np.inf]
us_map["q_cases"]= pd.cut(us_map["cases"],q_cases, labels=range(0,10))
#
us_map["q_deaths"]= pd.cut(us_map["deaths"],q_cases, labels=range(0,10))
us_map["q_deaths"].max()
us_map["cases_label"].replace("nan", "None reported", inplace = True)
us_map["deaths_label"].replace("nan", "None reported", inplace = True)

fig, ax = plt.subplots(1,1,figsize = (10,6))

plt.tight_layout()
plt.rcParams.update(plt.rcParamsDefault) # This will reset defaluts...

#################################################################################
# This is for the colorbar...

divider = make_axes_locatable(ax)

cax = divider.append_axes("right", size="3%", pad=0.1)

#################################################################################
## This creates a discrete colorbar scheme...
# https://gist.github.com/jakevdp/91077b0cae40f8f8244a

N = 10

base = plt.cm.get_cmap("RdBu_r")

color_list = base(np.linspace(0, 1, N))

cmap_name = base.name + str(N)

dcmap =  base.from_list(cmap_name, color_list, N)

#################################################################################
# This is the normal mapping...

#us_map[us_map.q_cases.isna()].plot(alpha = 0.25, color = "grey", ax = ax,)

us_map.plot(column='q_cases', ax = ax,
              # THIS IS NEW, it says color it based on this column
             cmap=dcmap, 
             alpha = 0.75,
             vmin=0, vmax=us_map.q_cases.max())

#################################################################################
# This then alows me to generate and edit the colorbar....
# https://stackoverflow.com/questions/53158096/editing-colorbar-legend-in-geopandas

sm = plt.cm.ScalarMappable(cmap=dcmap)
sm._A = []
cbr = fig.colorbar(sm, cax=cax)

cbr.set_label('Number of Covid Cases')
cbr.set_alpha(0.15)

cbr.set_ticks([0, 0.10, 0.20, 0.30,0.40,0.50,0.60,0.70,0.80, 0.90])
q_cases = [0,1,5,10,100,250,5000,10000,50000,100000,np.inf]
cbr.set_ticklabels(q_cases, update_ticks=True)

state_map.geometry.boundary.plot(color=None, edgecolor='k', alpha = 0.35, ax = ax)



ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)

ax.get_xaxis().set_visible(False)

ax.get_yaxis().set_visible(False)

#title = "Covid-19 Cases by County as of " + latest_date + ", Total Cases: " + f"{total:,d}"
#title_death = "Covid-19 Deaths by County as of " + latest_date + ", Total Deaths: " + f"{total_deaths:,d}"
#ax.set_title(title, fontsize = 10, loc= "left" )

plt.savefig("covid-19-map.png", bbox_inches = "tight", dip = 1200)
plt.show()
import requests
import pandas as pd
import psycopg2 
import csv

pd.set_option('display.max_rows', None)

from sqlalchemy import create_engine
#conn_string = 'postgresql://postgres:unsecurepwd1!@host.docker.internal:5432/analysis'
conn_string = 'postgresql://postgres:LrCRabhrawVTSBhQCvWgTgvPqCTJVpgu@monorail.proxy.rlwy.net:54587/postgres'
  
db = create_engine(conn_string) 
conn = db.connect()


# Replace 'API_KEY' with your actual API key from NewsAPI
API_KEY = 'fb3b9eb1459344b2a9924552242303'
url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q=Portland&aqi=yes"
response = requests.get(url)


# Call API and Check if the response is successful
if response.status_code == 200:
    data = response.json()
    
# Copy 'current' chunk of response data and put into pandas dataframe
cc_dict = [data['current']]
df_cc = pd.DataFrame.from_dict(cc_dict, orient='columns')

# Copy Air Quality data into new dataframe
aq_dict = [data['current']['air_quality']]
df_aq = pd.DataFrame.from_dict(aq_dict, orient='columns') 

# Merge current and air quality into one large dataframe
df_aq_plus_cc = df_cc.merge(df_aq, right_index=True, left_index=True)

# Copy Condition data into its own dataframe
cond_dict = [data['current']['condition']]
df_cond = pd.DataFrame.from_dict(cond_dict, orient='columns')

# Merge condition data into the current and air quality data.  Drop unnecessary columns.  Rename a couple of columns that postgres won't like
df_all = df_aq_plus_cc.merge(df_cond, right_index=True, left_index=True)
df_final = df_all.drop(columns=['air_quality', 'last_updated_epoch', 'temp_c', 'wind_kph', 'precip_mm', 'feelslike_c', 'vis_km', 'gust_kph','condition', 'code'])
df_final = df_final.rename({'us-epa-index': 'us_epa_index', 'gb-defra-index': 'gb_defra_index'}, axis=1)

# Send dataframe data to current_conditions table
df_final.to_sql('current_conditions', con=conn, if_exists='append', index=False)
    
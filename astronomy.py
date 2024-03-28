import requests
import pandas as pd
import psycopg2 
import csv
from datetime import date

pd.set_option('display.max_rows', None)

from sqlalchemy import create_engine
#conn_string = 'postgresql://postgres:unsecurepwd1!@host.docker.internal:5432/analysis'
conn_string = 'postgresql://postgres:LrCRabhrawVTSBhQCvWgTgvPqCTJVpgu@monorail.proxy.rlwy.net:54587/postgres'
  
db = create_engine(conn_string) 
conn = db.connect()

curr_date = date.today()
# set up the API key and URL to call the weather api
API_KEY = 'fb3b9eb1459344b2a9924552242303'
url = f"https://api.weatherapi.com/v1/astronomy.json?q=Portland&dt={curr_date}&key={API_KEY}"
response = requests.get(url)


# Call API and Check if the response is successful
if response.status_code == 200:
    data = response.json()
    #print(data['astronomy']['astro'])

astro_dict = [data['astronomy']['astro']]
df_astro = pd.DataFrame.from_dict(astro_dict, orient='columns')

# Send dataframe data to astronomy table
df_astro.to_sql('astronomy', con=conn, if_exists='append', index=False)
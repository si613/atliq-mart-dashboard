import pandas as pd
import sqlite3
import os

#Set paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'retail_events_db.sqlite')

#Load csv files
df_campaigns = pd.read_csv(os.path.join(DATA_DIR, 'dim_campaigns.csv'))
df_products = pd.read_csv(os.path.join(DATA_DIR, 'dim_products.csv'))
df_stores = pd.read_csv(os.path.join(DATA_DIR, 'dim_stores.csv'))
df_events = pd.read_csv(os.path.join(DATA_DIR, 'fact_events.csv'))

##Connecting to SQLite
conn = sqlite3.connect(DB_PATH)

# Loading the dataframes into the database
df_campaigns.to_sql('dim_campaigns', conn, if_exists='replace', index=False)
df_products.to_sql('dim_products', conn, if_exists='replace', index=False)
df_stores.to_sql('dim_stores', conn, if_exists='replace', index=False)
df_events.to_sql('fact_events', conn, if_exists='replace', index=False)

#Closing the connection
conn.close()

print("✅ Data loaded successfully into retail_events_db.sqlite")

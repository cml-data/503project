import os
import psycopg2
import requests
import json
import time

# connect to the database
def connect_to_database(dbname):
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', '5432')
    user = os.environ.get('DB_USER', 'noellematthews')

    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        dbname=dbname,
        password=None  # No password
    )
    return conn

# tomtom API key
API_KEY = "89800236-7eda-41a6-89ea-06e8246c7119"

# url for traffic incidents endpoint
INCIDENTS_URL = f"https://api.tomtom.com/traffic/services/4/incidentDetails/3/10/en/json?key={API_KEY}"

# url for traffic flow endpoint
FLOW_URL = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={API_KEY}"

# fetch traffic incidents data
def fetch_traffic_incidents():
    response = requests.get(INCIDENTS_URL)
    if response.status_code == 200:
        incidents_data = response.json()
        return incidents_data
    else:
        print(f"Failed to fetch traffic incidents: {response.status_code}")
        return None

# fetch traffic flow data
def fetch_traffic_flow():
    response = requests.get(FLOW_URL)
    if response.status_code == 200:
        flow_data = response.json()
        return flow_data
    else:
        print(f"Failed to fetch traffic flow: {response.status_code}")
        return None

def main():
    # connect to the databases
    conn_flow = connect_to_database('traffic_flow')
    conn_incidents = connect_to_database('traffic_incidents')
    
    while True:
        # traffic incidents
        incidents_data = fetch_traffic_incidents()
        if incidents_data:
            # Process and store the incidents data in the database
            pass # Placeholder for processing and storing data
            
        # traffic flow
        flow_data = fetch_traffic_flow()
        if flow_data:
            # Process and store the flow data in the database
            pass # Placeholder for processing and storing data
            
        # sleep 1hr before fetching again
        time.sleep(3600)

if __name__ == "__main__":
    main()

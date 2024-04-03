import os
import psycopg2
import requests
import json
import time

# database connection function
def connect_to_database():
    host = "127.0.0.1"
    port = os.environ.get('DB_PORT', '5432')
    user = os.environ.get('DB_USER', 'noellematthews')
    dbname = os.environ.get('DB_NAME', 'postgres')  # Connect to the default database
    
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        dbname=dbname,
        password=None  # No password
    )
    
    # search path to include the "public" schema
    cursor = conn.cursor()
    cursor.execute("SET search_path TO public")
    conn.commit()
    cursor.close()
    
    return conn

# insert traffic incidents data into the database
def insert_traffic_incidents(conn, data):
    cursor = conn.cursor()
    for incident in data:
        cursor.execute("""
            INSERT INTO traffic_incidents (start_location, end_location, road_name, type_of_delay, delay_length, significance, distance, incident_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            incident['start_location'],
            incident['end_location'],
            incident['road_name'],
            incident['type_of_delay'],
            incident['delay_length'],
            incident['significance'],
            incident['distance'],
            incident['incident_time']
        ))
    conn.commit()
    cursor.close()

# insert traffic flow data into the database
def insert_traffic_flow(conn, data):
    cursor = conn.cursor()
    for flow in data:
        cursor.execute("""
            INSERT INTO traffic_flow (segment_id, current_speed, freeflow_speed, quality_indicator, flow_time)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            flow['segment_id'],
            flow['current_speed'],
            flow['freeflow_speed'],
            flow['quality_indicator'],
            flow['flow_time']
        ))
    conn.commit()
    cursor.close()

# fetch traffic incidents data from the TomTom API
def fetch_traffic_incidents():
    # TomTom API key
    API_KEY = "6JGAhG8TKRPO076GGtGX01KasigzxFR4"
    
    # URL for traffic incidents endpoint
    INCIDENTS_URL = f"https://api.tomtom.com/traffic/services/4/incidentDetails/3/10/en/json?key={API_KEY}"

    response = requests.get(INCIDENTS_URL)
    if response.status_code == 200:
        incidents_data = response.json()
        return incidents_data
    else:
        print(f"Failed to fetch traffic incidents: {response.status_code}")
        return None

# fetch traffic flow data from the TomTom API
def fetch_traffic_flow():
    # TomTom API key
    API_KEY = "89800236-7eda-41a6-89ea-06e8246c7119"
    
    # url for traffic flow endpoint
    FLOW_URL = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={API_KEY}"

    response = requests.get(FLOW_URL)
    if response.status_code == 200:
        flow_data = response.json()
        return flow_data
    else:
        print(f"Failed to fetch traffic flow: {response.status_code}")
        return None

def main():
    # connect to the database
    conn = connect_to_database()
    # fetch data and insert into tables
    while True:
        # traffic incidents
        incidents_data = fetch_traffic_incidents()
        if incidents_data:
            # process and store the incidents data in the database
            insert_traffic_incidents(conn, incidents_data)
            
        # traffic flow
        flow_data = fetch_traffic_flow()
        if flow_data:
            # process and store the flow data in the database
            insert_traffic_flow(conn, flow_data)
            
        # sleep 1 hour before fetching again
        time.sleep(3600)

if __name__ == "__main__":
    main()

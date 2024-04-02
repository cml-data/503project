import requests
import json
import time

# TomTom API key
API_KEY = "89800236-7eda-41a6-89ea-06e8246c7119"

# URL for traffic incidents endpoint
INCIDENTS_URL = f"https://api.tomtom.com/traffic/services/4/incidentDetails/3/10/en/json?key={API_KEY}"

# URL for traffic flow endpoint
FLOW_URL = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={API_KEY}"

def fetch_traffic_incidents():
    """
    Fetches traffic incident data from the TomTom API.
    """
    response = requests.get(INCIDENTS_URL)
    if response.status_code == 200:
        incidents_data = response.json()
        # Process the incidents data and return as needed
        return incidents_data
    else:
        print(f"Failed to fetch traffic incidents: {response.status_code}")
        return None

def fetch_traffic_flow():
    """
    Fetches traffic flow data from the TomTom API.
    """
    response = requests.get(FLOW_URL)
    if response.status_code == 200:
        flow_data = response.json()
        # Process the flow data and return as needed
        return flow_data
    else:
        print(f"Failed to fetch traffic flow: {response.status_code}")
        return None

def main():
    while True:
        # Fetch traffic incidents
        incidents_data = fetch_traffic_incidents()
        if incidents_data:
            # Process and store the incidents data in the database

        # Fetch traffic flow
        flow_data = fetch_traffic_flow()
        if flow_data:
            # Process and store the flow data in the database

        # Sleep for 1 hour before fetching data again
        time.sleep(3600)

if __name__ == "__main__":
    main()


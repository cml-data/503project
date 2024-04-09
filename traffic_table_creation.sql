CREATE TABLE traffic_data (
    route VARCHAR(255),
    free_flow_time INT,
    travel_time INT,
    scrape_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

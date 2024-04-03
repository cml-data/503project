-- table for storing traffic incident data
CREATE TABLE traffic_incidents (
    incident_id SERIAL PRIMARY KEY,
    start_location VARCHAR(255),
    end_location VARCHAR(255),
    road_name VARCHAR(255),
    type_of_delay VARCHAR(255),
    delay_length INT,
    significance VARCHAR(255),
    distance INT,
    incident_time TIMESTAMP
);

-- table for storing traffic flow data
CREATE TABLE traffic_flow (
    flow_id SERIAL PRIMARY KEY,
    segment_id INT,
    current_speed INT,
    freeflow_speed INT,
    quality_indicator INT,
    flow_time TIMESTAMP
);

-- create table (don't repeat)
CREATE TABLE portland_events (
  raw_json JSONB,
  date_of_scrape timestamp default CURRENT_TIMESTAMP
);

-- this worked to get all events in a single column (don't do)
select date,
	raw_json ->> 'events_results' as result
from portland_events;

-- this worked to separate out title, location, and date for each event in events_results --> do this first time!
CREATE TABLE update_pdx_events AS (
SELECT
    date_of_scrape,
    event->>'title' AS title,
    (event->'address'->>0) || ', ' || (event->'address'->>1) AS location,
    (event->'date'->>'when') AS date
FROM
    portland_events,
    jsonb_array_elements(raw_json -> 'events_results') AS event
);

-- use this to update table after each scrape
INSERT INTO update_pdx_events 
SELECT 
	date_of_scrape,
    event->>'title' AS title,
    (event->'address'->>0) || ', ' || (event->'address'->>1) AS location,
    (event->'date'->>'when') AS date
FROM
    portland_events,
    jsonb_array_elements(raw_json -> 'events_results') AS event;
    
-- then clear scraper table    
DELETE FROM portland_events;
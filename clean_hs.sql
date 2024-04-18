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

-- load data

-- clear table/drop tables as needed
DELETE FROM update_pdx_events;
delete from pdx_events;
drop table pdx_events;

-- create new table
create table pdx_events (
  date_of_scrape timestamp,
  title text,
  location text,
  date text
);

-- load data
copy pdx_events
from '/Users/Haleigh/repos/503project/update_pdx_events.csv'
delimiter ',' csv header;

-- ------------------------
-- ------------------------

-- put in 3nf

-- convert date_of_scrape to only date
ALTER TABLE pdx_events
ALTER COLUMN date_of_scrape TYPE DATE USING date_of_scrape::DATE;

-- ------------------------

-- change "today" to actual date
UPDATE pdx_events
SET date = REPLACE(date, 'Today', TO_CHAR(date_of_scrape, 'YYYY-MM-DD'))
WHERE date LIKE 'Today%';

-- ------------------------

-- change several days to the same format
-- Add new columns for start_time and end_time
ALTER TABLE pdx_events
ADD COLUMN start_time text;

-- Temporary table to hold the updated rows
CREATE TEMP TABLE temp_pdx_events AS
SELECT
    date_of_scrape,
    title,
    location,
    date
FROM pdx_events;

-- Delete rows with the original entries
DELETE FROM pdx_events;

-- Insert new rows with individual dates and times
-- For entries like "Mon, Mar 25 – Tue, Mar 26"
INSERT INTO pdx_events (date_of_scrape, title, location, date)
SELECT
    date_of_scrape,
    title,
    location,
    TRIM(SPLIT_PART(date, '–', 1)) AS date
FROM temp_pdx_events
WHERE date SIMILAR TO '%[A-Za-z]{3}, [A-Za-z]{3} [0-9]+ – [A-Za-z]{3}, [A-Za-z]{3} [0-9]+%'; -- Using regular expression pattern

-- Insert another row for the second date in the range
INSERT INTO pdx_events (date_of_scrape, title, location, date)
SELECT
    date_of_scrape,
    title,
    location,
    TRIM(SPLIT_PART(date, '–', 2)) AS date
FROM temp_pdx_events
WHERE date SIMILAR TO '%[A-Za-z]{3}, [A-Za-z]{3} [0-9]+ – [A-Za-z]{3}, [A-Za-z]{3} [0-9]+%'; -- Using regular expression pattern

-- For entries like "2024-03-24, 7 - 9pm"
INSERT INTO pdx_events (date_of_scrape, title, location, date, start_time)
SELECT
    date_of_scrape,
    title,
    location,
    TRIM(SPLIT_PART(date, ',', 1)) AS date,
    CASE WHEN POSITION('-' IN date) > 0 THEN TRIM(SPLIT_PART(SPLIT_PART(date, ',', 2), '-', 1)) END AS start_time
FROM temp_pdx_events
WHERE date NOT SIMILAR TO '%[A-Za-z]{3}, [A-Za-z]{3} [0-9]+ – [A-Za-z]{3}, [A-Za-z]{3} [0-9]+%'; -- Using regular expression pattern

-- Drop the temporary table
DROP TABLE temp_pdx_events;


-- ------------------------

-- rename start time
ALTER TABLE pdx_events
RENAME COLUMN start_time TO time;

-- ------------------------

-- change from Mon, Mar 25 to date
UPDATE pdx_events
SET date = 
    CASE 
        WHEN date SIMILAR TO '%[A-Za-z]{3}, [A-Za-z]{3} [0-9]+%' THEN 
            TO_CHAR(TO_DATE(date, 'Dy, Mon DD'), 'YYYY-MM-DD')
        ELSE 
            date
    END;

-- fix the errors where it changed it to 0001
UPDATE pdx_events
SET date = CONCAT('2024-', SUBSTRING(date FROM 6))
WHERE date LIKE '0001-%';


-- ------------------------
-- ------------------------

-- now create schema
CREATE SCHEMA IF NOT EXISTS project;

DROP TABLE IF EXISTS project.date;
DROP TABLE IF EXISTS project.events;

CREATE TABLE project.date (
  id INT PRIMARY KEY,
  date date NOT NULL
);

CREATE TABLE project.events (
  id INT,
  title text,
  location text,
  time text,
  date_id INT,
  constraint fk_date foreign key (date_id) references project.date (id),
  constraint comp_key primary key (id, date_id)
);  

-- ------------------------

-- work with current table to get it ready to fill in new tables
  
-- Insert unique dates from pdx_events into project.date with serial id
INSERT INTO project.date (id, date)
SELECT ROW_NUMBER() OVER () AS id, date::date
FROM (
    SELECT DISTINCT date
    FROM pdx_events
) AS unique_dates;

-- add serial data type to pdx_events for merge
ALTER TABLE pdx_events
ADD COLUMN serial_number SERIAL;

-- Add a new column called date_id to pdx_events
ALTER TABLE pdx_events
ADD COLUMN date_id INT;

-- Update the date_id column in pdx_events based on matching dates from the date table
UPDATE pdx_events
SET date_id = project.date.id
FROM project.date
WHERE pdx_events.date::date = project.date.date;


-- Insert data from pdx_events into project.events
INSERT INTO project.events (id, title, location, time, date_id)
SELECT
    pdx_events.serial_number AS id,
    pdx_events.title,
    pdx_events.location,
    pdx_events.time,
    pdx_events.date_id
FROM pdx_events;
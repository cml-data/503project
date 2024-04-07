CREATE TABLE current_conditions (
    date timestamp WITH time zone DEFAULT NOW(),
	last_updated text NULL,
	temp_f float8 NULL,
	is_day int8 NULL,
	wind_mph float8 NULL,
	wind_degree int8 NULL,
	wind_dir text NULL,
	pressure_mb float8 NULL,
	pressure_in float8 NULL,
	precip_in float8 NULL,
	humidity int8 NULL,
	cloud int8 NULL,
	feelslike_f float8 NULL,
	vis_miles float8 NULL,
	uv float8 NULL,
	gust_mph float8 NULL,
	co float8 NULL,
	no2 float8 NULL,
	o3 float8 NULL,
	so2 float8 NULL,
	pm2_5 float8 NULL,
	pm10 float8 NULL,
	us_epa_index int8 NULL,
	gb_defra_index int8 NULL,
	"text" text NULL,
	icon text NULL
);


CREATE TABLE public.astronomy (
	date_pulled timestamp WITH time zone DEFAULT NOW(),
	date date,
	sunrise text NULL,
	sunset text NULL,
	moonrise text NULL,
	moonset text NULL,
	moon_phase text NULL,
	moon_illumination int8 NULL,
	is_moon_up int8 NULL,
	is_sun_up int8 NULL
);

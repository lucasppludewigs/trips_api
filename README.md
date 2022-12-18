# Trips API

The problem statement of this challenge can be found in the pdf file.

## Usage

Initialize the database:  
```
docker pull postgres
docker run -p 5432:5432 --name trip-postgres -e POSTGRES_PASSWORD=postgres -d postgres
docker exec -it trip-postgres psql -U postgres

# create table and its index to group trips with similar information:

create table trips (
 region varchar(100),
 origin_coord varchar(200),
 destination_coord varchar(200),
 datetime timestamp,
 datasource varchar(100)
);

create index trip_idx on trips (origin_coord, destination_coord, cast(datetime as time));
```

To be able to install psycopg2, we need postgres: `brew install postgresql`

Install the dependencies on requirements.txt: `pip install requirements.txt`

Run the flask python API:

`export FLASK_APP=app.py`  
`flask run`

Send a command to ingest data

```bash
curl -XPOST http://localhost:5000/trips -d "trip_file=trips.csv"
```

Send a command to get weekly data based on region or coordinates:

```bash
curl -XGET http://localhost:5000/trips -H "Content-Type: application/json" -d '{"region":"Hamburg"}'  

curl -XGET http://localhost:5000/trips -H "Content-Type: application/json" -d '{"coordinates":{"lat_low": 14.33, "lat_high": 14.59, "long_low": 50.04, "long_high": 50.11}}'
```

Answers to the query questions can be found at respective folder.

Regarding scalability, the API took 90 seconds to ingest 100K rows of data.

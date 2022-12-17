# Trips API

The problem statement of this challenge can be found in the pdf file.

## Usage

Initialize the database:  
```
docker pull postgres
docker run -p 5432:5432 --name trip-postgres -e POSTGRES_PASSWORD=postgres -d postgres
docker exec -it trip-postgres psql -U postgres
create table trips (
 region varchar(100),
 origin_coord varchar(200),
 destination_coord varchar(200),
 datetime timestamp,
 datasource varchar(100)
);
```

To be able to install psycopg2, we need postgres: `brew install postgresql`

Install the dependencies on requirements.txt: `pip install requirements.txt`

Run the flask python API:

`export FLASK_APP=app.py`  
`flask run`

Send a command to ingest data

```bash
curl -XPOST http://localhost:5000/ingest -d "trip_file=trips.csv"
```

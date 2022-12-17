# Trips API

## Usage

Run the flask python API:

`export FLASK_APP=app.py`  
`flask run`

Send a command to ingest data

```bash
curl -XPOST http://localhost:5000/ingest -d "trip_file=trips.csv"
```
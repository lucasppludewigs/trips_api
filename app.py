from flask import Flask, request
import pandas as pd

app = Flask(__name__)

# TODO: consider migrating to Fast API which is more robust

@app.route('/')
def hello_world():
    print('Hello')
    return 'Hello world!'

@app.route('/ingest', methods=['POST'])
def ingest_trip():
    # Considering that the data will be received as CSV
    trip_file = request.form['trip_file']
    # vaex + HDF5 might be better than pandas
    df = pd.read_csv(trip_file)
    for index, row in df.iterrows():
        print(index,row)
    return f'index: {index}, row {row}',201

print("I'm working")

# # Data Model

# region varchar(100)
# origin_coord varchar(200)
# destination_coord varchar(200)
# datetime datetime
# datasource varchar(100)

# partition keys: similar origin, destin, time of day
# https://stackoverflow.com/questions/37689554/postgres-partition-by-character-prefix

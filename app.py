from flask import Flask, request
import pandas as pd
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(user="postgres", password="postgres", host="localhost")

@app.route('/')
def hello_world():
    print('Hello!')
    return "I'm working!"

@app.route('/ingest', methods=['POST'])
def ingest_trip():
    # Considering that the data will be received as CSV
    trip_file = request.form['trip_file']
    # vaex + HDF5 might be better than pandas
    df = pd.read_csv(trip_file)
    cursor = conn.cursor()
    for index, row in df.iterrows():
        print(f"index: {index}, row: {row}")
        print(f"this is row datasource: {row['datasource']}")
        cursor.execute(f"INSERT INTO TRIPS VALUES ('{row['region']}','{row['origin_coord']}','{row['destination_coord']}','{row['datetime']}','{row['datasource']}');")
    conn.commit()
    cursor.close()
    return f'index: {index}, row {row}',201

# TODO: consider migrating to Fast API which is more robust
# TODO: check database persistency
# TODO: data model
# TODO: use alembic for database version and schema evolution
# TODO: encapsulate functions
# TODO: test these functins
# TODO: black formatter

# partition keys: similar origin, destin, time of day
# https://stackoverflow.com/questions/37689554/postgres-partition-by-character-prefix

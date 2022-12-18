from flask import Flask, request, jsonify
from utils import *

app = Flask(__name__)

conn = create_connection()


@app.route('/')
def hello_world():
    print('Hello!')
    return "I'm working!"


@app.route('/trips', methods=['POST'])
def ingest_trip():
    # Considering that the data will be received as CSV
    trip_file = request.form['trip_file']
    ingest_trip_logic(trip_file, conn)
    return f'Data succesfully ingested',201


@app.route('/trips', methods=['GET'])
def get_week_trips_area():
    response_dict = {}
    data = request.get_json()
    cursor = conn.cursor()
    print(f"Data received: {data}")

    if 'region' in data.keys():
        result = handle_region_trips(cursor, data)
    
    elif 'coordinates' in data.keys():
        result = handle_coordinates_trips(cursor, data)
    
    else:
        return jsonify({'error':'Specify either region or coordinates in the dict, see example in README'}), 400
    conn.commit()
    cursor.close()
    response_dict['result'] = result
    return response_dict, 200

# TODO: handle errors: invalid csv path, invalid schema
# TODO: sqlalchemy instead psycopg2?
# TODO: check database persistency
# TODO: data model pydantic
# TODO: use alembic for database version and schema evolution
# TODO: test encapsulated functins
# TODO: consider migrating to Fast API which is more robust
# TODO: convert prints to proper logging
# TODO: containerize API

# TODO: partition keys: similar origin, destin, time of day
# https://stackoverflow.com/questions/37689554/postgres-partition-by-character-prefix
# maybe just using an index is easier

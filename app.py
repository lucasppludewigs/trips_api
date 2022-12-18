from flask import Flask, request, jsonify
import pandas as pd
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(user="postgres", password="postgres", host="localhost")

@app.route('/')
def hello_world():
    print('Hello!')
    return "I'm working!"

@app.route('/trips', methods=['POST'])
def ingest_trip():
    # Considering that the data will be received as CSV
    trip_file = request.form['trip_file']
    # vaex + HDF5 might be better than pandas
    df = pd.read_csv(trip_file)
    cursor = conn.cursor()
    for index, row in df.iterrows():
        cursor.execute(f"""\
        INSERT INTO TRIPS VALUES 
        ('{row['region']}','{row['origin_coord']}','{row['destination_coord']}','{row['datetime']}','{row['datasource']}');
        """)
    conn.commit()
    cursor.close()
    return f'Data succesfully ingested',201

@app.route('/trips', methods=['GET'])
def get_wk_trips_area():
    response_dict = {}
    data = request.get_json()
    print(f"Data received: {data}")
    if 'region' in data.keys():
        cursor = conn.cursor()
        cursor.execute(f"""\
            SELECT region,round(AVG(trip_count),2) AS avg_trips_per_week
            FROM (
                SELECT region, COUNT(*) AS trip_count, date_trunc('week', datetime) AS week
                FROM trips
                GROUP BY region, week
            ) AS trip_counts_by_week
            WHERE region = '{data['region']}'
            GROUP BY region;
            ;""")
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
    elif 'coordinates' in data.keys():
        print(f"coordinates received: {data['coordinates']}")
        coord = data['coordinates']
        cursor = conn.cursor()
        cursor.execute(f"""\
            SELECT round(AVG(trip_count),2) AS avg_trips_per_week
            FROM (
                SELECT count(*) AS trip_count, date_trunc('week', datetime) AS week
                FROM trips
                WHERE substr(split_part(origin_coord,' ', 2), 2) between '{coord['lat_low']}' and '{coord['lat_high']}'
                and substr(split_part(origin_coord,' ', 3), 1, length(split_part(origin_coord,' ', 3))-1)  between '{coord['long_low']}' and '{coord['long_high']}' 
                GROUP BY week
            ) AS trip_counts_by_week;
            ;"""
            )
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
    else:
        return jsonify({'error':'Specify either region or coordinates in the dict, see example in README'}), 400
    response_dict['result'] = result
    return response_dict, 200

# TODO: handle errors: invalid csv path, invalid schema
# TODO: sqlalchemy instead psycopg2?
# TODO: check database persistency
# TODO: data model pydantic
# TODO: use alembic for database version and schema evolution
# TODO: encapsulate functions
# TODO: test these functins
# TODO: consider migrating to Fast API which is more robust

# TODO: partition keys: similar origin, destin, time of day
# https://stackoverflow.com/questions/37689554/postgres-partition-by-character-prefix

import psycopg2
import pandas as pd

def create_connection():
    connection = psycopg2.connect(user="postgres", password="postgres", host="localhost")
    return connection

def ingest_trip_logic(trip_file, conn):
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

def handle_region_trips(cursor, data):
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
    return cursor.fetchone()

def handle_coordinates_trips(cursor, data):
    print(f"coordinates received: {data['coordinates']}")
    coord = data['coordinates']
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
    return cursor.fetchone()

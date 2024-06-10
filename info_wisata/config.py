import pymysql
from flask import Flask, jsonify, request
import datetime
import os
from dotenv import load_dotenv
from kafka_client import send_message

load_dotenv()

app = Flask(__name__)

API_KEY = "FINALPROJECTEAI"  # Define your API key

def convert_to_dict_with_string_timedelta(records):
    converted_records = []
    for record in records:
        converted_record = {}
        for key, value in record.items():
            if isinstance(value, datetime.timedelta):
                converted_record[key] = str(value)
            else:
                converted_record[key] = value
        converted_records.append(converted_record)
    return converted_records

# Database connection configuration
def get_db_connection():
    timeout = 10
    return pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="informasi_wisata",  # Change to your database name
        host="mysql-389773d8-eai-uts.e.aivencloud.com",
        password="AVNS_9oUuhZxFkw8IAvYvBUx",
        read_timeout=timeout,
        port=28925,
        user="avnadmin",
        write_timeout=timeout,
    )

# Middleware for API key authentication
@app.before_request
def authenticate():
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key != API_KEY:
        return jsonify({'message': 'Forbidden: Invalid or missing API key'}), 403

@app.route('/infowisata', methods=['GET'])
def get_info_wisata():
    connection = get_db_connection()
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tempat_wisata")
        records = cursor.fetchall()
    finally:
        connection.close()

    if records: 
        converted_records = convert_to_dict_with_string_timedelta(records)
        return jsonify(converted_records)
    else:
        return jsonify([])

@app.route('/infowisata', methods=['POST'])
def create_info_wisata():
    data = request.get_json()
    connection = get_db_connection()
    
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO tempat_wisata (nama, alamat, jam, harga, `desc`, gambar_url)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (data['nama'], data['alamat'], data['jam'], data['harga'], data['desc'], data['gambar_url'])
        )
        connection.commit()
        new_id = cursor.lastrowid
        # Send a message to Kafka
        send_message('infowisata-topic', {'type': 'CREATE', 'data': data, 'id_wisata': new_id})
    finally:
        connection.close()
    
    return jsonify({'id_wisata': new_id}), 201

@app.route('/infowisata/<int:id_wisata>', methods=['DELETE'])
def delete_info_wisata(id_wisata):
    connection = get_db_connection()
    
    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM tempat_wisata WHERE id_wisata = %s", (id_wisata,)
        )
        connection.commit()
        rows_affected = cursor.rowcount
        if rows_affected:
            # Send a message to Kafka
            send_message('infowisata-topic', {'type': 'DELETE', 'id_wisata': id_wisata})
    finally:
        connection.close()
    
    if rows_affected:
        return jsonify({'message': 'Deleted successfully', 'id_wisata': id_wisata}), 200
    else:
        return jsonify({'message': 'ID not found'}), 404

@app.route('/infowisata/<int:id_wisata>', methods=['PUT'])
def update_info_wisata(id_wisata):
    data = request.get_json()
    connection = get_db_connection()
    
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE tempat_wisata
            SET nama = %s, alamat = %s, jam = %s, harga = %s, `desc` = %s, gambar_url = %s
            WHERE id_wisata = %s
            """,
            (data['nama'], data['alamat'], data['jam'], data['harga'], data['desc'], data['gambar_url'], id_wisata)
        )
        connection.commit()
        rows_affected = cursor.rowcount
        if rows_affected:
            # Send a message to Kafka
            send_message('infowisata-topic', {'type': 'UPDATE', 'data': data, 'id_wisata': id_wisata})
    finally:
        connection.close()
    
    if rows_affected:
        return jsonify({'message': 'Updated successfully', 'id_wisata': id_wisata}), 200
    else:
        return jsonify({'message': 'ID not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5432)

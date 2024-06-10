import pymysql
from flask import Flask, jsonify, request, render_template
import datetime
import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse
import psycopg2

load_dotenv()

app = Flask(__name__)

API_KEY = "FINALPROJECTEAI"  # Define your API key

@app.route("/")
def main():
    headers = {"x-api-key": API_KEY}
    try:
        # Fetch data from different endpoints
        train_data = requests.get("http://localhost:3000/train", headers=headers).json()
        flight_data = requests.get("http://localhost:3000/flight", headers=headers).json()
        hotel_data = requests.get("http://localhost:3000/hotel", headers=headers).json()
        attractions_data = requests.get("http://localhost:3000/attractions", headers=headers).json()
        wisata_data = requests.get("http://localhost:5432/infowisata", headers=headers).json()

        # Render the index.html template with the fetched data
        return render_template(
            "index.html",
            train=train_data,
            flight=flight_data,
            hotel=hotel_data,
            attractions=attractions_data,
            wisata=wisata_data,
        )
    except Exception as e:
        return str(e), 500

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

# MySQL database connection configuration
def get_mysql_connection():
    timeout = 10
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="informasi_wisata",
        host="mysql-389773d8-eai-uts.e.aivencloud.com",
        password=os.getenv("MYSQL_PASSWORD"),
        read_timeout=timeout,
        port=28925,
        user="avnadmin",
        write_timeout=timeout,
    )
    return connection

# PostgreSQL database connection configuration
def get_postgres_connection():
    # Database URL
    db_url = "postgres://ticker_order_user:DX6mgTvJCqqtSfrqFz7tHBNls1RgHMwy@dpg-con0p7q1hbls73fak2r0-a.singapore-postgres.render.com/ticker_order"
    
    # Parse the database URL
    parsed_url = urlparse(db_url)
    
    # Establish a connection
    connection = psycopg2.connect(
        user=parsed_url.username,
        password=parsed_url.password,
        host=parsed_url.hostname,
        port=parsed_url.port,
        database=parsed_url.path[1:]
    )
    
    return connection

@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')

# Get flight ticket data from PostgreSQL
@app.route("/flight", methods=["GET"])
def get_flight_tickets():
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.get("http://localhost:3000/flight", headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/flight", methods=["POST"])
def create_flight_ticket():
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.post("http://localhost:3000/flight", json=request.json, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/flight/<int:id>", methods=["PUT"])
def update_flight_ticket(id):
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.put(f"http://localhost:3000/flight/{id}", json=request.json, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/flight/<int:id>", methods=["DELETE"])
def delete_flight_ticket(id):
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.delete(f"http://localhost:3000/flight/{id}", headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get train ticket data from PostgreSQL
@app.route("/train", methods=["GET"])
def get_train_tickets():
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.get("http://localhost:3000/train", headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/train", methods=["POST"])
def create_train_ticket():
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.post("http://localhost:3000/train", json=request.json, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/train/<int:id>", methods=["PUT"])
def update_train_ticket(id):
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.put(f"http://localhost:3000/train/{id}", json=request.json, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/train/<int:id>", methods=["DELETE"])
def delete_train_ticket(id):
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.delete(f"http://localhost:3000/train/{id}", headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get hotel data from PostgreSQL
@app.route("/hotel", methods=["GET"])
def get_hotels():
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.get("http://localhost:3000/hotel", headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/hotel", methods=["POST"])
def create_hotel():
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.post("http://localhost:3000/hotel", json=request.json, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/hotel/<int:id>", methods=["PUT"])
def update_hotel(id):
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.put(f"http://localhost:3000/hotel/{id}", json=request.json, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/hotel/<int:id>", methods=["DELETE"])
def delete_hotel(id):
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.delete(f"http://localhost:3000/hotel/{id}", headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get attractions data from PostgreSQL
@app.route("/attractions", methods=["GET"])
def get_attractions():
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.get("http://localhost:3000/attractions", headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/attractions", methods=["POST"])
def create_attraction():
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.post("http://localhost:3000/attractions", json=request.json, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/attractions/<int:id>", methods=["PUT"])
def update_attraction(id):
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.put(f"http://localhost:3000/attractions/{id}", json=request.json, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/attractions/<int:id>", methods=["DELETE"])
def delete_attraction(id):
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.delete(f"http://localhost:3000/attractions/{id}", headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to create an order
@app.route("/order", methods=["POST"])
def create_order():
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.post("http://localhost:3000/order", json=request.json, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/order/<int:id>", methods=["PUT"])
def update_order(id):
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.put(f"http://localhost:3000/order/{id}", json=request.json, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/order/<int:id>", methods=["DELETE"])
def delete_order(id):
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.delete(f"http://localhost:3000/order/{id}", headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get data from MySQL
@app.route("/infowisata", methods=["GET"])
def get_info_wisata():
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.get("http://localhost:5432/infowisata", headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/infowisata", methods=["POST"])
def create_info_wisata():
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.post("http://localhost:5432/infowisata", json=request.json, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/infowisata/<int:id_wisata>", methods=["PUT"])
def update_info_wisata(id_wisata):
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.put(f"http://localhost:5432/infowisata/{id_wisata}", json=request.json, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/infowisata/<int:id_wisata>", methods=["DELETE"])
def delete_info_wisata(id_wisata):
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.delete(f"http://localhost:5432/infowisata/{id_wisata}", headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

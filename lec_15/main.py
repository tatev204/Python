from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "cars.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Car Management API!"})

@app.route("/cars", methods=["GET"])
def get_cars():
    data = load_data()
    return jsonify(data), 200

@app.route("/cars", methods=["POST"])
def add_car():
    data = load_data()
    new_car = request.json

    if "id" not in new_car:
        new_car["id"] = max((car["id"] for car in data), default=0) + 1

    if any(car["id"] == new_car["id"] for car in data):
        return jsonify({"error": "Car with this ID already exists!"}), 400

    data.append(new_car)
    save_data(data)
    return jsonify(new_car), 201

@app.route("/cars/<int:car_id>", methods=["GET"])
def get_car(car_id):
    data = load_data()
    car = next((car for car in data if car["id"] == car_id), None)
    if not car:
        return jsonify({"error": f"Car with ID {car_id} not found"}), 404
    return jsonify(car), 200

@app.route("/cars/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    data = load_data()
    car = next((car for car in data if car["id"] == car_id), None)
    if not car:
        return jsonify({"error": f"Car with ID {car_id} not found"}), 404

    updated_data = request.json
    car.update(updated_data)
    save_data(data)
    return jsonify(car), 200

@app.route("/cars/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    data = load_data()
    car = next((car for car in data if car["id"] == car_id), None)
    if not car:
        return jsonify({"error": f"Car with ID {car_id} not found"}), 404

    data.remove(car)
    save_data(data)
    return jsonify({"message": f"Car with ID {car_id} deleted successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)

import requests
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

def get_access_token():
    url = "https://api.baubuddy.de/index.php/login"
    payload = {
        "username": "365",
        "password": "1"
    }
    headers = {
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["oauth"]["access_token"]
    else:
        raise Exception("TokenError:", response.text)

def resolve_label_info(label_ids, token):
    if not label_ids:
        return []

    if isinstance(label_ids, str):
        label_ids = [label_ids]
    elif isinstance(label_ids, int):
        label_ids = [str(label_ids)]
    elif isinstance(label_ids, list):
        label_ids = [str(i) for i in label_ids if i is not None]
    else:
        label_ids = []

    labels_info = []
    headers = {"Authorization": f"Bearer {token}"}
    for label_id in label_ids:
        try:
            url = f"https://api.baubuddy.de/dev/index.php/v1/labels/{label_id}"
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                data = res.json()
                label_name = data.get("label")
                color = data.get("colorCode")
                if label_name:
                    labels_info.append({
                        "label": label_name,
                        "color": color
                    })
        except:
            continue
    return labels_info

@app.route("/upload-csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "csv file not be sent"}), 400
    file = request.files["file"]

    try:
        csv_df = pd.read_csv(file)
        csv_df["rnr"] = csv_df["rnr"].astype(str).str.strip()
    except Exception as e:
        return jsonify({"error": "Invalid CSV format"}), 400

    try:
        token = get_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        vehicles_response = requests.get(
            "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active",
            headers=headers
        )
        vehicles = vehicles_response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    vehicles = [v for v in vehicles if v.get("hu")]

    valid_vehicles = []
    for vehicle in vehicles:
        vehicle_rnr = str(vehicle.get("rnr", "")).strip()

        if vehicle_rnr in csv_df["rnr"].values:
            label_ids = vehicle.get("labelIds", [])
            resolved = resolve_label_info(label_ids, token)
            vehicle["resolved_labels"] = resolved
            valid_vehicles.append(vehicle)

    if not valid_vehicles:
        return jsonify({"message": "No matching vehicles found."}), 200

    return jsonify(valid_vehicles), 200

if __name__ == "__main__":
    app.run(debug=True)

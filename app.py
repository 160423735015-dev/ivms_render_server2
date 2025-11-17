from flask import Flask, request, jsonify
import datetime, csv, os

app = Flask(__name__)

CSV_FILE = "ivms_data.csv"
API_KEY = "MY_SECRET_KEY_123"

# Create CSV if missing
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp","latitude","longitude","speed_kmph","accel_magnitude"])


@app.route("/")
def home():
    return "IVMS Flask server is running on Render!"


@app.route("/api/data", methods=["POST"])
def data():
    key = request.headers.get("X-API-KEY")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    lat = data.get("latitude")
    lon = data.get("longitude")
    speed = data.get("speed")
    accel = data.get("accel")

    timestamp = datetime.datetime.utcnow().isoformat()

    with open(CSV_FILE, "a", newline="") as f:
        csv.writer(f).writerow([timestamp, lat, lon, speed, accel])

    print(f"[{timestamp}] LAT={lat} LON={lon} SPEED={speed} ACCEL={accel}")

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # Render will override port env variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

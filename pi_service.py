from flask import Flask, request, jsonify
import os

app = Flask(__name__)

PI_FILE_PATH = os.getenv("PI_FILE", "shard_0.txt")  # Set dynamically in Docker

def load_pi_data():
    """
    Reads the assigned shard file into memory (list of tuples).
    Each line is stored as (x, pi_x).
    """
    global pi_data
    with open(PI_FILE_PATH, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            x_value = float(parts[0])
            pi_x_value = int(parts[1])
            pi_data.append((x_value, pi_x_value))

def find_pi_value(x):
    """
    Performs a sequential search on the loaded pi_data array.
    Returns pi(x) for the closest match.
    """
    for x_value, pi_x_value in pi_data:
        if x_value >= x:
            return pi_x_value
    return None  # If x is out of range

@app.route('/pi', methods=['GET'])
def get_pi():
    try:
        x = float(request.args.get("x"))
        pi_x = find_pi_value(x)

        if pi_x is not None:
            return jsonify({"x": x, "pi(x)": pi_x})
        else:
            return jsonify({"error": "Value out of range"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    load_pi_data()  # Load the shard's data into memory at startup
    app.run(host="0.0.0.0", port=5000)
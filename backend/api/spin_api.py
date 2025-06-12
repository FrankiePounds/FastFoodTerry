import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game_math.spin_logic import generate_spin_data
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/spin", methods=["GET"])
def spin():
    result = generate_spin_data()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

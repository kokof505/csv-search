from flask import Flask, request, jsonify, send_from_directory
import pandas as pd

app = Flask(__name__)

# Load CSV and treat 'id' as string for consistent search
df = pd.read_csv("employees.csv", dtype={"id": str})
df['name'] = df['name'].astype(str)  # Ensure name is string too

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify([])

    # Match ID exactly or Name partially (case-insensitive)
    results = df[
        (df["id"].str.lower() == query) |
        (df["name"].str.lower().str.contains(query))
    ]

    return jsonify(results.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

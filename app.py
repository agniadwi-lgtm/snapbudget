import os
from flask import Flask, jsonify, render_template, request, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=BASE_DIR,
)

# Penyimpanan sementara titik survei lapangan selama sesi berjalan
SURVEY_POINTS = []


@app.route("/")
def home():
    # Jika index.html ada di folder templates/, render lewat templates
    if os.path.exists(os.path.join(BASE_DIR, "templates", "index.html")):
        return render_template("index.html")
    # Fallback jika index.html diletakkan langsung di folder utama proyek
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "app": "GeoMap ID (SnapGeo)"})


@app.route("/api/surveys", methods=["GET", "POST"])
def manage_surveys():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        if "lat" not in data or "lng" not in data:
            return jsonify({"error": "Koordinat lat dan lng wajib diisi"}), 400

        point = {
            "id": len(SURVEY_POINTS) + 1,
            "nama_titik": data.get("nama_titik", f"Titik #{len(SURVEY_POINTS) + 1}"),
            "litologi": data.get("litologi", "Belum ditentukan"),
            "catatan": data.get("catatan", ""),
            "lat": float(data["lat"]),
            "lng": float(data["lng"]),
        }
        SURVEY_POINTS.append(point)
        return jsonify({"message": "Titik survei tersimpan", "data": point}), 201

    return jsonify({"total": len(SURVEY_POINTS), "data": SURVEY_POINTS})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
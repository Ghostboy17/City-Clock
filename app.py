

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pytz 
import sqlite3

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

countries = {
    "EE.UU.": {
        "Nueva York": "America/New_York",
        "Los Ángeles": "America/Los_Angeles",
        "Chicago": "America/Chicago"
    },
    "Reino Unido": {
        "Londres": "Europe/London",
        "Manchester": "Europe/London",
        "Liverpool": "Europe/London"
    },
    "Japón": {
        "Tokio": "Asia/Tokyo",
        "Osaka": "Asia/Tokyo",
        "Nagoya": "Asia/Tokyo"
    },
    "Francia": {
        "París": "Europe/Paris",
        "Marsella": "Europe/Paris",
        "Lyon": "Europe/Paris"
    },
    "Rusia": {
        "Moscú": "Europe/Moscow",
        "San Petersburgo": "Europe/Moscow"
    },
    "Ecuador": {
        "Quito": "America/Guayaquil",
        "Guayaquil": "America/Guayaquil",
    }
}
@app.route('/countries')
def get_countries():
    return jsonify(countries)

@app.route('/time')
def get_time():
    country = request.args.get('country', 'EE.UU.')  # País por defecto
    city = request.args.get('city', 'Nueva York')  # Ciudad por defecto

    timezone = countries.get(country, {}).get(city, "UTC")  # Busca la zona horaria
    now = datetime.now(pytz.timezone(timezone))
    time_str = now.strftime("%H:%M:%S")

    return jsonify({"country": country, "city": city, "time": time_str})


def init_db():
    with sqlite3.connect("settings.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                          id INTEGER PRIMARY KEY,
                          city TEXT,
                          color TEXT)''')
        cursor.execute("INSERT OR IGNORE INTO settings (id, city, color) VALUES (1, 'UTC', 'red')")
        conn.commit()

init_db()

@app.route('/')
def index():
    with sqlite3.connect("settings.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT city, color FROM settings WHERE id=1")
        city, color = cursor.fetchone()
    return render_template('index.html', city=city, color=color)

# Diccionario de ciudades con sus respectivas zonas horarias
timezones = {
    "Nueva York": "America/New_York",
    "Londres": "Europe/London",
    "Tokio": "Asia/Tokyo",
    "París": "Europe/Paris",
    "Rusia": "Europe/Moscow",
    "Ecuador": "America/Guayaquil",
    "Rusia": "Europe/Moscow",
}


@app.route('/update', methods=['POST'])
def update_settings():
    data = request.json
    city = data.get("city", "UTC")
    color = data.get("color", "red")
    with sqlite3.connect("settings.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE settings SET city=?, color=? WHERE id=1", (city, color))
        conn.commit()
    return jsonify({"message": "Settings updated", "city": city, "color": color})

#if __name__ == '__main__':
    #app.run(debug=True)



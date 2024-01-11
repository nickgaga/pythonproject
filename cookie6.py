from flask import Flask, request, render_template
import mysql.connector
from datetime import datetime
from geopy.geocoders import Nominatim

app = Flask(__name__)

def get_location_info(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True)
    if location:
        return location.address
    else:
        return "Informazioni sulla posizione non trovate."

def save_data_to_database(username, last_access, location):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Test1234',
            database='talentform'
        )

        cursor = connection.cursor()

        query = "INSERT INTO users (username, last_access, location) VALUES (%s, %s, %s)"
        values = (username, last_access, location)

        cursor.execute(query, values)
        connection.commit()
        print("Dati salvati correttamente nel database.")
    except mysql.connector.Error as error:
        print("Errore durante il salvataggio dei dati:", error)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        last_access = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        latitude = 41.4628487
        longitude = 15.5257368
        location = get_location_info(latitude, longitude)

        save_data_to_database(username, last_access, location)

        return f'Dati salvati con successo per lo username: {username}'
    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)

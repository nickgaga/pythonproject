from flask import Flask, request, render_template, make_response
import mysql.connector
from datetime import datetime

app = Flask(__name__)


def save_data_to_database(username, last_access):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Test1234',
            database='talentform'
        )

        cursor = connection.cursor()

        query = "INSERT INTO users (username, last_access) VALUES (%s, %s)"
        values = (username, last_access)

        cursor.execute(query, values)
        connection.commit()
        print("Dati salvati correttamente nel database.")
    except mysql.connector.Error as error:
        print("Errore durante il salvataggio dei dati:", error)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/salvaCookie', methods=['POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        last_access = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("ciao")
        save_data_to_database(username, last_access)
        return f'Dati salvati con successo per lo username: {username}'


    else:
        return render_template('home.html')
@app.route('/')
def index():
    # Leggi il cookie esistente, se presente
    username = request.cookies.get('username')
    last_access_time = request.cookies.get('last_access_time')

    if username:
        message = f'Ciao {username}! Il tuo cookie è già impostato.'
        if last_access_time:
            last_access_time = datetime.fromisoformat(last_access_time)
            message += f' Ultimo accesso: {last_access_time.strftime("%Y-%m-%d %H:%M:%S")}'
    else:
        message = 'Benvenuto! Per favore, inserisci il tuo nome per impostare il cookie.'

    return render_template("home.html", message = message)

@app.route('/set-cookie', methods=['POST'])
def set_cookie():
    # Ottieni il nome utente dal form
    username = request.form['username']

    # Crea una risposta e imposta i cookie
    response = make_response('Cookie impostati con successo!')
    response.set_cookie('username', username)
    response.set_cookie('last_access_time', datetime.now().isoformat())

    return response


if __name__ == "__main__":
    app.run(debug=True)
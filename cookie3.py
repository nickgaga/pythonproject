from flask import Flask, request, make_response
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # Leggi il cookie esistente, se presente
    username = request.cookies.get('username')
    last_access_time = request.cookies.get('last_access_time')
    location = request.cookies.get('location')

    if username:
        message = f'Ciao {username}! Il tuo cookie è già impostato.'
        if last_access_time:
            last_access_time = datetime.fromisoformat(last_access_time)
            message += f' Ultimo accesso: {last_access_time.strftime("%Y-%m-%d %H:%M:%S")}'
        if location:
            location = location.replace('%20', ' ')  # Decodifica gli spazi
            message += f' Posizione: {location}'
    else:
        message = 'Benvenuto! Per favore, inserisci il tuo nome per impostare il cookie.'

    return f'''
        <h1>{message}</h1>
        <form method="post" action="/set-cookie">
            <label for="username">Nome utente:</label>
            <input type="text" id="username" name="username" required>
            <button type="submit">Imposta il cookie</button>
        </form>
        <script>
            function getLocation(position) {{
                var latitude = position.coords.latitude;
                var longitude = position.coords.longitude;
                var location = 'Lat: ' + latitude + ', Long: ' + longitude;
                document.cookie = 'location=' + encodeURIComponent(location) + '; expires=Thu, 31 Dec 2099 23:59:59 UTC; path=/';
                window.location.reload(); // Ricarica la pagina per mostrare il messaggio aggiornato
            }}

            function showError(error) {{
                console.log('Error occurred while getting geolocation:', error);
            }}

            function requestLocation() {{
                if (navigator.geolocation) {{
                    navigator.geolocation.getCurrentPosition(getLocation, showError);
                }} else {{
                    console.log("Geolocation is not supported by this browser.");
                }}
            }}

            requestLocation();
        </script>
    '''

@app.route('/set-cookie', methods=['POST'])
def set_cookie():
    # Ottieni il nome utente dal form
    username = request.form['username']

    # Crea una risposta e imposta i cookie
    response = make_response('Cookie impostati con successo!')
    response.set_cookie('username', username)
    response.set_cookie('last_access_time', datetime.now().isoformat())

    return response

if __name__ == '__main__':
    app.run(debug=True)


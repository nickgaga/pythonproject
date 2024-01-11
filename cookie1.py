from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    # Leggi il cookie esistente, se presente
    username = request.cookies.get('username')

    if username:
        message = f'Ciao {username}! Il tuo cookie è già impostato.'
    else:
        message = 'Benvenuto! Per favore, inserisci il tuo nome per impostare il cookie.'

    return f'''
        <h1>{message}</h1>
        <form method="post" action="/set-cookie">
            <label for="username">Nome utente:</label>
            <input type="text" id="username" name="username" required>
            <button type="submit">Imposta il cookie</button>
        </form>
    '''

@app.route('/set-cookie', methods=['POST'])
def set_cookie():
    # Ottieni il nome utente dal form
    username = request.form['username']

    # Crea una risposta e imposta il cookie
    response = make_response('Cookie impostato con successo!')
    response.set_cookie('username', username)

    return response

if __name__ == '__main__':
    app.run(debug=True)

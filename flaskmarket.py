from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = "supermarket_secret_key"  # Chiave segreta per cifrare i cookie di sessione

# Configura la connessione al database MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Test1234",
    database="talentform"
)

# Crea la tabella per gli utenti se non esiste già
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, user_email VARCHAR(255) UNIQUE, password VARCHAR(255))")
db.commit()

# Dizionario con i prezzi dei prodotti
product_prices = {
    "Tonno in scatola": 2.50,
    "Pasta": 2.00,
    "Latte": 1.20,
    "Carne": 8.00,
    "Pesce": 12.50,
    "Verdura": 2.50,
    "Yogurt": 1.80,
    "Formaggio": 3.50,
    "Televisore": 500.00,
    "Lavatrice": 400.00
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_email = request.form.get("user_email")
        password = request.form.get("password")

        # Controlla se l'utente esiste
        cursor.execute("SELECT * FROM users WHERE user_email = %s", (user_email,))
        user = cursor.fetchone()

        if user:
            # Verifica la password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user[2] == hashed_password:
                session["user_email"] = user_email
                return redirect(url_for("selections"))
            else:
                return render_template("loginUser.html", error="Credenziali non valide. Riprova.")
        else:
            return render_template("loginUser.html", error="Utente non esistente. Registrati.")

    return render_template("loginUser.html", error=None)

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        user_email = request.form.get("user_email")
        password = request.form.get("password")

        # Verifica se l'utente esiste già
        cursor.execute("SELECT * FROM users WHERE user_email = %s", (user_email,))
        user = cursor.fetchone()

        if user:
            return render_template("registration.html", error="Email già registrata. Scegline un'altra.")

        # Registra il nuovo utente
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO users (user_email, password) VALUES (%s, %s)", (user_email, hashed_password))
        db.commit()

        session["user_email"] = user_email
        return redirect(url_for("login"))

    return render_template("registration.html", error=None)

@app.route("/selections", methods=["GET", "POST"])
def selections():
    # Verifica se l'utente è autenticato
    if "user_email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        # Qui puoi gestire l'elaborazione delle selezioni dell'utente
        # ...

        return "Ordine completato! Grazie per il tuo acquisto."

    return render_template("super.html", products=product_prices)

if __name__ == "__main__":
    app.run(debug=True)

import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configura la cartella per il caricamento delle immagini
UPLOAD_FOLDER = 'static/uploads1'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Estensioni consentite per le immagini
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    file = ""
    if request.method == 'POST':
        # Controlla se è stato fornito un file
        if 'file' not in request.files:
            return "Nessun file fornito"

        file = request.files['file']
        # Controlla se il file ha un nome
        if file.filename == '':
            return "Nessun file selezionato"

        # Controlla se il file è un'immagine consentita
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload_success.html', filename = filename)

        return "File non valido. Le estensioni consentite sono: " + ", ".join(ALLOWED_EXTENSIONS)

    return render_template('upload_form.html')

if __name__ == '__main__':
    app.run(debug=True)

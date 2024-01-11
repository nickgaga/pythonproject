from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Test1234",
  database="talentform"
)
app = Flask(__name__)

# Dizionario per associare ogni piatto al suo prezzo
menu_prices = {
    "pasta": 10,
    "risotto": 12,
    "gnocchi": 11,
    "pollo": 15,
    "pesce": 18,
    "manzo": 20,
    "insalata": 5,
    "verdure": 6,
    "patate": 4,
    "tiramisu": 8,
    "pannacotta": 7,
    "torta": 9
}


@app.route('/')
def index():
    return render_template('ristorante.html')
@app.route('/gestore')
def gestore():
    return render_template('gestorelogin.html')

@app.route('/login_gestore', methods=['GET', 'POST'])
def gestore_log():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Test1234",
        database="talentform"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM risto")

    myresult = mycursor.fetchall()
    # Chiudi il cursore e la connessione al database
    mycursor.close()
    mydb.close()


    return render_template('gestoreOrdini.html', myresult = myresult)

@app.route('/stamp', methods=['POST'])
def stamp():
    primi_selezionati = request.form['primi']
    secondi_selezionati = request.form['secondi']
    contorni_selezionati = request.form['contorni']
    dolci_selezionati = request.form['dolci']
    totale = menu_prices.get(primi_selezionati, 0) + menu_prices.get(secondi_selezionati, 0) + \
             menu_prices.get(contorni_selezionati, 0) + menu_prices.get(dolci_selezionati, 0)
    sql = "INSERT INTO risto (primo, secondo, contorno,dolce, prezzo) VALUES (%s, %s, %s, %s, %s)"
    val = (primi_selezionati, secondi_selezionati, contorni_selezionati,  dolci_selezionati, totale)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)

    mydb.commit()
    # Calcola il totale del conto sommando i prezzi dei piatti selezionati


    return f"Hai selezionato i seguenti piatti:\nPrimi: {primi_selezionati} - Prezzo: {menu_prices.get(primi_selezionati)} Euro\n" \
           f"Secondi: {secondi_selezionati} - Prezzo: {menu_prices.get(secondi_selezionati)} Euro\n" \
           f"Contorni: {contorni_selezionati} - Prezzo: {menu_prices.get(contorni_selezionati)} Euro\n" \
           f"Dolci: {dolci_selezionati} - Prezzo: {menu_prices.get(dolci_selezionati)} Euro\n" \
           f"Totale: {totale} Euro"

@app.route('/rifiuta_ordine', methods=['POST'])
def rifiuta_ordine():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Test1234",
        database="talentform"
    )
    order_id = request.form['order_id']
    mycursor = mydb.cursor()
    sql = "DELETE FROM risto WHERE idristo = %s"
    val = (order_id,)

    try:
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('gestore_log'))  #
    except Exception as e:
        # In caso di errore, gestisci il rollback della transazione
        mydb.rollback()
        return "Errore durante la cancellazione dell'ordine: {}".format(str(e))

    return "Ordine {} rifutato!".format(order_id)
@app.route('/accetta_ordine', methods=['POST'])
def accetta_ordine():
        mydb = mysql.connector.connect(
         host="localhost",
         user="root",
         password="Test1234",
         database="talentform"
       )
        order_id = request.form['order_id']
        mycursor = mydb.cursor()




        # Seleziona i dati dalla tabella 'risto' per l'order_id specificato
        sql_select = "SELECT * FROM risto WHERE idristo = %s"
        val = (order_id,)
        mycursor.execute(sql_select, val)
        myresult = mycursor.fetchall()

            # Verifica se il risultato non è vuoto
        if myresult:
                # Estrai i dati dal risultato della query
            menu = myresult[0]  # Suppongo che ci sia solo un risultato per l'order_id

                # Inserisci il menu nella tabella 'storicoOrdini'
            sql_insert = "INSERT INTO storicoOrdini (primo, secondo, contorno, dolce, prezzo) VALUES (%s, %s, %s, %s, %s)"
            val_insert = (
                menu[1], menu[2], menu[3], menu[4], menu[5]
                )  # Assumendo che i dati corrispondano alle colonne specificate




        else:
            print("Nessun risultato trovato per l'order_id:", order_id)

        try:

            mycursor.execute(sql_insert, val_insert)
            mydb.commit()
            sql = "DELETE FROM risto WHERE idristo = %s"
            val = (order_id,)
            mycursor.execute(sql, val)
            mydb.commit()
            return redirect(url_for('gestore_log'))  #
        except Exception as e:
            # In caso di errore, gestisci il rollback della transazione
            mydb.rollback()
            return "Errore durante la cancellazione dell'ordine: {}".format(str(e))

        return "Ordine {} accetato!".format(order_id)

import matplotlib.pyplot as plt
import pandas as pd
from flask import render_template_string

# Funzione per visualizzare i dati

@app.route('/visualizza_dati')
def visualizza_dati():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Test1234",
        database="talentform"
    )
    mycursor = mydb.cursor()

    # Ottieni l'incasso totale
    sql_total = "SELECT SUM(prezzo) FROM storicoOrdini"
    mycursor.execute(sql_total)
    total_result = mycursor.fetchone()
    incasso_totale = total_result[0]

    # Ottieni i dati per il grafico a torta dei primi più scelti
    sql_primi = "SELECT primo, COUNT(*) AS conteggio FROM storicoOrdini GROUP BY primo ORDER BY conteggio DESC LIMIT 5"
    mycursor.execute(sql_primi)
    primi_results = mycursor.fetchall()
    primi_categorie = [result[0] for result in primi_results]
    primi_conteggi = [result[1] for result in primi_results]

    # Ottieni i dati per il grafico a torta dei secondi più scelti
    sql_secondi = "SELECT secondo, COUNT(*) AS conteggio FROM storicoOrdini GROUP BY secondo ORDER BY conteggio DESC LIMIT 5"
    mycursor.execute(sql_secondi)
    secondi_results = mycursor.fetchall()
    secondi_categorie = [result[0] for result in secondi_results]
    secondi_conteggi = [result[1] for result in secondi_results]

    # Chiudi il cursore e la connessione al database
    mycursor.close()
    mydb.close()

    # Genera il grafico a torta dei primi più scelti
    plt.figure(figsize=(8, 8))
    plt.pie(primi_conteggi, labels=primi_categorie, autopct='%1.1f%%')
    plt.title('Primi più scelti')
    plt.savefig('static/primi_piu_scelti.png')  # Salva il grafico come immagine nella cartella static
    plt.close()  # Chiudi il grafico per liberare la memoria

    # Genera il grafico a torta dei secondi più scelti
    plt.figure(figsize=(8, 8))
    plt.pie(secondi_conteggi, labels=secondi_categorie, autopct='%1.1f%%')
    plt.title('Secondi più scelti')
    plt.savefig('static/secondi_piu_scelti.png')  # Salva il grafico come immagine nella cartella static
    plt.close()  # Chiudi il grafico per liberare la memoria

    # Chiudi il cursore e la connessione al database
    mycursor.close()
    mydb.close()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Test1234",
        database="talentform"
    )
    # Ritorna l'incasso totale e i nomi dei file delle immagini dei grafici generati
    incasso_totale = ...  # Il codice per calcolare l'incasso totale va inserito qui
    primi_grafico = 'primi_piu_scelti.png'
    secondi_grafico = 'secondi_piu_scelti.png'

    mycursor = mydb.cursor()
    mycursor.execute("SELECT SUM(prezzo) FROM storicoOrdini")
    total_result = mycursor.fetchone()
    incasso_totale = total_result[0]

    # Chiudi il cursore e la connessione al database
    mycursor.close()
    mydb.close()

    # Ritorna l'incasso totale e i nomi dei file delle immagini dei grafici generati
    primi_grafico = 'primi_piu_scelti.png'
    secondi_grafico = 'secondi_piu_scelti.png'

    return render_template('visualizzaStatistiche.html', incasso_totale=incasso_totale, primi_grafico=primi_grafico,
                           secondi_grafico=secondi_grafico)

# Route per visualizzare i dati





# Il resto del tuo codice rimane invariato...



if __name__ == '__main__':
    app.run()

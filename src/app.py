from flask import Flask, render_template, request, jsonify

from src.GoogleService import GoogleService
from src.TorneoToHTML import TorneoToHTML
from src.config import SHEET_NAME, RANGE_TEAM_NAMES
from src.spreadsheet import spreadsheet_to_df, spreadsheet_cell, spreadsheet_name

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


google_service = GoogleService()


@app.route('/crea', methods=['POST'])
def crea():
    # Crea un nuovo Google Spreadsheet
    spreadsheet_id = google_service.clone_spreadsheet()

    print("Nuovo:", spreadsheet_id)
    # Rendi il file editabile da tutti
    google_service.share_spreadsheet(spreadsheet_id)

    # Reindirizza l'utente al nuovo Google Spreadsheet
    return jsonify({
        'id': spreadsheet_id,
        'url': f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
    })


@app.route('/fetchJSON', methods=['POST'])
def fetchJSON():
    spreadsheet_id = request.json['spreasheetID']
    return fetch(spreadsheet_id)


@app.route('/fetchFORM', methods=['POST'])
def fetchFORM():
    spreadsheet_id = request.form['spreasheetID']
    return fetch(spreadsheet_id)


@app.route('/torneo/<spreadsheet_id>', methods=['GET'])
def torneo(spreadsheet_id):
    return fetch(spreadsheet_id)


def fetch(spreadsheet_id):
    squadre = spreadsheet_to_df(spreadsheet_id, SHEET_NAME + RANGE_TEAM_NAMES)
    name = spreadsheet_name(spreadsheet_id)
    print("Tome Torneo:", name)
    n_gironi = int(spreadsheet_cell(spreadsheet_id, SHEET_NAME + "!K4"))
    n_campi = int(spreadsheet_cell(spreadsheet_id, SHEET_NAME + "!K3"))
    n_sq_per_girone = int(spreadsheet_cell(spreadsheet_id, SHEET_NAME + "!K5"))
    ora_inizio = int(spreadsheet_cell(spreadsheet_id, SHEET_NAME + "!K6"))
    min_inizio = int(spreadsheet_cell(spreadsheet_id, SHEET_NAME + "!K7"))
    durata_partita = int(spreadsheet_cell(spreadsheet_id, SHEET_NAME + "!K8"))

    torneo = TorneoToHTML(name, squadre, n_gironi=n_gironi, n_campi=n_campi,
                          n_sq_per_girone=n_sq_per_girone,
                          minuti=min_inizio,
                          ore=ora_inizio,
                          durata_partita=durata_partita)

    sq_per_gir = torneo.html_squadre_per_girone()
    pa_per_sq = torneo.html_partite_per_squadra()
    pa_per_cm = torneo.html_partite_per_campi()
    pa_per_tu = torneo.html_partite_per_turni()
    pa_per_gi = torneo.html_partite_per_gironi()

    return render_template("torneo.html", title=name, html=sq_per_gir + pa_per_sq + pa_per_cm + pa_per_tu + pa_per_gi)


if __name__ == '__main__':
    app.run(debug=True)

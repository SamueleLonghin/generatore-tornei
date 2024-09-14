import os

from flask import Flask, render_template, request, jsonify, send_file, make_response, redirect

from Eliminazione import Eliminazione
from TorneoToHTML import TorneoToHTML
from spreadsheet import clone_spreadsheet, share_spreadsheet, spreadsheet_to_df
from support import parse_multi_form

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/crea', methods=['POST'])
def crea():
    # Crea un nuovo Google Spreadsheet
    spreadsheet_id = clone_spreadsheet()

    print("Nuovo:", spreadsheet_id)
    # Rendi il file editabile da tutti
    share_spreadsheet(spreadsheet_id)

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
    return redirect(f"/torneo/{spreadsheet_id}")


@app.route('/torneo/<spreadsheet_id>', methods=['GET'])
def torneo(spreadsheet_id):
    return fetch(spreadsheet_id)


@app.route('/custom/<spreadsheet_id>', methods=['GET'])
def custom(spreadsheet_id):
    params, config = TorneoToHTML.presetsFromSpreadsheet(spreadsheet_id)
    title = config['nome']
    return render_template('custom.html', title=title, initial_presets=config, params=params)


@app.route('/custom', methods=['POST'])
def custom_post():
    spreadsheet_id = request.form['spreasheetID']
    return redirect(f"/custom/{spreadsheet_id}")


@app.route('/custom/<spreadsheet_id>/view', methods=['GET'])
def custom_torneo(spreadsheet_id):
    dati = parse_multi_form(request.args)
    configurations = dati['conf']
    params = dati['params']
    heads = []
    values = []
    infos = []
    print(dati)
    squadre = spreadsheet_to_df(spreadsheet_id, params['full_range_teams_names'])
    for i, conf in configurations.items():
        t = TorneoToHTML(squadre=squadre, spreadsheet_id=spreadsheet_id, **conf)
        title, info, html = t.getHTMLComponents().values()
        heads.append(title)
        infos.append(info)
        values.append(html)

    return render_template('compare.html', titles=heads, infos=infos, values=values)


@app.route('/partite')
def partite():
    print("Partite")
    return render_template('partite.html', db_url='db')


@app.route('/partite/<spreadsheet_id>')
def partiteDynamic(spreadsheet_id):
    print("Partite")
    return render_template('partite.html', db_url=f'/db/{spreadsheet_id}')


@app.route('/db')
def database():
    try:
        file_path = 'db.json'
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return make_response(f"File not found.", 404)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)


@app.route('/db/<spreadsheet_id>')
def databaseDynamic(spreadsheet_id):
    # squadre = spreadsheet_to_df(spreadsheet_id, SHEET_NAME + RANGE_TEAM_NAMES)
    # name = spreadsheet_name(spreadsheet_id)
    # n_gironi = int(spreadsheet_cell(spreadsheet_id, SHEET_NAME + "!K4", 3))
    # n_campi = int(spreadsheet_cell(spreadsheet_id, SHEET_NAME + "!K3", 2))
    # n_sq_per_girone = int(spreadsheet_cell(spreadsheet_id, SHEET_NAME + "!K5", 4))
    # ora_inizio = int(spreadsheet_cell(spreadsheet_id, SHEET_NAME + "!K6", 12))
    # min_inizio = int(spreadsheet_cell(spreadsheet_id, SHEET_NAME + "!K7", 0))
    # durata_partita = int(spreadsheet_cell(spreadsheet_id, SHEET_NAME + "!K8", 30))
    #
    # torneo = TorneoToHTML(name, squadre, n_gironi=n_gironi, n_campi=n_campi,
    #                       n_sq_per_girone=n_sq_per_girone,
    #                       minuti=min_inizio,
    #                       ore=ora_inizio,
    #                       durata_partita=durata_partita)
    e = Eliminazione(None)
    print(e.tournament_data)
    return jsonify(e.tournament_data)


def fetch(spreadsheet_id):
    torneo = TorneoToHTML.fromSpreadsheet(spreadsheet_id)
    return torneo.toHTML()


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

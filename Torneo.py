import datetime
import pickle

import pandas as pd

from Girone import Girone
from Partita import Partita
from Squadra import Squadra
from Style import *
from config import TEAMS_SHEET_NAME, RANGE_TEAM_NAMES, MATCHES_SHEET_NAME, CLASSIFICATION_SHEET_NAME
from spreadsheet import spreadsheet_to_df, spreadsheet_name, spreadsheet_cell, df_to_spreadsheet, \
    create_sheet_if_not_exists, run, mergeCells, writeCells, alignCenterCells, num_col, \
    set_columns_width, set_columns_width_auto, setBorders, setTextFormat, get_data_range


class Torneo:
    nome = None
    n_gironi = 0
    n_campi = 0
    n_turni = 0
    durata_partita = None
    dataora_inizio = None
    squadre = None
    gironi = None
    partite_ordinate = None
    partite = []
    spreadsheet_id = None
    punti_per_vittoria = 3
    punti_per_pareggio = 1

    def __init__(self, nome, squadre: pd.DataFrame, n_gironi, n_campi, n_sq_per_girone=None, padding=True,
                 ore=None, minuti=None, durata_partita=30, spreadsheet_id=None,
                 dataora_inizio=datetime.datetime(hour=14, minute=30, day=1, month=1, year=2000),
                 full_range_teams_names=None):
        self.nome = nome
        self.n_campi = int(n_campi)
        self.n_gironi = int(n_gironi)
        self.n_sq_per_girone = int(n_sq_per_girone)
        self.dataora_inizio = dataora_inizio
        self.durata_partita = int(durata_partita)
        self.spreadsheet_id = spreadsheet_id
        if ore is not None:
            self.dataora_inizio = self.dataora_inizio.replace(hour=int(ore))
        if minuti is not None:
            self.dataora_inizio = self.dataora_inizio.replace(minute=int(minuti))
        if not self.n_sq_per_girone:
            self.n_sq_per_girone = len(squadre) // self.n_gironi
        if padding:
            agg = (self.n_gironi * self.n_sq_per_girone) - len(squadre)
            for i in range(agg):
                squadre.loc[len(squadre)] = [f"Pad {i + 1}"] * squadre.columns.size
        self.squadre = Squadra.from_df(squadre)
        self.genera_gironi()
        self.partite = sorted(appiattisci([g.partite for g in self.gironi]), key=lambda x: x.__hash__())
        self.ordina_partite()

    def genera_gironi(self):
        self.gironi = [
            Girone(self, NOMI_GIRONI[i], i, self.squadre[self.n_sq_per_girone * i:self.n_sq_per_girone * (i + 1)])
            for i in range(self.n_gironi)
        ]

    @property
    def partite_campi(self):
        return [self.partite_ordinate[i::self.n_campi] for i in range(self.n_campi)]

    def ordina_partite(self):
        partite = []
        pl = list(self.partite)
        plt = pl
        usati = [0] * self.n_squadre
        while len(pl) > 0:
            if len(plt) == 0:
                # Se non sono disponibili partite evitando turni di riposo,
                # creo un turno di riposo
                p = Partita(None, None, self)
            else:
                p = plt.pop()
                # incremento usati
                usati[p.s1.id] += 1
                usati[p.s2.id] += 1
                if p in pl:
                    pl.remove(p)

            p.turno = self.n_turni
            p.campo = len(partite) % self.n_campi
            partite.append(p)
            # Ricalcolo il turno attuale
            self.n_turni = len(partite) // self.n_campi
            # sq da escludere
            i_da = ((self.n_turni - 1) * self.n_campi)
            i_da = max(i_da, 0)
            escludere = [sq for pa in partite[i_da:] for sq in pa]
            plt = get_partite_possibili(escludere, pl, usati)
        self.partite_ordinate = partite
        if len(partite) % self.n_campi != 0:
            print("Aggiungo un turno")
            self.n_turni += 1

    @property
    def n_squadre(self):
        return len(self.squadre)

    @property
    def partite_df(self):
        return [p.to_df_row() for p in self.partite_ordinate]

    @property
    def partite_list(self):
        return [tuple(p) for p in self.partite_ordinate]

    @property
    def partite_per_turno(self):
        return [self.partite_ordinate[self.n_campi * turno: self.n_campi * (turno + 1)] for turno in
                range(self.n_turni)]

    @property
    def n_partite_per_girone(self):
        return (self.n_sq_per_girone + 1) * self.n_sq_per_girone / 2

    @property
    def orario_inizio(self):
        return self.dataora_inizio.time().strftime("%H:%M").center(5)

    @property
    def orario_fine_gironi(self):
        return self.partite_ordinate[-1].ora_fine

    def squadra(self, id):
        if id is not None:
            return self.squadre[id].nome

    def set_risultato(self, turno, campo, p1, p2):
        partita = self.partite_ordinate[turno * self.n_campi + campo]
        partita.set_risultato(p1, p2)

    @classmethod
    def load(cls):
        return

    @classmethod
    def presetsFromSpreadsheet(cls, spreadsheet_id, sheet_name=TEAMS_SHEET_NAME, range_team_names=RANGE_TEAM_NAMES):
        padding = False
        full_range_teams_names = sheet_name + range_team_names
        print(full_range_teams_names)
        squadre = spreadsheet_to_df(spreadsheet_id, full_range_teams_names)
        nome = spreadsheet_name(spreadsheet_id)
        n_gironi = int(spreadsheet_cell(spreadsheet_id, TEAMS_SHEET_NAME + "!K4", 3))
        n_campi = int(spreadsheet_cell(spreadsheet_id, TEAMS_SHEET_NAME + "!K3", 2))
        n_sq_per_girone = int(spreadsheet_cell(spreadsheet_id, TEAMS_SHEET_NAME + "!K5", 4))
        ora_inizio = int(spreadsheet_cell(spreadsheet_id, TEAMS_SHEET_NAME + "!K6", 12))
        min_inizio = int(spreadsheet_cell(spreadsheet_id, TEAMS_SHEET_NAME + "!K7", 0))
        durata_partita = int(spreadsheet_cell(spreadsheet_id, TEAMS_SHEET_NAME + "!K8", 30))

        num_sq = squadre.shape[0]
        if num_sq < n_gironi * n_sq_per_girone:
            padding = True

        params = dict(
            squadre=squadre,
            spreadsheet_id=spreadsheet_id,
            full_range_teams_names=full_range_teams_names
        )
        configuration = dict(
            nome=nome,
            n_gironi=n_gironi,
            n_campi=n_campi,
            n_sq_per_girone=n_sq_per_girone,
            minuti=min_inizio,
            ore=ora_inizio,
            durata_partita=durata_partita,
            padding=padding
        )

        return params, configuration

    @classmethod
    def fromSpreadsheet(cls, spreadsheet_id, sheet_name=TEAMS_SHEET_NAME, range_team_names=RANGE_TEAM_NAMES):
        params, configuration = cls.presetsFromSpreadsheet(spreadsheet_id, sheet_name, range_team_names)
        return cls(**params, **configuration)

    def partite_to_spreadsheet(self, spreadsheet_id=None, matches_sheet=MATCHES_SHEET_NAME):
        if not spreadsheet_id:
            spreadsheet_id = self.spreadsheet_id

        # Creo il foglio
        sheet_id = create_sheet_if_not_exists(spreadsheet_id, matches_sheet)
        riga_titolo = 1
        riga_inizio_girone = 2

        cols = ['sq1.nome', 'sq2.nome', 'pt1', 'pt2', 'campo.nome', 'ora']
        num_columns = len(cols)
        lettera_fine = chr(ord('A') + num_columns)
        for girone in self.gironi:
            # Rinomino le colonne
            df = girone.partite_df[cols].rename(
                columns={'sq1.nome': "Casa", 'sq2.nome': "Ospite", 'pt1': "Punti Casa", 'pt2': "Punti Ospite",
                         'campo.nome': "Campo", 'ora': "Orario di Inizio"}).fillna('')

            # Ottengo il numero di partite
            num_partite = df.shape[0]

            # Unisco le celle e scrivo il titolo
            title_range_alfa = f"{matches_sheet}!A{riga_titolo}:{lettera_fine}{riga_titolo}"
            # title_range = alpha_to_grid_range(spreadsheet_id, title_range_alfa)

            # range riga titolo
            title_range = get_data_range(sheet_id,
                                         startRowIndex=riga_titolo - 1,  # Parto da 0, quindi riga 1 in excel => 0
                                         endRowIndex=riga_titolo,
                                         # Anche se è la stessa riga, dico quella successiva perchè la fine è esclusa
                                         startColumnIndex=0,  # Anche qui parte da 0, colonna A => 0
                                         endColumnIndex=num_columns  # Colonna in pos n_pos_punti +1
                                         )
            # range riga titolo
            int_range = get_data_range(sheet_id,
                                       startRowIndex=riga_titolo,  # Parto da 0, quindi riga 1 in excel => 0
                                       endRowIndex=riga_titolo + 1,
                                       # Anche se è la stessa riga, dico quella successiva perchè la fine è esclusa
                                       startColumnIndex=0,  # Anche qui parte da 0, colonna A => 0
                                       endColumnIndex=num_columns  # Colonna in pos n_pos_punti +1
                                       )
            # Range con tutto il Girone
            full_range = get_data_range(sheet_id,
                                        startRowIndex=riga_titolo - 1,  # Parto da 0, quindi riga 1 in excel => 0
                                        endRowIndex=riga_inizio_girone + num_partite,
                                        startColumnIndex=0,  # Anche qui parte da 0, colonna A => 0
                                        endColumnIndex=num_columns
                                        # Colonna in pos n_pos_punti + 2 perchè c'è il totale
                                        )
            # Aggiusto la grafica:
            # Unisco le prime celle
            # Allineo al centro nelle celle dei titoli
            # Imposto i bordi
            run(spreadsheet_id,
                mergeCells(title_range),
                setTextFormat(title_range, font_size=18, bold=True),
                alignCenterCells(title_range),
                setTextFormat(int_range, font_size=None, bold=True),
                alignCenterCells(int_range),
                setBorders(full_range)
                )
            writeCells(spreadsheet_id, title_range_alfa, "Partite del " + girone.nome)

            # Stampo la tabella
            df_to_spreadsheet(spreadsheet_id,
                              matches_sheet + f"!A{riga_inizio_girone}:{lettera_fine}", df)

            # Aggiorno i contatori
            riga_titolo = riga_inizio_girone + num_partite + 2
            riga_inizio_girone = riga_inizio_girone + num_partite + 3

        run(spreadsheet_id,
            set_columns_width(dict(sheetId=sheet_id, startIndex=0, endIndex=2), 200)
            )

    def campi_to_spreadsheet(self, spreadsheet_id=None, sheet_name="CAMPI"):
        if not spreadsheet_id:
            spreadsheet_id = self.spreadsheet_id

        # Creo il foglio
        sheet_id = create_sheet_if_not_exists(spreadsheet_id, sheet_name)
        riga_titolo = 1
        riga_inizio_girone = 2

        cols = ['sq1.nome', 'sq2.nome', 'pt1', 'pt2', 'campo.nome', 'ora']
        num_columns = len(cols)
        lettera_fine = chr(ord('A') + num_columns)
        for camp in self.partite_campi:
            print(camp)
            # Rinomino le colonne
            df = camp.ca[cols].rename(
                columns={'sq1.nome': "Casa", 'sq2.nome': "Ospite", 'pt1': "Punti Casa", 'pt2': "Punti Ospite",
                         'campo.nome': "Campo", 'ora': "Orario di Inizio"}).fillna('')

            # Ottengo il numero di partite
            num_partite = df.shape[0]

            # Unisco le celle e scrivo il titolo
            title_range_alfa = f"{sheet_name}!A{riga_titolo}:{lettera_fine}{riga_titolo}"
            # title_range = alpha_to_grid_range(spreadsheet_id, title_range_alfa)

            # range riga titolo
            title_range = get_data_range(sheet_id,
                                         startRowIndex=riga_titolo - 1,  # Parto da 0, quindi riga 1 in excel => 0
                                         endRowIndex=riga_titolo,
                                         # Anche se è la stessa riga, dico quella successiva perchè la fine è esclusa
                                         startColumnIndex=0,  # Anche qui parte da 0, colonna A => 0
                                         endColumnIndex=num_columns  # Colonna in pos n_pos_punti +1
                                         )
            # range riga titolo
            int_range = get_data_range(sheet_id,
                                       startRowIndex=riga_titolo,  # Parto da 0, quindi riga 1 in excel => 0
                                       endRowIndex=riga_titolo + 1,
                                       # Anche se è la stessa riga, dico quella successiva perchè la fine è esclusa
                                       startColumnIndex=0,  # Anche qui parte da 0, colonna A => 0
                                       endColumnIndex=num_columns  # Colonna in pos n_pos_punti +1
                                       )
            # Range con tutto il Girone
            full_range = get_data_range(sheet_id,
                                        startRowIndex=riga_titolo - 1,  # Parto da 0, quindi riga 1 in excel => 0
                                        endRowIndex=riga_inizio_girone + num_partite,
                                        startColumnIndex=0,  # Anche qui parte da 0, colonna A => 0
                                        endColumnIndex=num_columns
                                        # Colonna in pos n_pos_punti + 2 perchè c'è il totale
                                        )
            # Aggiusto la grafica:
            # Unisco le prime celle
            # Allineo al centro nelle celle dei titoli
            # Imposto i bordi
            run(spreadsheet_id,
                mergeCells(title_range),
                setTextFormat(title_range, font_size=18, bold=True),
                alignCenterCells(title_range),
                setTextFormat(int_range, font_size=None, bold=True),
                alignCenterCells(int_range),
                setBorders(full_range)
                )
            writeCells(spreadsheet_id, title_range_alfa, "Partite del " + camp)

            # Stampo la tabella
            df_to_spreadsheet(spreadsheet_id,
                              sheet_name + f"!A{riga_inizio_girone}:{lettera_fine}", df)

            # Aggiorno i contatori
            riga_titolo = riga_inizio_girone + num_partite + 2
            riga_inizio_girone = riga_inizio_girone + num_partite + 3

        run(spreadsheet_id,
            set_columns_width(dict(sheetId=sheet_id, startIndex=0, endIndex=2), 200)
            )

    def classifica_to_df(self, spreadsheet_id=None, classification_sheet=CLASSIFICATION_SHEET_NAME):
        if not spreadsheet_id:
            spreadsheet_id = self.spreadsheet_id

        # Creo il foglio
        sheet_id = create_sheet_if_not_exists(spreadsheet_id, classification_sheet)

        riga_intestazione = 1
        n_possibili_punti = int((self.n_sq_per_girone - 1) * self.punti_per_vittoria)
        colonna_fine_intestazione = num_col(1 + n_possibili_punti + 2)
        # Ottengo il numero di partite
        num_squadre = self.n_sq_per_girone
        for girone in self.gironi:
            value = []
            # Preparo il contenuto dell'intestazione
            intestazione = [[girone.nome] + [""] * n_possibili_punti + ['Totale']]

            # range riga titolo
            title_range = get_data_range(sheet_id,
                                         startRowIndex=riga_intestazione - 1,  # Parto da 0, quindi riga 1 in excel => 0
                                         endRowIndex=riga_intestazione,
                                         # Anche se è la stessa riga, dico quella successiva perchè la fine è esclusa
                                         startColumnIndex=0,  # Anche qui parte da 0, colonna A => 0
                                         endColumnIndex=n_possibili_punti + 1  # Colonna in pos n_pos_punti +1
                                         )

            # Range riga d'Intestazione
            int_range_alfa = f"{classification_sheet}!A{riga_intestazione}:{colonna_fine_intestazione}{riga_intestazione}"
            int_range = get_data_range(sheet_id,
                                       startRowIndex=riga_intestazione - 1,  # Parto da 0, quindi riga 1 in excel => 0
                                       endRowIndex=riga_intestazione,
                                       # Anche se è la stessa riga, dico quella successiva perchè la fine è esclusa
                                       startColumnIndex=0,  # Anche qui parte da 0, colonna A => 0
                                       endColumnIndex=n_possibili_punti + 2
                                       # Colonna in pos n_pos_punti + 2 perchè c'è il totale
                                       )

            # Range con tutto il Girone
            full_range = get_data_range(sheet_id,
                                        startRowIndex=riga_intestazione - 1,  # Parto da 0, quindi riga 1 in excel => 0
                                        endRowIndex=riga_intestazione + num_squadre,
                                        startColumnIndex=0,  # Anche qui parte da 0, colonna A => 0
                                        endColumnIndex=n_possibili_punti + 2
                                        # Colonna in pos n_pos_punti + 2 perchè c'è il totale
                                        )

            # Scrivo l'intestazione come Titolo + Tot
            writeCells(spreadsheet_id, int_range_alfa, intestazione)
            # runValues(spreadsheet_id, batch_insert_text(int_range_alfa, intestazione))

            # Scrivo il contenuto
            value += [[sq.nome] + [""] * n_possibili_punti for sq in girone.squadre]
            value_range = f"{classification_sheet}!A{riga_intestazione + 1}:{colonna_fine_intestazione}"
            writeCells(spreadsheet_id, value_range, value)

            # Aggiusto la grafica:
            # Unisco le prime celle
            # Allineo al centro nelle celle dei titoli
            # Imposto i bordi
            run(spreadsheet_id,
                mergeCells(title_range),
                setTextFormat(title_range, font_size=18, bold=True),
                alignCenterCells(int_range),
                setBorders(full_range)
                )

            # Aggiorno il contatore
            riga_intestazione += num_squadre + 2

        run(spreadsheet_id,
            set_columns_width(dict(sheetId=sheet_id, startIndex=1, endIndex=1 + n_possibili_punti), 20),
            set_columns_width_auto(dict(sheetId=sheet_id, startIndex=0, endIndex=1)),
            set_columns_width_auto(
                dict(sheetId=sheet_id, startIndex=n_possibili_punti + 1, endIndex=n_possibili_punti + 2))
            )

    def save(self, filename):
        file = open(filename, 'wb')
        pickle.dump(self, file)
        file.close()


def appiattisci(p) -> list:
    return [y for x in p for y in x]


def get_partite_possibili(escludere, pl, usati):
    s = list()
    u = list()
    for p in pl:
        if p.s1 not in escludere and p.s2 not in escludere:
            s.append(p)
            u.append(usati[p.s1.id] + usati[p.s2.id])

    df = pd.DataFrame({'partite': s, 'usati': u})
    df.sort_values(by=['usati'], ascending=False, inplace=True)

    return df['partite'].to_list()

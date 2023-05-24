import datetime

import pandas as pd
import numpy as np

from Girone import Girone
from Partita import Partita
from Squadra import Squadra
from Style import SPACE_SQUADRA_NOME, SPACE_ORA_INIZIO_FINE, SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ, NOMI_GIRONI, NOMI_CAMPI, \
    SPACE_PARTITA_DA_SQUADRA


class Torneo:
    nome = None
    n_gironi = 0
    n_campi = 0
    n_turni = 0
    durata_partita = 30
    orario_inizio = datetime.datetime(hour=14, minute=30, day=1, month=1, year=2000)
    squadre = None
    gironi = None
    partite_ordinate = None
    partite = []

    def __init__(self, nome, data: pd.DataFrame, n_gironi, n_campi, n_sq_per_girone=None, padding=True):
        self.nome = nome
        self.n_campi = n_campi
        self.n_gironi = n_gironi
        self.n_sq_per_girone = n_sq_per_girone
        if not self.n_sq_per_girone:
            self.n_sq_per_girone = len(data) // self.n_gironi
        if padding:
            agg = (n_gironi * n_sq_per_girone) - len(data)
            for i in range(agg):
                data.loc[len(data)] = [f"Pad {i + 1}"] * data.loc[0].size
        self.squadre = Squadra.from_df(data)
        self.genera_gironi()
        self.partite = appiattisci([g.partite for g in self.gironi])
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
                p = Partita(None, None, self)
            else:
                p = plt.pop()
                # pt = tuple(p)
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

    # @property
    # def partite(self):
    #     return appiattisci([g.partite for g in self.gironi])

    @property
    def n_squadre(self):
        return len(self.squadre)

    @property
    def partite_df(self):
        pl = []
        for p in self.partite_ordinate:
            pl.append(p.to_df_row())
        return pd.DataFrame(pl)
        # return pd.DataFrame(np.rot90(np.array(self.partite_campi)))

    @property
    def partite_list(self):
        return [tuple(p) for p in self.partite_ordinate]

    def get_partite_per_turno(self, turno):
        return self.partite_ordinate[self.n_campi * turno: self.n_campi * (turno + 1)]

    def stampa_partite_per_campo(self, campo):
        if campo < self.n_campi:
            pl = self.partite_campi[campo]
            for p in pl:
                print(p)

    def stampa_partite_per_campi(self):
        print("X" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)
        print("Partite per Campi".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
        for i in range(self.n_campi):
            print(NOMI_CAMPI[i].center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
            self.stampa_partite_per_campo(i)
            print("-" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)

    def stampa_partite_per_turno(self, turno):
        if turno < self.n_turni:
            for p in self.get_partite_per_turno(turno):
                print(p.partita_campo)

    def stampa_partite_per_turni(self):
        print("X" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)
        print("Partite per Turni".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
        for i in range(self.n_turni):
            print(f"Turno {i}".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
            self.stampa_partite_per_turno(i)
            print("-" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)

    def squadra(self, id):
        if id is not None:
            return self.squadre[id].nome

    def stampa_squadre_per_girone(self):
        print("X" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)
        print("Squadre per girone".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
        for g in self.gironi:
            print(g.nome.center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
            g.stampa_squadre()
            print("-" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)

    def stampa_partite_per_gironi(self):
        print("X" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)
        print("Partite per Gironi".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
        for g in self.gironi:
            print(g.nome.center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
            g.stampa_partite()
            print("-" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)

    def stampa_partite_per_squadre(self):
        print("X" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)
        print("Partite per Squadre".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
        print("".center(SPACE_SQUADRA_NOME), end='')
        for i in range(self.n_turni + 1):
            print(Partita.ora_inizio_partita(self, i).center(SPACE_PARTITA_DA_SQUADRA), end='')
        print()
        for g in self.gironi:
            print(g.nome.center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
            g.stampa_partite_squadre()
            print("-" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)

    def set_risultato(self, turno, campo, p1, p2):
        partita = self.partite_ordinate[turno * self.n_campi + campo]
        partita.set_risultato(p1, p2)


def appiattisci(p):
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

import datetime
import pickle

import pandas as pd

from Girone import Girone
from Partita import Partita
from Squadra import Squadra
from Style import *


class Torneo:
    nome = None
    n_gironi = 0
    n_campi = 0
    n_turni = 0
    durata_partita = None
    orario_inizio = None
    squadre = None
    gironi = None
    partite_ordinate = None
    partite = []

    def __init__(self, nome, data: pd.DataFrame, n_gironi, n_campi, n_sq_per_girone=None, padding=True,
                 orario_inizio=datetime.datetime(hour=14, minute=30, day=1, month=1, year=2000),
                 ore=None, minuti=None, durata_partita=30):
        self.nome = nome
        self.n_campi = n_campi
        self.n_gironi = n_gironi
        self.n_sq_per_girone = n_sq_per_girone
        self.orario_inizio = orario_inizio
        self.durata_partita = durata_partita
        if ore is not None:
            self.orario_inizio = self.orario_inizio.replace(hour=ore)
        if minuti is not None:
            self.orario_inizio = self.orario_inizio.replace(minute=minuti)
        if not self.n_sq_per_girone:
            self.n_sq_per_girone = len(data) // self.n_gironi
        if padding:
            agg = (n_gironi * n_sq_per_girone) - len(data)
            for i in range(agg):
                data.loc[len(data)] = [f"Pad {i + 1}"] * data.loc[0].size
        self.squadre = Squadra.from_df(data)
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

    def squadra(self, id):
        if id is not None:
            return self.squadre[id].nome

    def set_risultato(self, turno, campo, p1, p2):
        partita = self.partite_ordinate[turno * self.n_campi + campo]
        partita.set_risultato(p1, p2)

    @classmethod
    def load(cls):
        return

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

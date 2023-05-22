import datetime

import pandas as pd
import numpy as np


class Torneo:
    def __init__(self, nome, data: pd.DataFrame, n_gironi, n_campi, padding=False):
        self.nome = nome
        self.n_campi = n_campi
        self.n_gironi = n_gironi
        if padding:
            agg = n_gironi - (len(data) % n_gironi)
            print("Aggiungo", agg, "partedo da ", len(data))
            for i in range(agg):
                data.loc[len(data)] = ['Pad'] * data.loc[0].size
        self.squadre = data
        print(f"Genero girone di {self.n_sq_per_girone} sq per {self.n_gironi} gironi partendo da {self.n_squadre} sq")

    nome = None
    n_gironi = 0
    n_campi = 0
    durata_partita = 30
    orario_inizio = datetime.datetime(hour=14, minute=30, day=1, month=1, year=2000)
    squadre = None

    @property
    def n_sq_per_girone(self):
        return self.n_squadre // self.n_gironi

    @property
    def squadre_per_girone(self):
        return [self.squadre[self.n_sq_per_girone * i:self.n_sq_per_girone * (i + 1)] for i in range(self.n_gironi)]

    @property
    def matrice_partite(self):
        return [gen_girone(sqs) for sqs in self.squadre_per_girone]

    @property
    def partite_campi(self):
        return [self.partite_ordinate[i::self.n_campi] for i in range(self.n_campi)]

    @property
    def partite_ordinate(self):
        partite = []
        pl = self.partite
        plt = pl
        usati = [0] * self.n_squadre
        while len(pl) > 0:
            if len(plt) == 0:
                p = {-1}

            else:
                p = plt.pop()
                pt = tuple(p)
                # incremento usati
                usati[pt[0]] += 1
                usati[pt[1]] += 1
                if p in pl:
                    pl.remove(p)

            partite.append(p)
            # sq da escludere
            escludere = [sq for pa in partite[-self.n_campi:] for sq in pa]
            plt = get_partite_possibili(escludere, pl, usati)
        return partite

    @property
    def partite(self):
        return appiattisci(self.matrice_partite)

    @property
    def n_squadre(self):
        return len(self.squadre)

    @property
    def partite_df(self):
        return pd.DataFrame(np.rot90(np.array(self.partite_campi)))

    @property
    def partite_list(self):
        return [tuple(p) for p in self.partite_ordinate]

    def stampa_partite_per_campo(self, campo):
        if campo < self.n_campi:
            pl = self.partite_campi[campo]
            print(f"Campo {campo}".center(101))
            i = 0
            for p in pl:
                p = tuple(p)
                print(f"{self.squadra(p[0])}({self.ora_partita(i)} - {self.ora_partita(i + 1)}){self.squadra(p[1])}")
                i += 1
            print("-" * 101)

    def stampa_partite_per_campi(self):
        print("X" * 101)
        print("Partite per Campi".center(101))
        for i in range(self.n_campi):
            self.stampa_partite_per_campo(i)

    def squadra(self, id):
        return str(self.squadre.iloc[id]['Nome']).center(48)

    def stampa_squadre_per_girone(self):
        print("X" * 101)
        print("Squadre per girone".center(101))
        sq = self.squadre_per_girone
        for g in range(self.n_gironi):
            print(f"Girone {g}".center(101))
            for _, s in sq[g].iterrows():
                print(s['Nome'])

    def stampa_partite_per_gironi(self):
        print("X" * 101)
        print("Partite per Gironi".center(101))
        for g in range(self.n_gironi):
            print(f"Girone {g}".center(101))
            pl = self.matrice_partite[g]
            for p in pl:
                p = tuple(p)
                print(f"{self.squadra(p[0])}   -   {self.squadra(p[1])}")
            print("-" * 101)

    def ora_partita(self, i):
        ora = (self.orario_inizio + datetime.timedelta(minutes=self.durata_partita * i)).time()
        return ora.strftime("%H:%M").center(5)


def gen_girone(df):
    ps = set()
    for i, s1 in df.iterrows():
        for j, s2 in df.iterrows():
            p = frozenset((i, j))
            if i != j:
                ps.add(p)

    return list(ps)


def appiattisci(p):
    return [y for x in p for y in x]


def get_partite_possibili(escludere, pl, usati):
    s = list()
    u = list()
    for p in pl:
        pt = tuple(p)
        if pt[0] not in escludere and pt[1] not in escludere:
            s.append(p)
            u.append(usati[pt[0]] + usati[pt[1]])

    df = pd.DataFrame({'partite': s, 'usati': u})
    df.sort_values(by=['usati'], ascending=False, inplace=True)

    return df['partite'].to_list()

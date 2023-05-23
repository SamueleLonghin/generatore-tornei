import datetime

import pandas as pd
import numpy as np

from Girone import Girone
from Partita import Partita
from Squadra import Squadra


class Torneo:
    nome = None
    n_gironi = 0
    n_campi = 0
    durata_partita = 30
    orario_inizio = datetime.datetime(hour=14, minute=30, day=1, month=1, year=2000)
    squadre = None
    gironi = None
    partite_ordinate = None
    partite = []

    def __init__(self, nome, data: pd.DataFrame, n_gironi, n_campi, n_sq_per_girone=None, padding=False):
        self.nome = nome
        self.n_campi = n_campi
        self.n_gironi = n_gironi
        self.n_sq_per_girone = n_sq_per_girone
        if not self.n_sq_per_girone:
            self.n_sq_per_girone = len(data) // self.n_gironi
        if padding:
            agg = n_gironi - (len(data) % n_gironi)
            print("Aggiungo", agg, "partedo da ", len(data))
            for i in range(agg):
                data.loc[len(data)] = ['Pad'] * data.loc[0].size
        self.squadre = Squadra.from_df(data)
        print(f"Genero girone di {self.n_sq_per_girone} sq per {self.n_gironi} gironi partendo da {self.n_squadre} sq")
        self.gironi = [
            Girone(self, f"Girone {i} ", self.squadre[self.n_sq_per_girone * i:self.n_sq_per_girone * (i + 1)]) for i in
            range(self.n_gironi)]
        self.partite = appiattisci([g.partite for g in self.gironi])
        self.ordina_partite()
        print(self.partite)

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
                p = Partita(None, None)
            else:
                p = plt.pop()
                # pt = tuple(p)
                # incremento usati
                usati[p.s1] += 1
                usati[p.s2] += 1
                if p in pl:
                    pl.remove(p)

            turno = len(partite) // self.n_campi
            p.turno = turno
            partite.append(p)
            # sq da escludere
            i_da = ((turno - 1) * self.n_campi)
            i_da = max(i_da, 0)
            if turno == 1:
                print(1)
            if turno == 2:
                print(1)
            escludere = [sq for pa in partite[i_da:] for sq in pa]
            # escludere = [sq for pa in partite[-self.n_campi:] for sq in pa]
            plt = get_partite_possibili(escludere, pl, usati)
            print(plt)
        self.partite_ordinate = partite

    # @property
    # def partite(self):
    #     return appiattisci([g.partite for g in self.gironi])

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
            i = 0
            for p in pl:
                print(f"{self.squadra(p.s1)}({self.ora_partita(i)} - {self.ora_partita(i + 1)}){self.squadra(p.s2)}")
                i += 1

    def stampa_partite_per_campi(self):
        print("X" * 101)
        print("Partite per Campi".center(101))
        for i in range(self.n_campi):
            print(f"Campo {i}".center(101))
            self.stampa_partite_per_campo(i)
            print("-" * 101)

    def squadra(self, id):
        if id is None:
            out = 'riposo'
        else:
            out = self.squadre[id].nome
        return str(out).center(48)

    def stampa_squadre_per_girone(self):
        print("X" * 101)
        print("Squadre per girone".center(101))
        for g in self.gironi:
            print(g.nome.center(101))
            g.stampa_squadre()
            print("-" * 101)

    def stampa_partite_per_gironi(self):
        print("X" * 101)
        print("Partite per Gironi".center(101))
        for g in self.gironi:
            print(g.nome.center(101))
            g.stampa_partite()
            print("-" * 101)

    def ora_partita(self, i):
        ora = (self.orario_inizio + datetime.timedelta(minutes=self.durata_partita * i)).time()
        return ora.strftime("%H:%M").center(5)


#
# def gen_girone(df):
#     ps = set()
#     for i, s1 in df.iterrows():
#         for j, s2 in df.iterrows():
#             p = frozenset((i, j))
#             if i != j:
#                 ps.add(p)
#
#     return list(ps)
#
#
# def gen_girone_partite(df):
#     ps = set()
#     for i, s1 in df.iterrows():
#         for j, s2 in df.iterrows():
#             p = Partita(i, j)
#             if i != j:
#                 ps.add(p)
#
#     return list(ps)


def appiattisci(p):
    return [y for x in p for y in x]


def get_partite_possibili(escludere, pl, usati):
    s = list()
    u = list()
    for p in pl:
        if p.s1 not in escludere and p.s2 not in escludere:
            s.append(p)
            u.append(usati[p.s1] + usati[p.s2])

    df = pd.DataFrame({'partite': s, 'usati': u})
    df.sort_values(by=['usati'], ascending=False, inplace=True)

    return df['partite'].to_list()

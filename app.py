import numpy as np
import pandas as pd

from spreadsheet import beach


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Partita:
    s1 = -1
    s2 = -1

    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2

    def __contains__(self, item):
        return self.s1 == item or self.s2 == item

    def __eq__(self, other):
        return self.s1 in other and self.s2 in other


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


class Torneo:
    def __init__(self, nome, data, n_gironi, n_campi):
        self.nome = nome
        self.n_campi = n_campi
        self.n_gironi = n_gironi
        self.squadre = data
        print(f"Genero girone di {self.n_sq_per_girone} sq per {self.n_gironi} gironi partendo da {self.n_squadre} sq")

    nome = None
    n_gironi = 0
    n_campi = 0
    durata_partita = 30
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
                # raise "Impossibile"
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
            print(f"Campo {campo}".center(61))
            for p in pl:
                p = tuple(p)
                print(f"{self.squadra(p[0])}- {self.squadra(p[1])}")
            print("-" * 61)

    def stampa_partite_per_campi(self):
        print("X" * 61)
        print("Partite per Campi".center(61))
        for i in range(self.n_campi):
            self.stampa_partite_per_campo(i)

    def __str__(self):
        return f"""\
Torneo {self.nome}
Diviso in {self.n_gironi} gironi da {self.n_sq_per_girone} squadre
Squadre: {self.squadre_per_girone}
Lista Partite: {self.partite_campi}
"""

    def squadra(self, id):
        return str(self.squadre.iloc[id]['Nome']).center(30)

    def stampa_squadre_per_girone(self):
        print("X" * 61)
        print("Squadre per girone".center(61))
        sq = self.squadre_per_girone
        for g in range(self.n_gironi):
            print(f"Girone {g}".center(61))
            for _, s in sq[g].iterrows():
                print(s['Nome'])

    def stampa_partite_per_gironi(self):
        print("X" * 61)
        print("Partite per Gironi".center(61))
        for g in range(self.n_gironi):
            print(f"Girone {g}".center(61))
            pl = self.matrice_partite[g]
            for p in pl:
                p = tuple(p)
                print(f"{self.squadra(p[0])}- {self.squadra(p[1])}")
            print("-" * 61)


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


if __name__ == "__main__":
    # create_connection("./db")
    # crea_sq()
    # insert_sq(("A.C. Picchia", CALCIO))
    # get_sq()

    # data = spreadsheet_to_df(SPREADSHEET_ID, DATA_TO_PULL)
    # data.to_csv('calcetto.csv')
    # genera_gironi(calcetto(), 2)
    sq_beach = beach()
    # sq_beach.to_csv('beach.csv')
    # sq_beach = pd.read_csv('beach.csv')
    # genera_gironi(sq_beach, 3, 1)
    # p1 = Person("John", 36)
    beach = Torneo("Beach", sq_beach, n_gironi=4, n_campi=3)
    beach.stampa_partite_per_campi()
    beach.stampa_partite_per_gironi()
    beach.stampa_squadre_per_girone()
    # stampa_partite(partite)

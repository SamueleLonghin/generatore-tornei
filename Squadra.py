import pandas as pd


class Squadra:
    nome = None
    id = None
    partite = None

    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    @classmethod
    def from_df(cls, data: pd.DataFrame):
        squadre = []
        for i, s in data.iterrows():
            squadre.append(Squadra(i, s['Nome']))
        return squadre

    def stampa_partite(self):
        i = 0
        j = 0
        psl = sorted(self.partite)
        print(f"Partite di {self.nome}:" + (" " * (30 - len(self.nome))), end='')
        while i <= max(psl[-1].turno, 10):
            if len(psl) > j and psl[j].turno == i:
                print(f"({psl[j].campo})".center(5), end='')
                j += 1
            else:
                print("-".center(5), end='')
            i += 1
        print()

    def stampa_turni(self):
        psl = sorted(self.partite)
        print("Stampo", psl[-1])
        for p in psl:
            print("Partita contro", p.s2.nome if p.s1 == self else p.s1.nome, "\t\tal turno", p.turno)
        print()

    def aggiungi_partita(self, p):
        if self.partite:
            self.partite.append(p)
        else:
            self.partite = [p]

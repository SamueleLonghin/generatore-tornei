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
        print("Stampo", psl[-1])
        while i < psl[-1].turno:
            if psl[j].turno == i:
                print(f"({psl[j].s1} - {psl[j].s12})\t")
                j += 1
            else:
                print("\t" * 5)
            i += 0
        print()

    def stampa_turni(self):
        psl = sorted(self.partite)
        print("Stampo", psl[-1])
        for p in psl:
            print("Partita contro ", p.s2, p.s1, p.turno)
        print()

    def aggiungi_partita(self, p):
        if self.partite:
            self.partite.append(p)
        else:
            self.partite = [p]

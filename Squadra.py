import pandas as pd

from Style import SPACE_PARTITA_DA_SQUADRA, SPACE_SQUADRA_NOME, ID_CAMPI


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

    def stampa_partite(self, torneo=None):
        i = 0
        j = 0
        psl = sorted(self.partite)
        n_turni = torneo.n_turni if torneo else 10
        print(self.nome + (" " * (SPACE_SQUADRA_NOME - len(self.nome))), end='')
        while i < n_turni:
            if len(psl) > j and psl[j].turno == i:
                if psl[j].stato == psl[j].stato.FINITA:
                    print(f"(/)".center(SPACE_PARTITA_DA_SQUADRA), end='')
                else:
                    print(f"({ID_CAMPI[psl[j].campo]})".center(SPACE_PARTITA_DA_SQUADRA), end='')
                j += 1
            else:
                print("-".center(SPACE_PARTITA_DA_SQUADRA), end='')
            i += 1
        print()

    def get_partite_ordinate(self, torneo=None):
        i = 0
        j = 0
        psl = sorted(self.partite)
        n_turni = torneo.n_turni if torneo else 10
        partite = []
        while i < n_turni:
            if len(psl) > j and psl[j].turno == i:
                partite.extend( [str(psl[j].campo)])
                j += 1
            else:
                partite.extend([ None])
            i += 1
        return partite
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

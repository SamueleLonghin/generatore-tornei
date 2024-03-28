import pandas as pd

from Style import SPACE_PARTITA_DA_SQUADRA, SPACE_SQUADRA_NOME, ID_CAMPI
from config import ATTRIBUTO_NOME_SQUADRA


class Squadra:
    nome = None
    id = None
    partite = None

    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    def aggiungi_partita(self, p):
        if self.partite:
            self.partite.append(p)
        else:
            self.partite = [p]

    def get_partite_ordinate(self, torneo=None):
        j = 0
        psl = sorted(self.partite)
        partite = []
        for i in range(torneo.n_turni if torneo else 10):
            if len(psl) > j and psl[j].turno == i:
                partite.extend([psl[j]])
                j += 1
            else:
                partite.extend([None])
        return partite

    def stampa_partite(self, torneo=None):
        from Partita import Partita
        print(self.nome + (" " * (SPACE_SQUADRA_NOME - len(self.nome))), end='')
        turno: Partita
        for turno in self.get_partite_ordinate(torneo):
            if turno:
                if turno.stato == turno.stato.FINITA:
                    print(f"(/)".center(SPACE_PARTITA_DA_SQUADRA), end='')
                else:
                    print(f"({ID_CAMPI[turno.campo]})".center(SPACE_PARTITA_DA_SQUADRA), end='')
            else:
                print("-".center(SPACE_PARTITA_DA_SQUADRA), end='')
        print()

    def stampa_turni(self):
        psl = sorted(self.partite)
        print("Stampo", psl[-1])
        for p in psl:
            print("Partita contro", p.s2.nome if p.s1 == self else p.s1.nome, "\t\tal turno", p.turno)
        print()

    @classmethod
    def from_df(cls, data: pd.DataFrame):
        squadre = []
        for i, s in data.iterrows():
            squadre.append(Squadra(i, s[ATTRIBUTO_NOME_SQUADRA]))
        return squadre

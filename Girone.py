from Partita import Partita
from Squadra import Squadra
import pandas as pd


class Girone:
    squadre: [Squadra] = []
    torneo = None
    partite: [Partita] = None
    id = None

    def __init__(self, torneo, nome, id, squadre):
        self.nome = nome
        self.torneo = torneo
        self.id = id
        self.squadre = squadre
        self.genera_partite()

    def genera_partite(self) -> [Partita]:
        ps = set()
        for s1 in self.squadre:
            for s2 in self.squadre:
                if s2.id > s1.id:
                    p = Partita(s1, s2, self)
                    ps.add(p)
                    s1.aggiungi_partita(p)
                    s2.aggiungi_partita(p)
        self.partite = list(ps)

    @property
    def partite_df(self) -> pd.DataFrame:
        return pd.DataFrame([p.to_df_row() for p in self.partite])

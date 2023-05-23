import memo as memo

from Partita import Partita
from Squadra import Squadra


class Girone:
    squadre = []
    torneo = None
    partite = None

    def __init__(self, torneo, nome, squadre):
        self.nome = nome
        self.torneo = torneo
        self.squadre = squadre
        self.genera_partite()
        print(squadre)

    def genera_partite(self):
        ps = set()
        for s1 in self.squadre:
            for s2 in self.squadre:
                p = Partita(s1.id, s2.id)
                if s2.id > s1.id:
                    ps.add(p)
                    s1.aggiungi_partita(p)
                    s2.aggiungi_partita(p)

        self.partite = list(ps)

    def stampa_partite(self):
        for p in self.partite:
            print(f"{self.torneo.squadra(p.s1)}   -   {self.torneo.squadra(p.s2)}")

    def stampa_squadre(self):
        for s in self.squadre:
            print(f"{s.nome}")

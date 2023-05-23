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

    def genera_partite(self):
        ps = set()
        for s1 in self.squadre:
            for s2 in self.squadre:
                p = Partita(s1, s2, self)
                if s2.id > s1.id:
                    ps.add(p)
                    s1.aggiungi_partita(p)
                    s2.aggiungi_partita(p)

        self.partite = list(ps)

    def stampa_partite(self):
        for p in self.partite:
            print(
                f"{p.s1.nome.center(40)}" +
                f"({p.ora_inizio} - {p.ora_fine})".center(21) +
                f"{p.s2.nome.center(40)}"
            )

    def stampa_partite_squadre(self):
        for s in self.squadre:
            s.stampa_partite()

    def stampa_squadre(self):
        for s in self.squadre:
            print(f"{s.nome}")

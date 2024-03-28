from Partita import Partita
from Squadra import Squadra


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

    def genera_partite(self):
        ps = set()
        for s1 in self.squadre:
            for s2 in self.squadre:
                if s2.id > s1.id:
                    p = Partita(s1, s2, self)
                    ps.add(p)
                    s1.aggiungi_partita(p)
                    s2.aggiungi_partita(p)
        self.partite = list(ps)

    # def stampa_partite(self):
    #     for p in self.partite:
    #         print(p)

    # def stampa_partite_squadre(self):
    #     s: Squadra
    #     for s in self.squadre:
    #         s.stampa_partite(self.torneo)

    # def stampa_squadre(self):
    #     for s in self.squadre:
    #         print(f"{s.nome}")

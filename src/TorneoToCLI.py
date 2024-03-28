from Girone import Girone
from Partita import Partita
from Squadra import Squadra
from Style import SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ, NOMI_CAMPI, SPACE_SQUADRA_NOME, SPACE_PARTITA_DA_SQUADRA
from TorneoToDF import TorneoToDF


class TorneoToCLI(TorneoToDF):
    def stampa_partite_per_campi(self):
        print("X" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)
        print("Partite per Campi".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
        for i in range(self.n_campi):
            print(NOMI_CAMPI[i].center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
            pl = self.partite_campi[i]
            for p in pl:
                print(p)
            print("-" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)

    def stampa_partite_per_turni(self):
        print("X" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)
        print("Partite per Turni".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
        for i in range(self.n_turni):
            print(f"Turno {i}".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
            for p in self.partite_per_turno[i]:
                print(p.partita_campo)
            print("-" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)

    def stampa_squadre_per_girone(self):
        print("X" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)
        print("Squadre per girone".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
        for g in self.gironi:
            print(g.nome.center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
            for s in g.squadre:
                print(f"{s.nome}")
            print("-" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)

    def stampa_partite_per_gironi(self):
        print("X" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)
        print("Partite per Gironi".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
        for g in self.gironi:
            print(g.nome.center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
            for p in g.partite:
                print(p)
            print("-" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)

    def stampa_partite_per_squadre(self):
        print("X" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)
        print("Partite per Squadre".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
        print("".center(SPACE_SQUADRA_NOME), end='')
        for i in range(self.n_turni + 1):
            print(Partita.ora_inizio_partita(self, i).center(SPACE_PARTITA_DA_SQUADRA), end='')
        print()
        g: Girone
        for g in self.gironi:
            print(g.nome.center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ))
            s: Squadra
            for s in self.squadre:
                s.stampa_partite(self)
            print("-" * SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)

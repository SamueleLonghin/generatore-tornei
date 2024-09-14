import datetime

from Squadra import Squadra
from Style import SPACE_SQUADRA_NOME, SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ, SPACE_ORA_INIZIO_FINE, NOMI_CAMPI, ID_CAMPI
from support import Stato


class Partita:
    s1 = None
    s2 = None
    set1 = 0
    set2 = 0
    pt1 = None
    pt2 = None
    turno = None
    campo = None
    girone = None
    torneo = None
    stato = Stato.PROGRAMMATA

    def __hash__(self):
        return hash((self.s1.id, self.s2.id))

    def __init__(self, s1, s2, girone, torneo):
        self.s1 = s1
        self.s2 = s2
        self.girone = girone
        self.torneo = torneo

    def __contains__(self, item):
        if type(item) == int:
            return self.s1 == item or self.s2 == item
        elif type(item) == Squadra:
            return self.s1 == item or self.s2 == item
        else:
            print("Cercando di comparare Partita con ", item)

    def __eq__(self, other):
        return self.s1 in other and self.s2 in other

    def __getitem__(self, item):
        return (self.s1, self.s2)[item]

    def __setitem__(self, key, value):
        if key == 0:
            self.s1 = value
        elif key == 1:
            self.s2 = value

    def __lt__(self, other):
        if self.turno is not None and other.turno is not None:
            return self.turno < other.turno
        else:
            return False

    def __str__(self):
        return self.partita_ora

    @property
    def partita_ora(self):
        if self.s1 and self.s2:
            sq1 = self.s1.nome
            sq2 = self.s2.nome
            if self.stato == self.stato.PROGRAMMATA:
                return sq1.center(SPACE_SQUADRA_NOME) + \
                    f"({self.ora_inizio} - {self.ora_fine})".center(SPACE_ORA_INIZIO_FINE) + \
                    sq2.center(SPACE_SQUADRA_NOME)
            elif self.stato == self.stato.IN_GIOCO:
                return sq1.center(SPACE_SQUADRA_NOME) + \
                    f"(in gioco)".center(SPACE_ORA_INIZIO_FINE) + \
                    sq2.center(SPACE_SQUADRA_NOME)
            else:
                if self.pt1 >= self.pt2:
                    sq1 = f"[{sq1}]"
                if self.pt2 >= self.pt1:
                    sq2 = f"[{sq2}]"
                return sq1.center(SPACE_SQUADRA_NOME) + \
                    f"({self.pt1} - {self.pt2})".center(SPACE_ORA_INIZIO_FINE) + \
                    sq2.center(SPACE_SQUADRA_NOME)
        else:
            return f"riposo".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)

    @property
    def partita_campo(self):
        if self.s1 and self.s2:
            sq1 = self.s1.nome
            sq2 = self.s2.nome
            if self.stato == self.stato.PROGRAMMATA:
                return sq1.center(SPACE_SQUADRA_NOME) + \
                    f"({NOMI_CAMPI[self.campo]})".center(SPACE_ORA_INIZIO_FINE) + \
                    sq2.center(SPACE_SQUADRA_NOME)
            elif self.stato == self.stato.IN_GIOCO:
                return sq1.center(SPACE_SQUADRA_NOME) + \
                    f"(in gioco ({ID_CAMPI[self.campo]}))".center(SPACE_ORA_INIZIO_FINE) + \
                    sq2.center(SPACE_SQUADRA_NOME)
            else:
                if self.pt1 >= self.pt2:
                    sq1 = f"[{sq1}]"
                if self.pt2 >= self.pt1:
                    sq2 = f"[{sq2}]"
                return sq1.center(SPACE_SQUADRA_NOME) + \
                    f"{self.pt1} - {self.pt2}".center(SPACE_ORA_INIZIO_FINE) + \
                    sq2.center(SPACE_SQUADRA_NOME)
        else:
            return f"riposo".center(SPACE_RIGA_SQ_ORA_INIZIO_FINE_SQ)

    @property
    def ora_inizio(self):
        return Partita.ora_inizio_partita(self.torneo, self.turno)

    @classmethod
    def ora_inizio_partita(cls, torneo, turno):
        return torneo.ora_inizio_turno(turno).strftime("%H:%M").center(5)

    @property
    def ora_fine(self):
        ora = (self.torneo.dataora_inizio + datetime.timedelta(
            minutes=self.torneo.durata_partita * (self.turno + 1))).time()
        return ora.strftime("%H:%M").center(5)

    def altra(self, s):
        return self.s1 if s == self.s2 else self.s2

    def set_risultato(self, p1, p2):
        self.pt1 = p1
        self.pt2 = p2
        self.stato = Partita.stato.FINITA

    def to_df_row(self):
        return {
            'sq1': self.s1.id,
            'sq2': self.s2.id,
            'sq1.nome': self.s1.nome,
            'sq2.nome': self.s2.nome,
            'turno': self.turno,
            'ora': self.ora_inizio,
            'campo': self.campo,
            'campo.nome': NOMI_CAMPI[self.campo],
            'pt1': self.pt1,
            'pt2': self.pt2,
            'stato': str(self.stato),
            'girone': self.girone.id if self.girone else None
        }

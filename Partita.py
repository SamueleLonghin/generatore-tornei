import datetime

from Squadra import Squadra


class Partita:
    s1 = None
    s2 = None
    set1 = 0
    set2 = 0
    pt1 = 0
    pt2 = 0
    turno = None
    campo = None
    girone = None

    def __hash__(self):
        return hash(k for k in (self.s1.id, self.s2.id))

    def __init__(self, s1, s2, girone):
        self.s1 = s1
        self.s2 = s2
        self.girone = girone

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

    @property
    def ora_inizio(self):
        ora = (self.girone.torneo.orario_inizio + datetime.timedelta(
            minutes=self.girone.torneo.durata_partita * self.turno)).time()
        return ora.strftime("%H:%M").center(5)

    @property
    def ora_fine(self):
        ora = (self.girone.torneo.orario_inizio + datetime.timedelta(
            minutes=self.girone.torneo.durata_partita * (self.turno + 1))).time()
        return ora.strftime("%H:%M").center(5)

    def altra(self, s):
        return self.s1 if s == self.s2 else self.s2

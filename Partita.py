class Partita:
    s1 = -1
    s2 = -1
    set1 = 0
    set2 = 0
    pt1 = 0
    pt2 = 0

    def __hash__(self):
        return hash(k for k in (self.s1, self.s2))

    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2

    def __contains__(self, item):
        if type(item) == int:
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

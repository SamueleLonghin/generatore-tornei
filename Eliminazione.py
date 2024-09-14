import random
import math

from Torneo import Torneo


class Eliminazione:
    torneo: Torneo = None
    divisi = []

    def __init__(self, torneo):
        self.tournament_data = dict(participant=[], stage=[], group=[], round=[], match=[], match_game=[])
        self.genera()

    def genera(self):
        TEAMS_COUNT = 32
        GROUPS = ['A', 'B', 'C', 'D']
        GROUPS_COUNT = len(GROUPS)
        TEAMS_PER_GROUP = TEAMS_COUNT // GROUPS_COUNT  # Squadre per girone
        TOTAL_ROUNDS = int(math.log2(TEAMS_COUNT))
        # Creo la struttura dati desiderata con i risultati nulli all'inizio
        partecipants = {}
        for g in range(GROUPS_COUNT):
            partecipants[GROUPS[g]] = []
            for s in range(TEAMS_PER_GROUP):
                partecipants[GROUPS[g]].append({
                    "id": (g * TEAMS_PER_GROUP + s), "tournament_id": 0,
                    "name": f'Team {s + 1} Group {GROUPS[g]}',
                    "group": GROUPS[g]
                })
        self.tournament_data["participant"] = [item for row in partecipants.values() for item in row]
        # self.tournament_data["participant"] = [{"id": i, "tournament_id": 0, "name": name} for i, name in
        #                                        enumerate([f'Team {i}' for i in range(TEAMS_COUNT)])]
        self.tournament_data["participant"].append({"id": -1, "tournament_id": 0, "name": "", "group": -1})

        self.tournament_data['stage'] = [{
            "id": 0,
            "tournament_id": 0,
            "name": "Torneo super Bellissimo",
            "type": "single_elimination",
            "number": 1,
            "settings": {
                "size": TEAMS_COUNT,
                "seedOrdering": ["natural", "natural", "reverse_half_shift", "reverse"],
                "grandFinal": "grand_final",
                "grandFinalType": "simple",
                "matchesChildCount": 0
            }
        }]

        self.tournament_data["group"] = [{"id": 0, "stage_id": 0, "number": 1}]

        # Generazione dei round in base al numero di partecipanti.
        for i in range(TOTAL_ROUNDS):
            self.tournament_data["round"].append({"id": i, "number": i + 1, "stage_id": 0, "group_id": 0})

        groups_matches = {}

        # Associo le rivalità, in ordine inverso (A->D, D->A, B->C, C->B)
        rivals = {GROUPS[i]: GROUPS[GROUPS_COUNT - 1 - i] for i in range(GROUPS_COUNT)}

        # Associo alle prime 4 di ogni girone le loro avversarie
        for i_g, g in enumerate(GROUPS):
            r = rivals[g]
            groups_matches[g] = []
            for i in range(TEAMS_PER_GROUP // 2):
                f = TEAMS_PER_GROUP - 1 - i
                groups_matches[g].append((partecipants[g][i], partecipants[r][f]))

        first_round_matches = []
        for i in range(GROUPS_COUNT):
            # i è quella testa di serie
            prima = groups_matches[GROUPS[i % GROUPS_COUNT]][0]
            seconda = groups_matches[GROUPS[(i + 3) % GROUPS_COUNT]][3]
            terza = groups_matches[GROUPS[(i + 1) % GROUPS_COUNT]][2]
            quarta = groups_matches[GROUPS[(i + 2) % GROUPS_COUNT]][1]

            if i % 2 == 0:
                first_round_matches += [prima, terza, seconda, quarta]
            else:
                first_round_matches += [prima, seconda, terza, quarta]

        match_id = 0
        for round_id in range(TOTAL_ROUNDS):
            num_matches = TEAMS_COUNT // (2 ** (round_id + 1))
            for match_number in range(num_matches):
                if round_id == 0:
                    opponent1, opponent2 = first_round_matches[match_number]
                else:
                    opponent1 = {"id": -1}  # Placeholder per i round successivi
                    opponent2 = {"id": -1}  # Placeholder per i round successivi

                self.tournament_data["match"].append({
                    "id": match_id,
                    "number": match_number + 1,
                    "stage_id": 0,
                    "group_id": 0,
                    "round_id": round_id,
                    "child_count": 0,
                    "status": 0,
                    "opponent1": opponent1,
                    "opponent2": opponent2
                })
                match_id += 1

    def generaCasuale(self):
        import math
        TEAMS_COUNT = 32
        GROUPS = ['A', 'B', 'C', 'D']
        TEAMS_PER_GROUP = TEAMS_COUNT // len(GROUPS)  # Squadre per girone
        TOTAL_ROUNDS = int(math.log2(TEAMS_COUNT))
        # Creo la struttura dati desiderata con i risultati nulli all'inizio
        self.tournament_data = dict(participant=[], stage=[], group=[], round=[], match=[], match_game=[])
        # self.tournament_data['participant'] = [{"id": i, "tournament_id": 0, "name": name.nome}
        #                                        for i, name in enumerate(teams)]
        # Creazione dei partecipanti suddivisi per girone
        self.tournament_data["participant"] = [
            {"id": i, "tournament_id": 0,
             "name": f'Team {(i % TEAMS_PER_GROUP) + 1} Group {GROUPS[i // TEAMS_PER_GROUP]}',
             "group": GROUPS[i // TEAMS_PER_GROUP]}
            for i in range(TEAMS_COUNT)]
        # self.tournament_data["participant"] = [{"id": i, "tournament_id": 0, "name": name} for i, name in
        #                                        enumerate([f'Team {i}' for i in range(TEAMS_COUNT)])]
        self.tournament_data["participant"].append({"id": -1, "tournament_id": 0, "name": "", "group": -1})

        self.tournament_data['stage'] = [{
            "id": 0,
            "tournament_id": 0,
            "name": "Torneo super Bellissimo",
            "type": "single_elimination",
            "number": 1,
            "settings": {
                "size": TEAMS_COUNT,
                "seedOrdering": ["natural", "natural", "reverse_half_shift", "reverse"],
                "grandFinal": "grand_final",
                "grandFinalType": "simple",
                "matchesChildCount": 0
            }
        }]

        self.tournament_data["group"] = [{"id": 0, "stage_id": 0, "number": 1}]

        # Generazione dei round in base al numero di partecipanti.
        for i in range(TOTAL_ROUNDS):
            self.tournament_data["round"].append({"id": i, "number": i + 1, "stage_id": 0, "group_id": 0})

        # Generazione dei match.
        first_round_matches = []
        second_round_matches = []
        match_id = 0
        num_matches = TEAMS_COUNT // (2 ** (0 + 1))
        print("NUm:", num_matches)
        for match_number in range(num_matches):
            print("Creo la partita ", match_number, "del round", 0)
            # Determinazione degli ID dei team per il primo round
            index1 = match_number
            index2 = TEAMS_PER_GROUP - 1 - match_number
            # if match_number % 2 == 0:  # Gironi A-D e B-C
            group1, group2 = ('A', 'D') if match_number < TEAMS_PER_GROUP else ('B', 'C')
            # else:
            # group1, group2 = ('D', 'A') if match_number < TEAMS_PER_GROUP  else ('C', 'B')
            # print("p1:", [p for p in self.tournament_data["participant"] if p['group'] == group1], index1)
            # print("p2:", [p for p in self.tournament_data["participant"] if p['group'] == group2], index2)
            opponent1 = [p for p in self.tournament_data["participant"] if p['group'] == group1][
                index1 % TEAMS_PER_GROUP]
            opponent2 = [p for p in self.tournament_data["participant"] if p['group'] == group2][
                index2 % TEAMS_PER_GROUP]
            first_round_matches.append((opponent1, opponent2))
            match_id += 1

        # Mescoliamo i match del primo round
        random.shuffle(first_round_matches)

        # Generazione dei match mescolati.
        match_id = 0
        for round_id in range(TOTAL_ROUNDS):
            num_matches = TEAMS_COUNT // (2 ** (round_id + 1))
            for match_number in range(num_matches):
                if round_id == 0:
                    opponent1, opponent2 = first_round_matches[match_number]
                else:
                    opponent1 = {"id": -1}  # Placeholder per i round successivi
                    opponent2 = {"id": -1}  # Placeholder per i round successivi

                self.tournament_data["match"].append({
                    "id": match_id,
                    "number": match_number + 1,
                    "stage_id": 0,
                    "group_id": 0,
                    "round_id": round_id,
                    "child_count": 0,
                    "status": 0,
                    "opponent1": opponent1,
                    "opponent2": opponent2
                })
                match_id += 1

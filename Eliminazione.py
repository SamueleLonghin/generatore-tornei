from Torneo import Torneo


class Eliminazione:
    torneo: Torneo = None

    def __init__(self, torneo):
        # self.torneo = torneo
        groups_count = 3
        # teams = self.torneo.squadre[:(2 ** groups_count) * 2]
        # Definisco la lista delle 16 squadre
        # teams = [f"Team {i+1}" for i in range(16)]

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
        match_id = 0
        for round_id in range(TOTAL_ROUNDS):
            num_matches = TEAMS_COUNT // (2 ** (round_id + 1))
            print("NUm:", num_matches)
            for match_number in range(num_matches):
                print("Creo la partita ", match_number, "del round", round_id)
                # Determinazione degli ID dei team per il primo round
                if round_id == 0:  # Solo il primo round ha abbinamenti speciali
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
        # tournament_data = {
        #     "participant": [
        #         {"id": i, "tournament_id": 0, "name": name.nome} for i, name in enumerate(teams)
        #     ],
        #     "stage": [{
        #         "id": 0,
        #         "tournament_id": 0,
        #         "name": "Torneo super Bellissimo",
        #         "type": "single_elimination",
        #         "number": 1,
        #         "settings": {
        #             "size": 16,
        #             "seedOrdering": ["natural", "natural", "reverse_half_shift", "reverse"],
        #             "grandFinal": "grand_final",
        #             "grandFinalType": "simple",
        #             "matchesChildCount": 0
        #         }
        #     }],
        #     "group": [
        #         {"id": i, "stage_id": 0, "number": i + 1} for i in range(groups_count)
        #     ],
        #     "round": [
        #         {"id": i, "number": i % 4 + 1, "stage_id": 0, "group_id": i // 4} for i in range(12)
        #     ],
        #     "match": [
        #         {
        #             "id": i, "number": i + 1, "stage_id": 0, "group_id": 0, "round_id": i // 8, "child_count": 0,
        #             "status": 0,
        #             "opponent1": None if i > 15 else
        #             {"id": 2 * i, "position": 2 * i + 1, "score": None, "result": None},
        #             "opponent2": None if i > 15 else
        #             {"id": 2 * i + 1, "position": 2 * i + 2, "score": None, "result": None}
        #         } for i in range(31)  # Numero arbitrario di partite
        #     ],
        #     "match_game": [
        #
        #     ]
        # }

from Torneo import Torneo


class Eliminazione:
    torneo: Torneo = None

    def __init__(self, torneo):
        # self.torneo = torneo
        groups_count = 3
        # teams = self.torneo.squadre[:(2 ** groups_count) * 2]
        # Definisco la lista delle 16 squadre
        # teams = [f"Team {i+1}" for i in range(16)]

        TEAMS_COUNT = 32

        # Creo la struttura dati desiderata con i risultati nulli all'inizio
        self.tournament_data = dict(participant=[], stage=[], group=[], round=[], match=[], match_game=[])
        # self.tournament_data['participant'] = [{"id": i, "tournament_id": 0, "name": name.nome}
        #                                        for i, name in enumerate(teams)]
        self.tournament_data["participant"] = [{"id": i, "tournament_id": 0, "name": name} for i, name in
                                               enumerate([f'Team {i}' for i in range(TEAMS_COUNT)])]
        self.tournament_data["participant"].append({"id": -1, "tournament_id": 0, "name": ""})

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
        import math
        total_rounds = int(math.log2(TEAMS_COUNT))
        for i in range(total_rounds):
            self.tournament_data["round"].append({"id": i, "number": i + 1, "stage_id": 0, "group_id": 0})

        # Generazione dei match.
        match_id = 0
        for round_id in range(total_rounds):
            num_matches = TEAMS_COUNT // (2 ** (round_id + 1))
            for match_number in range(num_matches):
                self.tournament_data["match"].append({
                    "id": match_id,
                    "number": match_number + 1,
                    "stage_id": 0,
                    "group_id": 0,
                    "round_id": round_id,
                    "child_count": 0,
                    "status": 0,
                    "opponent1": {"id": -1},
                    "opponent2": {"id": -1}
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

import pandas as pd

from Partita import Partita
from Style import NOMI_CAMPI, NOMI_TURNI
from Torneo import Torneo


class TorneoToDF(Torneo):
    def df_squadre_per_girone(self):
        df = pd.DataFrame(columns=['Squadra', 'Girone'])
        for g in self.gironi:
            for s in g.squadre:
                df.loc[len(df)] = (s.nome, g.nome)
        return df

    def df_partite_per_gironi(self):
        gironi = []
        cols = ['Casa', 'Orario', 'Ospite', 'Girone']
        for g in self.gironi:
            girone = [[p.s1.nome, p.ora_inizio, p.s2.nome, g.nome] for p in g.partite]
            df = pd.DataFrame(girone, columns=cols)
            gironi.append(df)
        return pd.concat(gironi, ignore_index=True)

    def df_partite_per_turni(self):
        turni = []
        cols = ['Casa', 'Campo', 'Ospite', 'Inizio', 'Fine', 'Turno']
        for i in range(self.n_turni):
            turno = [[p.s1.nome, p.campo, p.s2.nome, p.ora_inizio, p.ora_fine, NOMI_TURNI[i]] for p in
                     self.partite_per_turno[i]]
            df = pd.DataFrame(turno, columns=cols)
            turni.append(df)
        return pd.concat(turni, ignore_index=True)

    def df_partite_per_campi(self):
        campi = []
        cols = ['Casa', 'Orario', 'Ospite']
        for i in range(self.n_campi):
            campo = [[p.s1.nome, p.ora_inizio, p.s2.nome] for p in self.partite_campi[i]]
            df = pd.DataFrame(campo, columns=cols)
            df['Campo'] = NOMI_CAMPI[i]
            campi.append(df)

        return pd.concat(campi, ignore_index=True)

    def df_partite_per_squadre(self):
        cols = ['squadra', 'girone']
        c = [Partita.ora_inizio_partita(self, i) for i in range(self.n_turni)]
        cols += c
        df = pd.DataFrame(columns=cols)
        for g in self.gironi:
            for s in g.squadre:
                ss = [s.nome, g.nome]
                sp = [NOMI_CAMPI[int(p.campo)] if p else '' for p in s.get_partite_ordinate(self)]
                sf = ss + sp
                df.loc[len(df)] = sf
        return df

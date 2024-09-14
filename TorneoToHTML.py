from flask import render_template

from Style import NOMI_TURNI, NOMI_CAMPI
from TorneoToDF import TorneoToDF


def df_to_html(df):
    return df.to_html(classes=['table', 'table-hover', 'table-bordered'], index=False)


class TorneoToHTML(TorneoToDF):
    def html_partite_per_gironi(self):
        df = self.df_partite_per_gironi()
        html = ""
        gironi = []
        for (groupName, groupDf) in df.groupby('Girone'):
            gironi.append(groupDf.iloc[0]['Girone'])
            groupDf = groupDf.drop('Girone', axis=1)
            html += f"<td>{df_to_html(groupDf)}</td>"

        gironi = ''.join(['<th> {} </th>'.format(c) for c in gironi])
        return f"<table> <thead> <tr> {gironi} </tr> </thead> <tbody> <tr> {html} </tr> </tbody> </table>"

    def html_partite_per_turni(self):
        df = self.df_partite_per_turni()
        html = ""
        turni = ""
        for ((groupName, groupDf), i) in zip(df.groupby('Turno'), range(1, self.n_turni)):
            inizio = groupDf.iloc[0]['Inizio']
            fine = groupDf.iloc[0]['Fine']
            groupDf = groupDf.drop(['Turno', 'Inizio', 'Fine'], axis=1)
            html += f"<tr> <th> {NOMI_TURNI[i]} </th> <td> {inizio} - {fine} </td> <td>{df_to_html(groupDf)}</td> </tr>"
        return f"<table> <thead> <tr> {turni} </tr> </thead> <tbody>  {html} </tbody> </table>"

    def html_partite_per_campi(self):
        df = self.df_partite_per_campi()
        html = ""
        for (groupName, groupDf) in df.groupby('Campo'):
            groupDf = groupDf.drop('Campo', axis=1)
            html += f"<td>{df_to_html(groupDf)}</td>"

        campi = ''.join(['<th> {} </th>'.format(c) for c in NOMI_CAMPI[:self.n_campi]])
        return f"<table> <thead> <tr> {campi} </tr> </thead> <tbody> <tr> {html} </tr> </tbody> </table>"

    def html_partite_per_squadra(self):
        return df_to_html(self.df_partite_per_squadre().fillna(''))

    def html_squadre_per_girone(self):
        df = self.df_squadre_per_girone()
        html = ""
        for (groupName, groupDf) in df.groupby('Girone'):
            groupDf = groupDf.drop('Girone', axis=1)
            groupDf.rename(columns={'Squadra': groupName}, inplace=True)
            html += f"<td>{df_to_html(groupDf)}</td>"

        return f"<table> <tbody> <tr> {html} </tr> </tbody> </table>"

    def html_orari(self):
        data = [["La prima partita inizia alle", self.orario_inizio],
                ["Per la fase a gironi sono necessari", f"{self.n_turni} turni"],
                ["L'ultima partita della fase a gironi termina alle", self.orario_fine_gironi]]
        html = ""
        for th, td in data:
            html += f"<tr><th> {th} </th> <td> {td} </td> </tr>"

        return f"<table class='table table-striped'><tbody> {html} </tbody></table>"

    def html_info(self):
        data = [["Numero Gironi", self.n_gironi],
                ["Numero Campi", self.n_campi],
                ["Numero Squadre per Girone", self.n_sq_per_girone],
                ["Numero Turni", self.n_turni],
                ["Durata Partita", self.durata_partita],
                ]
        html = ""
        for th, td in data:
            html += f"<tr><th> {th} </th> <td> {td} </td> </tr>"

        return f"<table class='table table-striped'><tbody> {html} </tbody></table>"

    def toHTML(self):
        sq_per_gir = self.html_squadre_per_girone()
        pa_per_sq = self.html_partite_per_squadra()
        pa_per_cm = self.html_partite_per_campi()
        pa_per_tu = self.html_partite_per_turni()
        pa_per_gi = self.html_partite_per_gironi()
        info = self.html_info()
        orari = self.html_orari()

        return render_template("torneo.html", title=self.nome,
                               info=info + orari,
                               html=sq_per_gir + pa_per_sq + pa_per_cm + pa_per_tu + pa_per_gi)

    def getHTMLComponents(self):
        sq_per_gir = self.html_squadre_per_girone()
        pa_per_sq = self.html_partite_per_squadra()
        pa_per_cm = self.html_partite_per_campi()
        pa_per_tu = self.html_partite_per_turni()
        pa_per_gi = self.html_partite_per_gironi()
        info = self.html_info()
        orari = self.html_orari()

        return dict(title=self.nome,
                    info=info + orari,
                    html=sq_per_gir + pa_per_sq + pa_per_cm + pa_per_tu + pa_per_gi)

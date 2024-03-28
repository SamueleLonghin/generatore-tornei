from src.Style import NOMI_TURNI, NOMI_CAMPI
from src.TorneoToDF import TorneoToDF


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
        gironi = []
        for (groupName, groupDf) in df.groupby('Girone'):
            gironi.append(groupDf.iloc[0]['Girone'])
            groupDf = groupDf.drop('Girone', axis=1)
            html += f"<td>{df_to_html(groupDf)}</td>"

        gironi = ''.join(['<th> {} </th>'.format(c) for c in gironi])
        return f"<table> <thead> <tr> {gironi} </tr> </thead> <tbody> <tr> {html} </tr> </tbody> </table>"

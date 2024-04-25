import pickle

from secret import SPREADSHEET_ID
from spreadsheet import calcetto, spreadsheet_to_df
from TorneoToCLI import TorneoToCLI

if __name__ == "__main__":
    spreadsheet_id = "1_4bVk0UlmRALqKLRcIm_ZwrKGXw0STMHl3Ek_dFaE1s"
    squadre = spreadsheet_to_df(spreadsheet_id)
    torneo = TorneoToCLI("Torneo Ping Pong 2^ edizione", squadre, spreadsheet_id=spreadsheet_id,
                         n_gironi=4,
                         n_campi=4,
                         n_sq_per_girone=11,
                         padding=True
                         )

    """EXPORT"""
    # file = open('torneo.export', 'wb')
    # pickle.dump(torneo, file)
    # file.close()
    """INPORT"""
    # file2 = open('torneo.export', 'rb')
    # torneo: TorneoToCLI = pickle.load(file2)

    torneo.stampa_partite_per_campi()
    # # torneo.set_risultato(4, 0, 3, 2)
    torneo.stampa_partite_per_turni()
    #
    torneo.stampa_partite_per_gironi()
    torneo.stampa_squadre_per_girone()
    torneo.stampa_partite_per_squadre()
    torneo.stampa_orari()

    # sqg = torneo.df_squadre_per_girone()
    # torneo.stampa_partite_per_squadre()
    # df = torneo.partite_df
    # df.to_csv("partite.csv")

    # Salvo Torneo
    # torneo.save('calcetto.export')

    """
    SPREADSHEET
    """
    torneo.partite_to_spreadsheet()
    torneo.classifica_to_df()

    # print()
    # print(sqg)
    # print()

    # torneo.df_partite_per_squadre().to_csv('partite_squadre.csv')

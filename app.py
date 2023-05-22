from spreadsheet import beach, calcetto
from Torneo import Torneo

if __name__ == "__main__":
    # create_connection("./db")
    # crea_sq()
    # insert_sq(("A.C. Picchia", CALCIO))
    # get_sq()

    # data = spreadsheet_to_df(SPREADSHEET_ID, DATA_TO_PULL)
    # data.to_csv('calcetto.csv')
    # genera_gironi(calcetto(), 2)
    sq_beach = beach()
    # sq_beach.to_csv('beach.csv')
    # sq_beach = pd.read_csv('beach.csv')
    # genera_gironi(sq_beach, 3, 1)
    # p1 = Person("John", 36)
    # beach = Torneo("Beach", sq_beach, n_gironi=4, n_campi=2, padding=False)
    beach = Torneo("Beach", sq_beach, n_gironi=4, n_campi=3, padding=True)
    # beach = Torneo("Calcetto", calcetto(), n_gironi=4, n_campi=2, padding=True)
    beach.stampa_partite_per_campi()
    beach.stampa_partite_per_gironi()
    beach.stampa_squadre_per_girone()
    # stampa_partite(partite)

from Torneo import Torneo

from spreadsheet import calcetto

if __name__ == "__main__":
    # create_connection("./db")
    # crea_sq()
    # insert_sq(("A.C. Picchia", CALCIO))
    # get_sq()

    # data = spreadsheet_to_df(SPREADSHEET_ID, DATA_TO_PULL)
    # data.to_csv('calcetto.csv')
    # genera_gironi(calcetto(), 2)
    # sq_beach = beach()
    # sq_beach = beach()
    sq_calcetto = calcetto()
    # sq_beach.to_csv('beach.csv')
    # sq_beach = pd.read_csv('squadre.csv')
    # genera_gironi(sq_beach, 3, 1)
    # p1 = Person("John", 36)
    """
    Beach Volley
    """
    ## Versione che si userà -> 4 triangolari in due campi d'erba
    # torneo = Torneo("Beach", sq_beach, n_gironi=4, n_campi=2, n_sq_per_girone=3)
    ## Variante con utilizzo del terzo campo
    # torneo = Torneo("Beach", sq, n_gironi=4, n_campi=3, n_sq_per_girone=3)

    """
    Calcetto
    """
    ## Versione 8 sq in 2 gironi
    # torneo = Torneo("Calcetto", sq_calcetto, n_gironi=2, n_campi=2, n_sq_per_girone=4)
    ## Versione 9 sq in 3 gironi
    # torneo = Torneo("Calcetto", sq_calcetto, n_gironi=3, n_campi=2, n_sq_per_girone=3)
    ## Versione 10 sq in 2 gironi
    # torneo = Torneo("Calcetto", sq_calcetto, n_gironi=2, n_campi=2, n_sq_per_girone=5)
    ## Versione 12 sq in 3 gironi
    # torneo = Torneo("Calcetto", sq_beach, n_gironi=3, n_campi=2, n_sq_per_girone=4)
    ## Versione 4 triangolari
    torneo = Torneo("Calcetto", sq_calcetto, n_gironi=3, n_campi=1, n_sq_per_girone=4, minuti=0, ore=9,
                    durata_partita=25)
    # file = open('torneo.export', 'wb')
    # pickle.dump(torneo, file)
    # file.close()

    # # torneo = None
    # file2 = open('torneo.export', 'rb')
    # torneo: Torneo = pickle.load(file2)
    # beach = Torneo("Calcetto", calcetto(), n_gironi=4, n_campi=2, padding=True)
    torneo.stampa_partite_per_campi()
    # torneo.set_risultato(4, 0, 3, 2)
    torneo.stampa_partite_per_turni()

    torneo.stampa_partite_per_gironi()
    torneo.stampa_squadre_per_girone()
    sqg = torneo.df_squadre_per_girone()
    # torneo.stampa_partite_per_squadre()
    # df = torneo.partite_df
    # df.to_csv("partite.csv")

    # Salvo Torneo
    torneo.save('calcetto.export')
    # stampa_partite(partite)

    print()
    print(sqg)
    print()

    torneo.df_partite_per_squadre().to_csv('partite_squadre.csv')

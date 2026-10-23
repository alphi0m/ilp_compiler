from pathlib import Path

CALCOLATRICE = Path(__file__).parent.parent / "examples" / "calcolatrice.al"

MENU = "1) Somma 2) Sottrazione 3) Moltiplicazione 4) Divisione\n"


def giro(risultato):
    return (
        MENU
        + "Primo numero:\n"
        + "Secondo numero:\n"
        + "Risultato:\n"
        + risultato
        + "Continuare? 1 = si, 0 = no\n"
    )


def test_un_solo_calcolo(esegui_file):
    r = esegui_file(CALCOLATRICE, "1\n2\n3\n0\n")
    assert r.returncode == 0
    assert r.stdout == giro("5\n")


def test_tutte_le_operazioni(esegui_file):
    ingresso = "1\n2\n3\n1\n2\n10\n4\n1\n3\n2.5\n2\n1\n4\n9\n2\n0\n"
    r = esegui_file(CALCOLATRICE, ingresso)
    assert r.stdout == (
        giro("5\n") + giro("6\n") + giro("5\n") + giro("4.5\n")
    )


def test_divisione_per_zero(esegui_file):
    r = esegui_file(CALCOLATRICE, "4\n1\n0\n0\n")
    assert r.stdout == giro("Errore: divisione per zero\n0\n")


def test_ciclo_di_continuazione(esegui_file):
    r = esegui_file(CALCOLATRICE, "1\n1\n1\n1\n1\n2\n2\n0\n")
    assert r.stdout == giro("2\n") + giro("4\n")

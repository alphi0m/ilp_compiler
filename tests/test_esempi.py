from pathlib import Path

import pytest

ESEMPI = Path(__file__).parent.parent / "examples"


@pytest.mark.parametrize(
    "nome, ingresso, atteso",
    [
        ("fattoriale.al", "5\n", "Inserisci un intero:\n120\n"),
        (
            "fibonacci.al",
            "7\n",
            "Quanti numeri di Fibonacci?\n0\n1\n1\n2\n3\n5\n8\n",
        ),
        (
            "numeri_primi.al",
            "20\n",
            "Numeri primi fino a:\n2\n3\n5\n7\n11\n13\n17\n19\n",
        ),
        (
            "media.al",
            "4\n1\n2\n3\n4\n",
            "Quanti numeri?\nNumero:\nNumero:\nNumero:\nNumero:\nMedia:\n2.5\n",
        ),
        ("media.al", "0\n", "Quanti numeri?\n"),
    ],
)
def test_esempi_validi(esegui_file, nome, ingresso, atteso):
    r = esegui_file(ESEMPI / nome, ingresso)
    assert r.returncode == 0
    assert r.stdout == atteso


@pytest.mark.parametrize(
    "nome, messaggio",
    [
        ("errore_sintassi.al", "errore di sintassi alla riga 4"),
        ("errore_tipo.al", "impossibile assegnare real a 'n'"),
        ("errore_non_dichiarata.al", "identificatore 'b' non dichiarato"),
        ("errore_argomenti.al", "vuole 2 argomenti, ne ha 1"),
        ("errore_return.al", "l'ultima istruzione deve essere un return"),
        ("errore_main.al", "manca la funzione 'main'"),
    ],
)
def test_esempi_con_errori(esegui_file, nome, messaggio):
    r = esegui_file(ESEMPI / "errori" / nome)
    assert r.returncode == 1
    assert r.stdout == ""
    assert messaggio in r.stderr

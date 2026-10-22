import pytest

from symbol_table import (
    ErroreSemantico,
    SimboloFunzione,
    TabellaFunzioni,
    TabellaVariabili,
)


def test_cerca_variabile_dichiarata():
    t = TabellaVariabili()
    t.dichiara("x", "integer")
    assert t.cerca("x") == "integer"


def test_variabile_non_dichiarata():
    assert TabellaVariabili().cerca("x") is None


def test_variabile_dichiarata_due_volte():
    t = TabellaVariabili()
    t.dichiara("x", "integer")
    with pytest.raises(ErroreSemantico):
        t.dichiara("x", "real")


def test_cerca_funzione_dichiarata():
    t = TabellaFunzioni()
    f = SimboloFunzione("somma", ["integer", "integer"], "integer")
    t.dichiara(f)
    assert t.cerca("somma") == f


def test_funzione_non_dichiarata():
    assert TabellaFunzioni().cerca("somma") is None


def test_funzione_dichiarata_due_volte():
    t = TabellaFunzioni()
    t.dichiara(SimboloFunzione("main", [], None))
    with pytest.raises(ErroreSemantico):
        t.dichiara(SimboloFunzione("main", [], None))

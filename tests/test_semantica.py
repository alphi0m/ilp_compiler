from pathlib import Path

import pytest

from parser import parse, parse_file
from semantica import analizza
from symbol_table import ErroreSemantico

CALCOLATRICE = Path(__file__).parent.parent / "examples" / "calcolatrice.al"

FATTORIALE = """
func fattoriale(n: integer) -> integer
    var r: integer;
    r = 1;
    while n > 1 do
        r = r * n;
        n = n - 1;
    endwhile
    return r;
endfunc

func main()
    var n: integer;
    read(n);
    print(fattoriale(n));
endfunc
"""


def programma(corpo_main):
    return analizza(parse("func main()\n" + corpo_main + "\nendfunc"))


def test_calcolatrice_corretta():
    analizza(parse_file(CALCOLATRICE))


def test_fattoriale_corretto():
    analizza(parse(FATTORIALE))


def test_tipi_annotati():
    p = programma("var x: real;\nx = 1 + 2.5;")
    espressione = p.functions[0].body[1].expr
    assert espressione.type == "real"
    assert espressione.left.type == "integer"
    assert espressione.right.type == "real"


def test_confronto_ha_tipo_bool():
    p = programma("var x: integer;\nif x > 1 then\n print(x);\nendif")
    assert p.functions[0].body[1].cond.type == "bool"


def test_divisione_tra_interi_resta_intera():
    p = programma("var x: integer;\nx = 7 / 2;")
    assert p.functions[0].body[1].expr.type == "integer"


def test_promozione_integer_a_real():
    programma("var x: real;\nx = 3;")


def test_chiamata_come_istruzione_di_funzione_con_ritorno():
    analizza(
        parse(
            "func f() -> integer\n return 1;\nendfunc\n"
            "func main()\n f();\nendfunc"
        )
    )


def test_funzione_chiamata_prima_della_definizione():
    analizza(
        parse(
            "func main()\n print(f());\nendfunc\n"
            "func f() -> integer\n return 1;\nendfunc"
        )
    )


@pytest.mark.parametrize(
    "sorgente",
    [
        # identificatore non dichiarato
        "func main()\n x = 1;\nendfunc",
        # uso prima della dichiarazione
        "func main()\n x = 1;\n var x: integer;\nendfunc",
        # variabile dichiarata due volte
        "func main()\n var x: integer;\n var x: real;\nendfunc",
        # parametro e variabile con lo stesso nome
        "func f(a: integer)\n var a: integer;\nendfunc\nfunc main()\nendfunc",
        # funzione dichiarata due volte
        "func main()\nendfunc\nfunc main()\nendfunc",
        # main assente
        "func f()\nendfunc",
        # main con parametri
        "func main(a: integer)\nendfunc",
        # main con tipo di ritorno
        "func main() -> integer\n return 1;\nendfunc",
        # real assegnato a integer
        "func main()\n var n: integer;\n n = 2.5;\nendfunc",
        # stringa assegnata a variabile
        'func main()\n var n: integer;\n n = "a";\nendfunc',
        # condizione non booleana
        "func main()\n var n: integer;\n while n do\n n = 1;\n endwhile\nendfunc",
        # funzione con ritorno che non termina con return
        "func f(a: integer) -> integer\n print(a);\nendfunc\nfunc main()\nendfunc",
        # return con valore in funzione senza ritorno
        "func f()\n return 1;\nendfunc\nfunc main()\nendfunc",
        # return senza valore in funzione con ritorno
        "func f() -> integer\n return;\nendfunc\nfunc main()\nendfunc",
        # return di tipo sbagliato
        "func f() -> integer\n return 1.5;\nendfunc\nfunc main()\nendfunc",
        # operazione su stringa
        'func main()\n print("a" + 1);\nendfunc',
        # confronto tra stringhe
        'func main()\n var n: integer;\n if "a" == "b" then\n n = 1;\n endif\nendfunc',
        # meno unario su stringa
        'func main()\n print(-"a");\nendfunc',
        # numero di argomenti errato
        "func f(a: integer)\nendfunc\nfunc main()\n f(1, 2);\nendfunc",
        # tipo di argomento errato
        "func f(a: integer)\nendfunc\nfunc main()\n f(1.5);\nendfunc",
        # funzione non definita
        "func main()\n g();\nendfunc",
        # funzione senza ritorno usata in un'espressione
        "func f()\nendfunc\nfunc main()\n print(f());\nendfunc",
        # read su variabile non dichiarata
        "func main()\n read(x);\nendfunc",
        # print di un confronto
        "func main()\n print(1 < 2);\nendfunc",
        # costante intera fuori intervallo
        "func main()\n var n: integer;\n n = 3000000000;\nendfunc",
    ],
)
def test_errori_semantici(sorgente):
    with pytest.raises(ErroreSemantico):
        analizza(parse(sorgente))

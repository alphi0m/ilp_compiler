import subprocess
import sys
from pathlib import Path

MAIN = Path(__file__).parent.parent / "src" / "main.py"


def main_con(corpo):
    return "func main()\n" + corpo + "\nendfunc"


def test_aritmetica_intera(esegui):
    r = esegui(main_con("print(2 + 3 * 4);"))
    assert r.stdout == "14\n"


def test_divisione_intera(esegui):
    r = esegui(main_con("print(7 / 2);"))
    assert r.stdout == "3\n"


def test_aritmetica_reale(esegui):
    r = esegui(main_con("print(7.0 / 2.0);"))
    assert r.stdout == "3.5\n"


def test_promozione_integer_a_real(esegui):
    r = esegui(main_con("var x: real;\nx = 3;\nprint(x / 2);"))
    assert r.stdout == "1.5\n"


def test_meno_unario(esegui):
    r = esegui(main_con("print(-5);\nprint(-2.5);"))
    assert r.stdout == "-5\n-2.5\n"


def test_variabili_inizializzate_a_zero(esegui):
    r = esegui(main_con("var n: integer;\nvar x: real;\nprint(n);\nprint(x);"))
    assert r.stdout == "0\n0\n"


def test_stringa(esegui):
    r = esegui(main_con('print("ciao 100%");'))
    assert r.stdout == "ciao 100%\n"


def test_if_else(esegui):
    corpo = 'if 1 < 2 then\n print("si");\nelse\n print("no");\nendif'
    assert esegui(main_con(corpo)).stdout == "si\n"
    corpo = 'if 2 < 1 then\n print("si");\nelse\n print("no");\nendif'
    assert esegui(main_con(corpo)).stdout == "no\n"


def test_confronto_misto_integer_real(esegui):
    r = esegui(main_con('if 2 < 2.5 then\n print("ok");\nendif'))
    assert r.stdout == "ok\n"


def test_while(esegui):
    corpo = (
        "var i: integer;\nvar s: integer;\ni = 1;\n"
        "while i <= 4 do\n s = s + i;\n i = i + 1;\nendwhile\nprint(s);"
    )
    assert esegui(main_con(corpo)).stdout == "10\n"


def test_read_integer_e_real(esegui):
    corpo = "var n: integer;\nvar x: real;\nread(n);\nread(x);\nprint(n);\nprint(x * 2.0);"
    r = esegui(main_con(corpo), "3\n2.5\n")
    assert r.stdout == "3\n5\n"


def test_funzione_con_parametri(esegui):
    sorgente = (
        "func somma(a: integer, b: real) -> real\n return a + b;\nendfunc\n"
        + main_con("print(somma(1, 2.5));")
    )
    assert esegui(sorgente).stdout == "3.5\n"


def test_argomento_integer_per_parametro_real(esegui):
    sorgente = (
        "func meta(x: real) -> real\n return x / 2.0;\nendfunc\n"
        + main_con("print(meta(5));")
    )
    assert esegui(sorgente).stdout == "2.5\n"


def test_ricorsione(esegui):
    sorgente = (
        "func f(n: integer) -> integer\n"
        " if n <= 1 then\n  return 1;\n endif\n"
        " return n * f(n - 1);\nendfunc\n" + main_con("print(f(5));")
    )
    assert esegui(sorgente).stdout == "120\n"


def test_funzione_chiamata_prima_della_definizione(esegui):
    sorgente = main_con("print(f());") + "\nfunc f() -> integer\n return 7;\nendfunc"
    assert esegui(sorgente).stdout == "7\n"


def test_return_anticipato_in_funzione_senza_ritorno(esegui):
    sorgente = (
        "func stampa(n: integer)\n"
        " if n == 0 then\n  return;\n endif\n"
        " print(n);\nendfunc\n" + main_con("stampa(0);\nstampa(7);")
    )
    assert esegui(sorgente).stdout == "7\n"


def test_return_dentro_while(esegui):
    sorgente = (
        "func primo_maggiore(n: integer) -> integer\n"
        " var i: integer;\n i = 0;\n"
        " while 1 == 1 do\n  i = i + 1;\n"
        "  if i > n then\n   return i;\n  endif\n endwhile\n"
        " return 0;\nendfunc\n" + main_con("print(primo_maggiore(4));")
    )
    assert esegui(sorgente).stdout == "5\n"


def test_funzione_utente_con_nome_di_libreria_c(esegui):
    sorgente = (
        "func printf() -> integer\n return 4;\nendfunc\n"
        + main_con("print(printf());")
    )
    assert esegui(sorgente).stdout == "4\n"


def test_errore_semantico_da_riga_di_comando(esegui):
    r = esegui(main_con("x = 1;"))
    assert r.returncode == 1
    assert "Errore" in r.stderr


def test_errore_sintattico_da_riga_di_comando(esegui):
    r = esegui("func main()\n x = 1\nendfunc")
    assert r.returncode == 1
    assert "Errore" in r.stderr


def test_generazione_file_ll(tmp_path):
    sorgente = tmp_path / "p.al"
    sorgente.write_text(main_con('print("ciao");'), encoding="utf-8")
    r = subprocess.run(
        [sys.executable, str(MAIN), str(sorgente)], capture_output=True, text=True
    )
    assert r.returncode == 0
    assert "define i32 @\"main\"" in (tmp_path / "p.ll").read_text()

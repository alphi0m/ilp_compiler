from pathlib import Path

import pytest

import ast_nodes as ast
from parser import ErroreSintattico, parse, parse_file

CALCOLATRICE = Path(__file__).parent.parent / "examples" / "calcolatrice.al"


def corpo_main(istruzioni):
    programma = parse("func main()\n" + istruzioni + "\nendfunc")
    return programma.functions[0].body


def espressione(testo):
    return corpo_main("x = " + testo + ";")[0].expr


def test_calcolatrice():
    programma = parse_file(CALCOLATRICE)
    nomi = [f.name for f in programma.functions]
    assert nomi == ["dividi", "calcola", "main"]
    assert programma.functions[2].params == []
    assert programma.functions[2].return_type is None


def test_funzione_con_parametri_e_ritorno():
    programma = parse(
        "func somma(a: integer, b: real) -> real\n"
        "    return a + b;\n"
        "endfunc"
    )
    f = programma.functions[0]
    assert f.params == [ast.Param("a", "integer"), ast.Param("b", "real")]
    assert f.return_type == "real"
    assert f.body == [
        ast.Return(ast.BinOp("+", ast.VarRef("a"), ast.VarRef("b")))
    ]


def test_dichiarazione_e_assegnazione():
    corpo = corpo_main("var n: integer;\nn = 5;")
    assert corpo == [ast.VarDecl("n", "integer"), ast.Assign("n", ast.IntConst(5))]


def test_precedenza_moltiplicazione():
    atteso = ast.BinOp(
        "+", ast.IntConst(1), ast.BinOp("*", ast.IntConst(2), ast.IntConst(3))
    )
    assert espressione("1 + 2 * 3") == atteso


def test_parentesi():
    atteso = ast.BinOp(
        "*", ast.BinOp("+", ast.IntConst(1), ast.IntConst(2)), ast.IntConst(3)
    )
    assert espressione("(1 + 2) * 3") == atteso


def test_sottrazione_associativa_a_sinistra():
    atteso = ast.BinOp(
        "-", ast.BinOp("-", ast.VarRef("a"), ast.VarRef("b")), ast.VarRef("c")
    )
    assert espressione("a - b - c") == atteso


def test_meno_unario():
    assert espressione("-a") == ast.Neg(ast.VarRef("a"))


def test_confronto_dopo_aritmetica():
    atteso = ast.BinOp(
        "<", ast.BinOp("+", ast.VarRef("a"), ast.IntConst(1)), ast.VarRef("b")
    )
    assert espressione("a + 1 < b") == atteso


def test_costanti():
    assert espressione("2.5") == ast.RealConst(2.5)
    assert espressione('"ciao"') == ast.StringConst("ciao")


def test_chiamata_con_argomenti():
    atteso = ast.Call("f", [ast.IntConst(1), ast.VarRef("x")])
    assert espressione("f(1, x)") == atteso


def test_chiamata_senza_argomenti_come_istruzione():
    assert corpo_main("f();") == [ast.CallStat(ast.Call("f", []))]


def test_if_senza_else():
    corpo = corpo_main("if a == 1 then\n print(a);\nendif")
    atteso = ast.If(
        ast.BinOp("==", ast.VarRef("a"), ast.IntConst(1)),
        [ast.Print(ast.VarRef("a"))],
        [],
    )
    assert corpo == [atteso]


def test_if_con_else():
    corpo = corpo_main("if a > 0 then\n print(1);\nelse\n print(2);\nendif")
    assert corpo[0].then_body == [ast.Print(ast.IntConst(1))]
    assert corpo[0].else_body == [ast.Print(ast.IntConst(2))]


def test_while_e_read():
    corpo = corpo_main("while n > 0 do\n read(n);\nendwhile")
    assert corpo == [
        ast.While(
            ast.BinOp(">", ast.VarRef("n"), ast.IntConst(0)),
            [ast.Read("n")],
        )
    ]


def test_return_senza_espressione():
    assert corpo_main("return;") == [ast.Return(None)]


@pytest.mark.parametrize(
    "sorgente",
    [
        "func main()\n    x = 1\nendfunc",
        "func main()\n    var x;\nendfunc",
        "func main()\n    if x > 0 then\n        print(x);\nendfunc",
        "func main()\n    x = 1;\n",
        "func main()\n    x = 1 + ;\nendfunc",
        "func main()\n    x = a < b < c;\nendfunc",
        "func main()\n    x = @;\nendfunc",
        "x = 1;",
        "",
    ],
)
def test_errori_sintattici(sorgente):
    with pytest.raises(ErroreSintattico):
        parse(sorgente)

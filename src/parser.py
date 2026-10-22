from pathlib import Path

from lark import Lark, Transformer
from lark.exceptions import UnexpectedInput

import ast_nodes as ast

GRAMMATICA = Path(__file__).with_name("grammatica.lark")
_lark = Lark(GRAMMATICA.read_text(encoding="utf-8"), parser="lalr")


class ErroreSintattico(Exception):
    pass


class CostruttoreAst(Transformer):
    def start(self, c):
        return ast.Program(c)

    def func_decl(self, c):
        nome = str(c[0])
        corpo = c[-1]
        params = []
        tipo_ritorno = None
        for x in c[1:-1]:
            if isinstance(x, list):
                params = x
            else:
                tipo_ritorno = x
        return ast.Function(nome, params, tipo_ritorno, corpo)

    def params(self, c):
        return list(c)

    def param(self, c):
        return ast.Param(str(c[0]), c[1])

    def type(self, c):
        return str(c[0])

    def body(self, c):
        return list(c)

    def var_decl(self, c):
        return ast.VarDecl(str(c[0]), c[1])

    def assign(self, c):
        return ast.Assign(str(c[0]), c[1])

    def call_stat(self, c):
        return ast.CallStat(c[0])

    def return_stat(self, c):
        return ast.Return(c[0] if c else None)

    def print_stat(self, c):
        return ast.Print(c[0])

    def read_stat(self, c):
        return ast.Read(str(c[0]))

    def if_stat(self, c):
        else_body = c[2] if len(c) > 2 else []
        return ast.If(c[0], c[1], else_body)

    def while_stat(self, c):
        return ast.While(c[0], c[1])

    def eq(self, c):
        return ast.BinOp("==", c[0], c[1])

    def ne(self, c):
        return ast.BinOp("!=", c[0], c[1])

    def lt(self, c):
        return ast.BinOp("<", c[0], c[1])

    def le(self, c):
        return ast.BinOp("<=", c[0], c[1])

    def gt(self, c):
        return ast.BinOp(">", c[0], c[1])

    def ge(self, c):
        return ast.BinOp(">=", c[0], c[1])

    def add(self, c):
        return ast.BinOp("+", c[0], c[1])

    def sub(self, c):
        return ast.BinOp("-", c[0], c[1])

    def mul(self, c):
        return ast.BinOp("*", c[0], c[1])

    def div(self, c):
        return ast.BinOp("/", c[0], c[1])

    def neg(self, c):
        return ast.Neg(c[0])

    def int_const(self, c):
        return ast.IntConst(int(c[0]))

    def real_const(self, c):
        return ast.RealConst(float(c[0]))

    def string_const(self, c):
        return ast.StringConst(str(c[0])[1:-1])

    def var_ref(self, c):
        return ast.VarRef(str(c[0]))

    def call(self, c):
        args = c[1] if len(c) > 1 else []
        return ast.Call(str(c[0]), args)

    def args(self, c):
        return list(c)


def parse(sorgente):
    try:
        albero = _lark.parse(sorgente)
    except UnexpectedInput as e:
        raise ErroreSintattico(
            f"errore di sintassi alla riga {e.line}, colonna {e.column}"
        ) from e
    return CostruttoreAst().transform(albero)


def parse_file(percorso):
    return parse(Path(percorso).read_text(encoding="utf-8"))

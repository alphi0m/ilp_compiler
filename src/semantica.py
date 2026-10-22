import ast_nodes as ast
from symbol_table import (
    ErroreSemantico,
    SimboloFunzione,
    TabellaFunzioni,
    TabellaVariabili,
)

NUMERICI = ("integer", "real")
INT_MIN = -(2**31)
INT_MAX = 2**31 - 1


def compatibile(atteso, trovato):
    return atteso == trovato or (atteso == "real" and trovato == "integer")


class AnalizzatoreSemantico:
    def __init__(self):
        self.funzioni = TabellaFunzioni()
        self.variabili = None
        self.funzione = None

    def errore(self, messaggio):
        raise ErroreSemantico(f"in '{self.funzione.name}': {messaggio}")

    # ---------- programma e funzioni ----------

    def analizza(self, programma):
        for f in programma.functions:
            tipi = [p.type for p in f.params]
            self.funzioni.dichiara(SimboloFunzione(f.name, tipi, f.return_type))
        self.controlla_main()
        for f in programma.functions:
            self.analizza_funzione(f)
        return programma

    def controlla_main(self):
        main = self.funzioni.cerca("main")
        if main is None:
            raise ErroreSemantico("manca la funzione 'main'")
        if main.tipi_parametri or main.tipo_ritorno is not None:
            raise ErroreSemantico(
                "'main' non deve avere parametri ne' tipo di ritorno"
            )

    def analizza_funzione(self, f):
        self.funzione = f
        self.variabili = TabellaVariabili()
        for p in f.params:
            self.variabili.dichiara(p.name, p.type)
        self.analizza_corpo(f.body)
        if f.return_type is not None:
            if not f.body or not isinstance(f.body[-1], ast.Return):
                self.errore("l'ultima istruzione deve essere un return")

    # ---------- istruzioni ----------

    def analizza_corpo(self, corpo):
        for s in corpo:
            self.analizza_istruzione(s)

    def analizza_istruzione(self, s):
        match s:
            case ast.VarDecl():
                self.variabili.dichiara(s.name, s.type)
            case ast.Assign():
                tipo_var = self.tipo_variabile(s.name)
                tipo_expr = self.tipo(s.expr)
                if not compatibile(tipo_var, tipo_expr):
                    self.errore(
                        f"impossibile assegnare {tipo_expr} a '{s.name}' "
                        f"di tipo {tipo_var}"
                    )
            case ast.CallStat():
                self.tipo_chiamata(s.call, in_espressione=False)
            case ast.Return():
                self.analizza_return(s)
            case ast.Print():
                tipo = self.tipo(s.expr)
                if tipo not in NUMERICI + ("string",):
                    self.errore(f"print non accetta il tipo {tipo}")
            case ast.Read():
                tipo = self.tipo_variabile(s.name)
                if tipo not in NUMERICI:
                    self.errore(f"read richiede una variabile numerica: '{s.name}'")
            case ast.If():
                self.controlla_condizione(s.cond)
                self.analizza_corpo(s.then_body)
                self.analizza_corpo(s.else_body)
            case ast.While():
                self.controlla_condizione(s.cond)
                self.analizza_corpo(s.body)

    def analizza_return(self, s):
        atteso = self.funzione.return_type
        if atteso is None:
            if s.expr is not None:
                self.errore("return con valore in una funzione senza tipo di ritorno")
            return
        if s.expr is None:
            self.errore("return senza valore in una funzione con tipo di ritorno")
        tipo = self.tipo(s.expr)
        if not compatibile(atteso, tipo):
            self.errore(f"return di tipo {tipo}, atteso {atteso}")

    def controlla_condizione(self, cond):
        tipo = self.tipo(cond)
        if tipo != "bool":
            self.errore(f"la condizione deve essere un confronto, trovato {tipo}")

    # ---------- espressioni ----------

    def tipo_variabile(self, nome):
        tipo = self.variabili.cerca(nome)
        if tipo is None:
            self.errore(f"identificatore '{nome}' non dichiarato")
        return tipo

    def tipo(self, e):
        e.type = self.calcola_tipo(e)
        return e.type

    def calcola_tipo(self, e):
        match e:
            case ast.IntConst():
                if not INT_MIN <= e.value <= INT_MAX:
                    self.errore(f"costante intera fuori intervallo: {e.value}")
                return "integer"
            case ast.RealConst():
                return "real"
            case ast.StringConst():
                return "string"
            case ast.VarRef():
                return self.tipo_variabile(e.name)
            case ast.Neg():
                tipo = self.tipo(e.operand)
                if tipo not in NUMERICI:
                    self.errore(f"meno unario non applicabile al tipo {tipo}")
                return tipo
            case ast.BinOp():
                return self.tipo_binario(e)
            case ast.Call():
                return self.tipo_chiamata(e, in_espressione=True)

    def tipo_binario(self, e):
        sinistro = self.tipo(e.left)
        destro = self.tipo(e.right)
        if sinistro not in NUMERICI or destro not in NUMERICI:
            self.errore(
                f"operatore '{e.op}' non applicabile a {sinistro} e {destro}"
            )
        if e.op in ("==", "!=", "<", "<=", ">", ">="):
            return "bool"
        if "real" in (sinistro, destro):
            return "real"
        return "integer"

    def tipo_chiamata(self, chiamata, in_espressione):
        simbolo = self.funzioni.cerca(chiamata.name)
        if simbolo is None:
            self.errore(f"funzione '{chiamata.name}' non definita")
        if len(chiamata.args) != len(simbolo.tipi_parametri):
            self.errore(
                f"'{chiamata.name}' vuole {len(simbolo.tipi_parametri)} "
                f"argomenti, ne ha {len(chiamata.args)}"
            )
        for arg, atteso in zip(chiamata.args, simbolo.tipi_parametri):
            tipo = self.tipo(arg)
            if not compatibile(atteso, tipo):
                self.errore(
                    f"argomento di tipo {tipo} in '{chiamata.name}', "
                    f"atteso {atteso}"
                )
        if in_espressione and simbolo.tipo_ritorno is None:
            self.errore(f"'{chiamata.name}' non restituisce un valore")
        chiamata.type = simbolo.tipo_ritorno
        return chiamata.type


def analizza(programma):
    return AnalizzatoreSemantico().analizza(programma)

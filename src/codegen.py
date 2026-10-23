from llvmlite import binding, ir

import ast_nodes as ast

I32 = ir.IntType(32)
I8 = ir.IntType(8)
DOUBLE = ir.DoubleType()
PTR = I8.as_pointer()
TIPI = {"integer": I32, "real": DOUBLE}
CONFRONTI = ("==", "!=", "<", "<=", ">", ">=")


def raccogli_dichiarazioni(corpo):
    dichiarazioni = []
    for s in corpo:
        match s:
            case ast.VarDecl():
                dichiarazioni.append(s)
            case ast.If():
                dichiarazioni += raccogli_dichiarazioni(s.then_body)
                dichiarazioni += raccogli_dichiarazioni(s.else_body)
            case ast.While():
                dichiarazioni += raccogli_dichiarazioni(s.body)
    return dichiarazioni


class GeneratoreIR:
    def __init__(self):
        self.modulo = ir.Module(name="programma")
        self.modulo.triple = binding.get_default_triple()
        tipo_io = ir.FunctionType(I32, [PTR], var_arg=True)
        self.printf = ir.Function(self.modulo, tipo_io, name="printf")
        self.scanf = ir.Function(self.modulo, tipo_io, name="scanf")
        self.stringhe = {}
        self.funzioni = {}
        self.firme = {}
        self.builder = None
        self.funzione_ast = None
        self.variabili = {}
        self.tipi = {}

    # ---------- programma e funzioni ----------

    def genera(self, programma):
        for f in programma.functions:
            self.dichiara_funzione(f)
        for f in programma.functions:
            self.genera_funzione(f)
        return str(self.modulo)

    def dichiara_funzione(self, f):
        if f.name == "main":
            nome = "main"
            tipo_ritorno = I32
        else:
            nome = "al_" + f.name
            tipo_ritorno = TIPI[f.return_type] if f.return_type else ir.VoidType()
        tipo = ir.FunctionType(tipo_ritorno, [TIPI[p.type] for p in f.params])
        self.funzioni[f.name] = ir.Function(self.modulo, tipo, name=nome)
        self.firme[f.name] = f

    def genera_funzione(self, f):
        self.funzione_ast = f
        funzione = self.funzioni[f.name]
        self.builder = ir.IRBuilder(funzione.append_basic_block("entry"))
        self.variabili = {}
        self.tipi = {}
        for p, argomento in zip(f.params, funzione.args):
            self.crea_variabile(p.name, p.type)
            self.builder.store(argomento, self.variabili[p.name])
        for d in raccogli_dichiarazioni(f.body):
            self.crea_variabile(d.name, d.type)
        self.corpo(f.body)
        if not self.builder.block.is_terminated:
            self.chiudi_funzione()

    def crea_variabile(self, nome, tipo):
        self.variabili[nome] = self.builder.alloca(TIPI[tipo], name=nome)
        self.tipi[nome] = tipo

    def chiudi_funzione(self):
        if self.funzione_ast.name == "main":
            self.builder.ret(ir.Constant(I32, 0))
        elif self.funzione_ast.return_type is None:
            self.builder.ret_void()
        else:
            self.builder.unreachable()

    # ---------- istruzioni ----------

    def corpo(self, istruzioni):
        for s in istruzioni:
            if self.builder.block.is_terminated:
                break
            self.istruzione(s)

    def istruzione(self, s):
        match s:
            case ast.VarDecl():
                zero = ir.Constant(TIPI[s.type], 0.0 if s.type == "real" else 0)
                self.builder.store(zero, self.variabili[s.name])
            case ast.Assign():
                valore = self.espressione(s.expr)
                valore = self.converti(valore, s.expr.type, self.tipi[s.name])
                self.builder.store(valore, self.variabili[s.name])
            case ast.CallStat():
                self.chiamata(s.call)
            case ast.Return():
                self.istruzione_return(s)
            case ast.Print():
                self.istruzione_print(s)
            case ast.Read():
                formato = "%d" if self.tipi[s.name] == "integer" else "%lf"
                self.builder.call(
                    self.scanf, [self.stringa(formato), self.variabili[s.name]]
                )
            case ast.If():
                self.istruzione_if(s)
            case ast.While():
                self.istruzione_while(s)

    def istruzione_return(self, s):
        if self.funzione_ast.name == "main":
            self.builder.ret(ir.Constant(I32, 0))
        elif s.expr is None:
            self.builder.ret_void()
        else:
            valore = self.espressione(s.expr)
            valore = self.converti(
                valore, s.expr.type, self.funzione_ast.return_type
            )
            self.builder.ret(valore)

    def istruzione_print(self, s):
        tipo = s.expr.type
        if tipo == "string":
            argomento = self.stringa(s.expr.value)
            formato = self.stringa("%s\n")
        elif tipo == "integer":
            argomento = self.espressione(s.expr)
            formato = self.stringa("%d\n")
        else:
            argomento = self.espressione(s.expr)
            formato = self.stringa("%g\n")
        self.builder.call(self.printf, [formato, argomento])

    def nuovo_blocco(self, nome):
        return self.builder.function.append_basic_block(nome)

    def salta_a(self, blocco):
        if not self.builder.block.is_terminated:
            self.builder.branch(blocco)

    def istruzione_if(self, s):
        condizione = self.espressione(s.cond)
        blocco_then = self.nuovo_blocco("then")
        blocco_else = self.nuovo_blocco("else")
        blocco_fine = self.nuovo_blocco("endif")
        self.builder.cbranch(condizione, blocco_then, blocco_else)
        self.builder.position_at_end(blocco_then)
        self.corpo(s.then_body)
        self.salta_a(blocco_fine)
        self.builder.position_at_end(blocco_else)
        self.corpo(s.else_body)
        self.salta_a(blocco_fine)
        self.builder.position_at_end(blocco_fine)

    def istruzione_while(self, s):
        blocco_cond = self.nuovo_blocco("while_cond")
        blocco_corpo = self.nuovo_blocco("while_body")
        blocco_fine = self.nuovo_blocco("endwhile")
        self.builder.branch(blocco_cond)
        self.builder.position_at_end(blocco_cond)
        condizione = self.espressione(s.cond)
        self.builder.cbranch(condizione, blocco_corpo, blocco_fine)
        self.builder.position_at_end(blocco_corpo)
        self.corpo(s.body)
        self.salta_a(blocco_cond)
        self.builder.position_at_end(blocco_fine)

    # ---------- espressioni ----------

    def espressione(self, e):
        match e:
            case ast.IntConst():
                return ir.Constant(I32, e.value)
            case ast.RealConst():
                return ir.Constant(DOUBLE, e.value)
            case ast.VarRef():
                return self.builder.load(self.variabili[e.name])
            case ast.Neg():
                valore = self.espressione(e.operand)
                if e.type == "integer":
                    return self.builder.neg(valore)
                return self.builder.fneg(valore)
            case ast.BinOp():
                return self.binario(e)
            case ast.Call():
                return self.chiamata(e)

    def binario(self, e):
        sinistro = self.espressione(e.left)
        destro = self.espressione(e.right)
        if e.op in CONFRONTI:
            if "real" in (e.left.type, e.right.type):
                sinistro = self.converti(sinistro, e.left.type, "real")
                destro = self.converti(destro, e.right.type, "real")
                return self.builder.fcmp_ordered(e.op, sinistro, destro)
            return self.builder.icmp_signed(e.op, sinistro, destro)
        if e.type == "real":
            sinistro = self.converti(sinistro, e.left.type, "real")
            destro = self.converti(destro, e.right.type, "real")
            istruzioni = {
                "+": self.builder.fadd,
                "-": self.builder.fsub,
                "*": self.builder.fmul,
                "/": self.builder.fdiv,
            }
        else:
            istruzioni = {
                "+": self.builder.add,
                "-": self.builder.sub,
                "*": self.builder.mul,
                "/": self.builder.sdiv,
            }
        return istruzioni[e.op](sinistro, destro)

    def chiamata(self, c):
        firma = self.firme[c.name]
        argomenti = []
        for arg, param in zip(c.args, firma.params):
            valore = self.espressione(arg)
            argomenti.append(self.converti(valore, arg.type, param.type))
        return self.builder.call(self.funzioni[c.name], argomenti)

    def converti(self, valore, da, a):
        if da == "integer" and a == "real":
            return self.builder.sitofp(valore, DOUBLE)
        return valore

    # ---------- stringhe ----------

    def stringa(self, testo):
        if testo not in self.stringhe:
            dati = bytearray(testo.encode("utf-8") + b"\0")
            tipo = ir.ArrayType(I8, len(dati))
            globale = ir.GlobalVariable(
                self.modulo, tipo, name=f".str{len(self.stringhe)}"
            )
            globale.global_constant = True
            globale.linkage = "internal"
            globale.initializer = ir.Constant(tipo, dati)
            zero = ir.Constant(I32, 0)
            self.stringhe[testo] = globale.gep([zero, zero])
        return self.stringhe[testo]


def genera_ir(programma):
    return GeneratoreIR().genera(programma)

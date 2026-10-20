from dataclasses import dataclass, field


# ---------- Programma ----------

@dataclass
class Program:
    functions: list


@dataclass
class Param:
    name: str
    type: str


@dataclass
class Function:
    name: str
    params: list
    return_type: str | None
    body: list


# ---------- Istruzioni ----------

@dataclass
class VarDecl:
    name: str
    type: str


@dataclass
class Assign:
    name: str
    expr: object


@dataclass
class CallStat:
    call: object


@dataclass
class Return:
    expr: object | None


@dataclass
class Print:
    expr: object


@dataclass
class Read:
    name: str


@dataclass
class If:
    cond: object
    then_body: list
    else_body: list


@dataclass
class While:
    cond: object
    body: list


# ---------- Espressioni ----------
# Il campo type viene riempito dall'analisi semantica.

@dataclass
class IntConst:
    value: int
    type: str | None = field(default=None, compare=False)


@dataclass
class RealConst:
    value: float
    type: str | None = field(default=None, compare=False)


@dataclass
class StringConst:
    value: str
    type: str | None = field(default=None, compare=False)


@dataclass
class VarRef:
    name: str
    type: str | None = field(default=None, compare=False)


@dataclass
class Call:
    name: str
    args: list
    type: str | None = field(default=None, compare=False)


@dataclass
class BinOp:
    op: str
    left: object
    right: object
    type: str | None = field(default=None, compare=False)


@dataclass
class Neg:
    operand: object
    type: str | None = field(default=None, compare=False)

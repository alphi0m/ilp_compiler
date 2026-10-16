# Specifica del linguaggio

Progetto del corso di Ingegneria dei Linguaggi di Programmazione.
Estensione dei file sorgente: `.al`

## 1. Specifiche lessicali

### 1.1 Parole chiave

| Token | Lessema |
|---|---|
| FUNC | `func` |
| ENDFUNC | `endfunc` |
| VAR | `var` |
| IF | `if` |
| THEN | `then` |
| ELSE | `else` |
| ENDIF | `endif` |
| WHILE | `while` |
| DO | `do` |
| ENDWHILE | `endwhile` |
| RETURN | `return` |
| PRINT | `print` |
| READ | `read` |
| INTEGER | `integer` |
| REAL | `real` |

### 1.2 Operatori e simboli

| Token | Lessema |
|---|---|
| PLUS | `+` |
| MINUS | `-` |
| TIMES | `*` |
| DIV | `/` |
| ASSIGN | `=` |
| EQ | `==` |
| NE | `!=` |
| LT | `<` |
| LE | `<=` |
| GT | `>` |
| GE | `>=` |
| TYPERETURN | `->` |
| COLON | `:` |
| SEMI | `;` |
| COMMA | `,` |
| LPAR | `(` |
| RPAR | `)` |

### 1.3 Token a pattern

| Token | Descrizione | Esempi |
|---|---|---|
| ID | lettera o `_` seguita da lettere, cifre o `_` | `calcola`, `x`, `continua` |
| INTEGER_CONST | una o più cifre | `1`, `42` |
| REAL_CONST | cifre, punto, cifre | `0.0`, `2.5` |
| STRING_CONST | testo tra doppi apici, senza a capo | `"Primo numero:"` |

### 1.4 Altre regole lessicali

- Spazi, tab e a capo sono ignorati.
- Non sono previsti commenti.
- `main` non è un token a parte: è un normale ID. Che esista una funzione `main` è una regola semantica.

## 2. Specifiche sintattiche

La grammatica formale, in sintassi Lark, è in `src/grammatica.lark`. Di seguito la stessa grammatica in forma BNF.

### 2.1 Programma e funzioni

```
Program     ::= Function Program
              | Function

Function    ::= FUNC ID LPAR Params RPAR ReturnType Body ENDFUNC

Params      ::= Param COMMA Params
              | Param
              | /* vuoto */

Param       ::= ID COLON Type

ReturnType  ::= TYPERETURN Type
              | /* vuoto */

Type        ::= INTEGER
              | REAL
```

### 2.2 Corpo e istruzioni

```
Body        ::= VarDecl Body
              | Stat Body
              | /* vuoto */

VarDecl     ::= VAR ID COLON Type SEMI

Stat        ::= ID ASSIGN Expr SEMI
              | Call SEMI
              | RETURN Expr SEMI
              | RETURN SEMI
              | PRINT LPAR Expr RPAR SEMI
              | READ LPAR ID RPAR SEMI
              | IF Expr THEN Body ENDIF
              | IF Expr THEN Body ELSE Body ENDIF
              | WHILE Expr DO Body ENDWHILE
```

### 2.3 Espressioni

Dalla precedenza più bassa alla più alta:

```
Expr        ::= Sum
              | Sum EQ Sum | Sum NE Sum
              | Sum LT Sum | Sum LE Sum
              | Sum GT Sum | Sum GE Sum

Sum         ::= Sum PLUS Term
              | Sum MINUS Term
              | Term

Term        ::= Term TIMES Factor
              | Term DIV Factor
              | Factor

Factor      ::= MINUS Factor
              | Atom

Atom        ::= INTEGER_CONST
              | REAL_CONST
              | STRING_CONST
              | ID
              | Call
              | LPAR Expr RPAR

Call        ::= ID LPAR Args RPAR

Args        ::= Expr COMMA Args
              | Expr
              | /* vuoto */
```

### 2.4 Note sintattiche

- Un programma contiene una o più funzioni, in qualsiasi ordine.
- La funzione `main` non ha tipo di ritorno: `-> Tipo` è facoltativo.
- Le dichiarazioni `var` e le istruzioni possono alternarsi nel corpo.
- `print` è un'unica istruzione e accetta stringhe ed espressioni.
- I confronti non sono associativi: `a < b < c` non è ammesso.
- `if`, `while` e le funzioni non vogliono `;` dopo `endif`, `endwhile`, `endfunc`.
- Il tipo booleano non esiste: le condizioni di `if` e `while` sono confronti.

### 2.5 Esempi corretti

```
func somma(a: integer, b: integer) -> integer
    return a + b;
endfunc
```

```
func main()
    var x: real;
    read(x);
    if x > 0.0 then
        print("positivo");
    else
        print("non positivo");
    endif
endfunc
```

### 2.6 Esempi sintatticamente errati

Manca il `;` dopo `return`:

```
func somma(a: integer, b: integer) -> integer
    return a + b
endfunc
```

Manca il tipo nella dichiarazione di variabile:

```
func main()
    var x;
endfunc
```

Manca `endif` a chiusura dell'`if`:

```
func main()
    if x > 0 then
        print("ok");
endfunc
```

## 3. Specifiche semantiche

_Da completare._

## 4. Esempi di programmi

Vedi `examples/calcolatrice.al`.

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

### 3.1 Tipi

| Tipo | Rappresentazione | Note |
|---|---|---|
| `integer` | intero a 32 bit con segno | dichiarabile |
| `real` | virgola mobile a 64 bit (double) | dichiarabile |
| stringa | costante di testo | **non** dichiarabile: esiste solo come argomento di `print` |
| bool | risultato di un confronto | **non** dichiarabile: usabile solo come condizione di `if` e `while` |

Le costanti intere fuori dall'intervallo a 32 bit sono un errore.

### 3.2 Scoping

Il linguaggio ha un **unico scope per funzione**:

- I nomi delle funzioni sono globali e unici. Non c'è overloading.
- I parametri e le variabili dichiarate in una funzione appartengono allo scope di quella funzione. I blocchi di `if` e `while` **non** creano un nuovo scope.
- Un nome non può essere dichiarato due volte nello stesso scope, né come parametro né come variabile.
- Una variabile deve essere dichiarata **prima** dell'uso, in ordine testuale.
- Le funzioni possono essere chiamate prima della loro definizione e possono essere ricorsive.
- Ogni variabile è inizializzata a `0` (integer) o `0.0` (real) al momento della dichiarazione.
- Non esistono variabili globali.

### 3.3 Programma e funzioni

- Deve esistere **una e una sola** funzione `main`, senza parametri e senza tipo di ritorno. L'esecuzione parte da lì.
- Una funzione con tipo di ritorno deve avere come **ultima istruzione del corpo** un `return` con un'espressione di tipo compatibile.
- Una funzione senza tipo di ritorno può usare solo `return;`, senza espressione.
- I parametri sono passati per valore e possono essere modificati nel corpo della funzione, senza effetto sul chiamante.

### 3.4 Compatibilità dei tipi

**Promozione implicita:** un `integer` può essere usato dove è richiesto un `real`. Il contrario non è ammesso.

**Operatori aritmetici** `+ - * /`

| Operando sinistro | Operando destro | Risultato |
|---|---|---|
| integer | integer | integer |
| integer | real | real |
| real | integer | real |
| real | real | real |

La divisione tra due `integer` è divisione intera. Il segno meno unario ha lo stesso tipo dell'operando.

**Operatori di confronto** `== != < <= > >=`

| Operando sinistro | Operando destro | Risultato |
|---|---|---|
| integer o real | integer o real | bool |

Le stringhe non si possono confrontare né usare in operazioni.

### 3.5 Regole di type checking

Notazione: `T(e)` indica il tipo dell'espressione `e`.

- **Costanti:** `INTEGER_CONST` ha tipo integer, `REAL_CONST` ha tipo real, `STRING_CONST` ha tipo stringa.
- **Identificatore:** SE `x` è dichiarato nello scope corrente ALLORA `T(x)` è il suo tipo, ALTRIMENTI errore "identificatore non dichiarato".
- **Operatore aritmetico:** SE `T(e1)` e `T(e2)` sono numerici ALLORA `e1 op e2` ha il tipo dato dalla tabella 3.4, ALTRIMENTI errore di tipo.
- **Confronto:** SE `T(e1)` e `T(e2)` sono numerici ALLORA `e1 op e2` ha tipo bool, ALTRIMENTI errore di tipo.
- **Assegnazione** `x = e;`: SE `x` è dichiarata E (`T(x) = T(e)` OPPURE `T(x)` è real e `T(e)` è integer) ALLORA è corretta, ALTRIMENTI errore di tipo.
- **if / while:** SE `T(condizione)` è bool E i corpi sono corretti ALLORA l'istruzione è corretta, ALTRIMENTI errore di tipo.
- **Chiamata** `f(a1, ..., an)`: SE `f` esiste E ha `n` parametri E ogni `ai` è compatibile con il tipo del parametro i-esimo ALLORA la chiamata è corretta e ha il tipo di ritorno di `f`, ALTRIMENTI errore.
- **Chiamata come istruzione:** ammessa per qualsiasi funzione, l'eventuale valore è scartato. Una funzione senza tipo di ritorno **non** può comparire in un'espressione.
- **return** `return e;`: SE la funzione ha tipo di ritorno `R` E `T(e)` è compatibile con `R` ALLORA è corretto, ALTRIMENTI errore.
- **print(e):** SE `T(e)` è integer, real o stringa ALLORA è corretto, ALTRIMENTI errore. Ogni `print` termina con un a capo.
- **read(x):** SE `x` è dichiarata di tipo integer o real ALLORA è corretto, ALTRIMENTI errore. L'input arriva dalla tastiera.

### 3.6 Errori semantici da segnalare

1. Identificatore non dichiarato.
2. Identificatore dichiarato più volte nello stesso scope.
3. Funzione non definita, oppure `main` assente, duplicata, con parametri o con tipo di ritorno.
4. Errore di tipo in un operatore, in un'assegnazione o in un confronto.
5. Condizione di `if` o `while` non booleana.
6. Numero o tipo di argomenti errato in una chiamata.
7. `return` con espressione in una funzione senza tipo di ritorno, o senza espressione in una funzione con tipo di ritorno.
8. Funzione con tipo di ritorno che non termina con `return`.
9. Funzione senza tipo di ritorno usata in un'espressione.
10. `read` su una variabile non numerica o non dichiarata.
11. Costante intera fuori intervallo.

### 3.7 Esempi semanticamente errati (sintatticamente corretti)

Uso prima della dichiarazione:

```
func main()
    x = 1;
    var x: integer;
endfunc
```

Assegnazione di `real` a `integer`:

```
func main()
    var n: integer;
    n = 2.5;
endfunc
```

Condizione non booleana:

```
func main()
    var n: integer;
    while n do
        n = n - 1;
    endwhile
endfunc
```

Funzione con tipo di ritorno che non termina con `return`:

```
func somma(a: integer, b: integer) -> integer
    print(a + b);
endfunc
```

Operazione su una stringa:

```
func main()
    print("a" + 1);
endfunc
```

## 4. Esempi di programmi

### 4.1 Calcolatrice

Vedi `examples/calcolatrice.al`: menu di scelta, input di interi e reali, calcolo, ciclo di continuazione, tre funzioni (`dividi`, `calcola`, `main`).

### 4.2 Fattoriale

```
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
    print("Inserisci un intero:");
    read(n);
    print(fattoriale(n));
endfunc
```

## 5. Scelte tecniche

1. **Linguaggio di sviluppo:** Python.
2. **Codice target:** LLVM IR, prodotto con llvmlite (senza MLIR). `integer` diventa `i32`, `real` diventa `double`.
3. **Input/output:** tramite `printf` e `scanf` della libreria C, dichiarate nell'IR.
4. **Metodologia:** generatore automatico di parser con Lark (LALR), con la grammatica in `src/grammatica.lark`.
5. **Architettura:** pipeline in fasi successive: parsing, costruzione dell'AST, analisi semantica con tabella dei simboli, generazione dell'IR.
6. **Test:** pytest, con test per ogni fase e un test end-to-end sulla calcolatrice.

## 6. Punti da discutere con il docente

1. L'unico scope per funzione, senza variabili globali, è adeguato?
2. Va bene la promozione implicita da `integer` a `real` e la divisione intera tra interi?
3. È accettabile non avere il tipo stringa dichiarabile né il tipo booleano?
4. L'uso di `printf`/`scanf` per l'I/O nel codice generato è accettabile?

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
| STRING_CONST | testo tra doppi apici | `"Primo numero:"` |

### 1.4 Altre regole lessicali

- Spazi, tab e a capo sono ignorati.
- `main` non è un token a parte: è un normale ID. Che esista una funzione `main` è una regola semantica.

## 2. Specifiche sintattiche

_Da completare._

## 3. Specifiche semantiche

_Da completare._

## 4. Esempi di programmi

Vedi `examples/calcolatrice.al`.

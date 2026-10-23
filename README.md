# Compilatore per un linguaggio imperativo (`.al`)

Progetto del corso di Ingegneria dei Linguaggi di Programmazione (A.A. 2025/26).
Compilatore scritto in Python che traduce programmi `.al` in LLVM IR.

## Requisiti

- Python 3.10 o superiore
- Dipendenze (in `requirements.txt`): `lark`, `llvmlite`, `pytest`

Installazione:

```
pip install -r requirements.txt
```

## Uso

Dalla radice del progetto:

```
python src/main.py examples/calcolatrice.al --run
```

| Comando | Effetto |
|---|---|
| `python src/main.py programma.al` | genera `programma.ll` accanto al sorgente |
| `python src/main.py programma.al -o out.ll` | genera il file `.ll` indicato |
| `python src/main.py programma.al --run` | genera il `.ll` e lo esegue subito |

L'esecuzione con `--run` usa il compilatore JIT di llvmlite. Le istruzioni
`print` e `read` usano `printf` e `scanf` della libreria C del sistema.

In caso di errore sintattico o semantico il compilatore stampa `Errore: ...`
su stderr e termina con codice di uscita 1.

## Test

```
python -m pytest -q
```

I test coprono parser, tabella dei simboli, analisi semantica, generazione del
codice, gli esempi in `examples/` e il test obbligatorio sulla calcolatrice
(`tests/test_calcolatrice.py`), che compila ed esegue il programma con input
simulato.

## Il linguaggio in breve

```
func somma(a: integer, b: integer) -> integer
    return a + b;
endfunc

func main()
    var x: integer;
    read(x);
    if x > 0 then
        print(somma(x, 1));
    else
        print("non positivo");
    endif
endfunc
```

- Tipi: `integer` (32 bit) e `real` (double).
- Istruzioni: dichiarazione `var`, assegnazione `=`, `if/else`, `while`,
  `return`, `print`, `read`, chiamata di funzione.
- Esecuzione da `main`, funzione senza parametri e senza tipo di ritorno.

Specifica completa (lessico, grammatica, semantica) in `docs/specifica.md`.

## Struttura del progetto

```
README.md
requirements.txt
pytest.ini
docs/
    specifica.md          specifiche del linguaggio
examples/
    calcolatrice.al       programma-test con menu, input e ciclo
    fattoriale.al
    fibonacci.al
    numeri_primi.al
    media.al
    errori/               programmi che il compilatore deve rifiutare
src/
    grammatica.lark       grammatica Lark
    ast_nodes.py          nodi dell'albero sintattico
    parser.py             parsing e costruzione dell'AST
    symbol_table.py       tabelle dei simboli
    semantica.py          analisi semantica e type checking
    codegen.py            generazione di LLVM IR
    main.py               riga di comando
tests/
```

## Fasi della compilazione

1. **Parsing:** `grammatica.lark` e `parser.py` trasformano il sorgente in AST.
2. **Analisi semantica:** `semantica.py` controlla dichiarazioni e tipi e scrive
   il tipo di ogni espressione nell'AST.
3. **Generazione del codice:** `codegen.py` produce LLVM IR con llvmlite.

## Esempi

| File | Cosa mostra |
|---|---|
| `calcolatrice.al` | menu, input di interi e reali, ciclo, tre funzioni |
| `fattoriale.al` | funzione con `while` |
| `fibonacci.al` | ricorsione |
| `numeri_primi.al` | funzione con `return` dentro un ciclo, divisione intera |
| `media.al` | variabili reali e conversione da `integer` a `real` |
| `errori/*.al` | un errore sintattico e cinque errori semantici |

## Limiti noti

- Non ci sono commenti, tipo booleano né variabili di tipo stringa.
- Gli interi sono a 32 bit: nessun controllo di overflow a runtime.
- Se l'utente digita un valore non numerico in un `read`, il comportamento
  dipende da `scanf`.

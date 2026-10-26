# Documentazione tecnica

## 1. Panoramica

Il progetto è un compilatore per un piccolo linguaggio imperativo, i cui
sorgenti hanno estensione `.al`. È scritto in Python: legge un programma, ne
verifica la correttezza e genera codice LLVM IR, che si può salvare in un file
`.ll` oppure eseguire subito con il JIT di llvmlite.

Il programma di riferimento è `examples/calcolatrice.al`. Mostra un menu di
quattro operazioni, legge la scelta (un intero) e due operandi (reali), stampa
il risultato e chiede se continuare. Usa tre funzioni, una delle quali ne
chiama un'altra, e ripete il ciclo finché l'utente non risponde di no.

La definizione formale del linguaggio è in `docs/specifica.md`; installazione
e uso sono in `README.md`.

## 2. Il linguaggio

Un programma è una sequenza di funzioni, in qualsiasi ordine. L'esecuzione
parte dalla funzione `main`, che non ha parametri né tipo di ritorno.

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

I tipi sono due: `integer`, intero a 32 bit con segno, e `real`, un double a
64 bit. Le istruzioni sono la dichiarazione di variabile, l'assegnazione,
`if` con `else` facoltativo, `while`, `return`, `print`, `read` e la chiamata
di funzione. Le espressioni usano costanti, variabili, chiamate, gli operatori
`+ - * /`, il meno unario e i confronti `== != < <= > >=`.

Un confronto produce un valore di un tipo interno `bool`, che si può usare
soltanto come condizione di `if` e `while`: non si può dichiarare una
variabile booleana. Analogamente, le stringhe esistono solo come costanti da
passare a `print`.

## 3. Struttura del compilatore

Il compilatore è una pipeline in tre fasi. Ciascuna riceve l'output della
precedente e non sa nulla delle altre: il parser ignora i tipi, il generatore
di codice non ripete i controlli semantici.

```
sorgente .al
    |   parser.py + grammatica.lark
    v
AST
    |   semantica.py + symbol_table.py
    v
AST con il tipo di ogni espressione
    |   codegen.py
    v
LLVM IR (.ll)  -->  esecuzione con il JIT (main.py --run)
```

| Modulo | Contenuto |
|---|---|
| `src/grammatica.lark` | token e grammatica in sintassi Lark |
| `src/ast_nodes.py` | classi dei nodi dell'albero sintattico |
| `src/parser.py` | parsing e costruzione dell'AST |
| `src/symbol_table.py` | tabella delle funzioni, tabella delle variabili, `ErroreSemantico` |
| `src/semantica.py` | analisi semantica e controllo dei tipi |
| `src/codegen.py` | generazione di LLVM IR |
| `src/main.py` | interfaccia a riga di comando |

## 4. Scelte di progetto

### 4.1 Strumenti

Il compilatore è in Python, con llvmlite per costruire l'IR e Lark per il
parsing. llvmlite permette di generare l'IR con un builder invece di
concatenare testo, e di eseguirlo senza installare altri strumenti LLVM. Lark
legge la grammatica da un file, quindi la sintassi del linguaggio resta in un
unico posto leggibile, e segnala riga e colonna degli errori. Si usa il parser
LALR, più veloce di quello Earley di default e sufficiente per questa
grammatica. Non viene prodotto MLIR.

### 4.2 Parsing e AST

Le espressioni sono scritte a livelli: confronto, somma e differenza, prodotto
e quoziente, meno unario, elementi atomici. La precedenza e l'associatività a
sinistra degli operatori seguono dalla struttura della grammatica, senza
dichiarazioni di priorità a parte.

Non ci sono ambiguità da risolvere: `if`, `while` e le funzioni terminano con
`endif`, `endwhile` ed `endfunc`, quindi l'`else` non resta mai "appeso". Le
parole chiave hanno la precedenza sul pattern degli identificatori, ma solo
se coincidono con l'intero lessema: `print` è una parola chiave, `printf` è un
identificatore.

L'albero prodotto da Lark viene convertito in un AST proprio, costituito da
dataclass Python (`ast_nodes.py`). La conversione è fatta da un `Transformer`
in cui ogni metodo prende il nome di una regola della grammatica o di un suo
alias (`add`, `eq`, `var_ref`, ...). I terminali con nome che inizia per `_`
non compaiono nell'albero di Lark, che resta ridotto agli elementi che
servono. Le fasi successive lavorano solo sull'AST e non dipendono da Lark.

Gli operatori binari condividono un solo nodo, `BinOp`, con un campo `op`:
l'analisi dei tipi e il generatore di codice li trattano per gruppi
(aritmetici e di confronto), quindi una classe per operatore avrebbe solo
aumentato il codice. Ogni nodo espressione ha un campo `type`, vuoto dopo il
parsing e riempito dall'analisi semantica: è il modo in cui le informazioni
sui tipi arrivano al generatore di codice.

### 4.3 Analisi semantica

Lo scope è uno solo per funzione. I nomi delle funzioni sono globali,
parametri e variabili locali stanno in un'unica tabella per funzione, i
blocchi di `if` e `while` non introducono scope e non esistono variabili
globali. Bastano quindi due strutture semplici, una tabella globale delle
funzioni e una tabella di variabili creata per ogni funzione analizzata, senza
catene di tabelle.

L'analisi fa due visite. La prima registra tutte le funzioni con firma e tipo
di ritorno, e controlla che esista un solo `main`, senza parametri né tipo di
ritorno. In questo modo una funzione può essere chiamata prima di essere
definita, e la ricorsione funziona. La seconda visita analizza i corpi,
istruzione per istruzione.

Le regole principali sono queste:

- Una variabile va dichiarata prima dell'uso, in ordine testuale, e una sola
  volta per funzione. Alla dichiarazione vale `0` o `0.0`.
- L'unica conversione implicita è da `integer` a `real`. Vale nelle
  operazioni aritmetiche e di confronto, nelle assegnazioni, negli argomenti
  delle chiamate e nei `return`. Il contrario non è ammesso. La divisione tra
  due interi è intera.
- Le condizioni di `if` e `while` devono essere confronti.
- Una funzione con tipo di ritorno deve avere come ultima istruzione del
  corpo un `return` di tipo compatibile. È più restrittivo di un'analisi di
  tutti i cammini di esecuzione, ma si controlla in modo banale e basta per i
  programmi scritti nel linguaggio. Una funzione senza tipo di ritorno può
  usare solo `return;`.
- Una chiamata ha tanti argomenti quanti sono i parametri, ciascuno
  compatibile con il tipo del parametro. Una funzione senza valore di ritorno
  può comparire solo come istruzione, non in un'espressione.
- `print` accetta interi, reali e stringhe; `read` richiede una variabile
  numerica già dichiarata.

Il tipo calcolato per ogni espressione viene scritto nel campo `type` del
nodo. Al primo errore l'analisi si ferma con un `ErroreSemantico` che indica
la funzione e il motivo.

### 4.4 Generazione del codice

**Variabili.** Ogni parametro e ogni variabile locale è una cella di memoria
(`alloca`) creata all'inizio della funzione, e le variabili si leggono e si
scrivono con `load` e `store`. Così non serve costruire la forma SSA a mano.
Prima di generare il corpo, il generatore raccoglie le dichiarazioni di tutta
la funzione, anche quelle dentro `if` e `while`, quindi la cella esiste
sempre; l'istruzione `var` scrive soltanto il valore iniziale.

**Tipi.** `integer` diventa `i32` e `real` diventa `double`. Il campo `type`
dei nodi decide se emettere istruzioni intere (`add`, `sdiv`, `icmp`) o
in virgola mobile (`fadd`, `fdiv`, `fcmp`). Quando un intero deve diventare
reale si usa `sitofp`.

**Funzioni.** La funzione `main` diventa il `main` della libreria C: ha tipo
`i32` e restituisce `0`. Le funzioni senza tipo di ritorno diventano `void`.
Le altre funzioni prendono nell'IR il prefisso `al_`, così un programma può
definire una funzione chiamata `printf` senza entrare in conflitto con quella
della libreria C. Tutte le funzioni vengono dichiarate prima di generarne i
corpi, per permettere chiamate in avanti.

**Controllo di flusso.** `if` e `while` si traducono in blocchi base collegati
da salti condizionali. Dopo un `return` il resto del blocco non viene
generato, per non emettere istruzioni dopo un terminatore. Questo vale anche
per un `return` dentro un ciclo o un ramo di `if`.

**Input e output.** `print` e `read` usano `printf` e `scanf` della libreria C,
dichiarate nel modulo. `print` va sempre a capo. Gli interi si stampano con
`%d`, i reali con `%g` (3.5 diventa `3.5`, 5.0 diventa `5`). Le stringhe sono
passate come argomento di `%s` e non come stringa di formato, così un
carattere `%` nel testo non viene interpretato. `read` usa `%d` per gli interi
e `%lf` per i reali. Le stringhe costanti sono variabili globali, condivise
quando uguali.

**Esecuzione.** Con `--run`, `main.py` verifica il modulo, lo compila con il
JIT di llvmlite ed esegue `main`. Il file `.ll` viene scritto comunque.
Poiché `printf` e `scanf` sono quelle del sistema, l'esecuzione dipende dalla
libreria C della piattaforma.

### 4.5 Gestione degli errori

Un errore di sintassi solleva `ErroreSintattico` con riga e colonna; un errore
semantico solleva `ErroreSemantico` con funzione e motivo. La riga di comando
stampa `Errore: ...` su stderr ed esce con codice 1, senza generare codice.

## 5. Test

I test usano pytest e si lanciano con `python -m pytest -q`; sono 99.

- `test_parser.py` controlla l'AST di programmi validi, la precedenza degli
  operatori, l'associatività e il rifiuto di nove programmi sintatticamente
  errati.
- `test_symbol_table.py` controlla dichiarazione, ricerca e duplicati nelle
  due tabelle.
- `test_semantica.py` controlla programmi corretti, i tipi scritti nei nodi e
  il rifiuto di 24 programmi, uno per ciascuna regola semantica.
- `test_codegen.py` compila ed esegue piccoli programmi: aritmetica intera e
  reale, conversioni, `if`, `while`, `read`, funzioni, ricorsione, `return`
  anticipati, una funzione utente chiamata `printf`, errori da riga di
  comando.
- `test_calcolatrice.py` compila ed esegue `examples/calcolatrice.al` con input
  simulato: singolo calcolo, tutte le operazioni, divisione per zero, ciclo di
  continuazione.
- `test_esempi.py` esegue gli esempi di `examples/` e controlla l'output, e
  verifica che i programmi in `examples/errori/` siano rifiutati con il
  messaggio previsto.

I test di generazione del codice e degli esempi lanciano `main.py` come
processo separato fornendo l'input, quindi provano l'intera catena dal
sorgente all'output del programma.

## 6. Limiti e sviluppi possibili

- Non ci sono commenti, tipo booleano né variabili di tipo stringa.
- Non c'è nessun controllo a runtime su overflow degli interi e divisione
  intera per zero.
- Gli errori semantici non riportano la riga del sorgente e l'analisi si ferma
  al primo errore.
- Un valore non numerico in un `read` non viene gestito: il comportamento è
  quello di `scanf`.
- Il codice generato non è ottimizzato.

Estensioni naturali sarebbero commenti, operatori logici (`&&`, `||`, `!`), un
tipo booleano, array, numeri di riga negli errori semantici e un controllo di
tutti i cammini per i `return`.

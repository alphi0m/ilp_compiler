# Relazione sull'uso dell'AI

## 1. Strumento utilizzato

Abbiamo usato un solo strumento: Claude Fable (Anthropic), nell'interfaccia di
chat web/app, con una conversazione che copre tutto il lavoro, dalla scelta
della proposta alla documentazione. Claude eseguiva il codice nel proprio
ambiente per provare moduli e test prima di consegnarli; quell'ambiente non è
il nostro, quindi ogni risultato è stato poi riprovato in locale.

## 2. Dove e quanto abbiamo usato l'AI

| Fase | Uso dell'AI | Peso | Cosa abbiamo deciso o verificato noi |
|---|---|---|---|
| Scelta della proposta | un'analisi comparativa di fattibilità delle proposte | limitato | la scelta della proposta A e del linguaggio di sviluppo; la valutazione dei rischi per due persone |
| Specifiche del linguaggio | bozze di token, grammatica, regole semantiche, esempi | medio | le scelte di design aperte (`main`, `print`, `else`, confronti, niente booleani, promozione da `integer` a `real`, unico scope) |
| Codice | bozza di ogni modulo, un passo alla volta | alto | la divisione in moduli e l'ordine dei passi; il controllo di ogni modulo con i test; la correzione dei problemi |
| Test | suite scritta insieme a ogni modulo | alto, sistematico | quali casi coprire (esempi aggiuntivi, programmi con errori); esecuzione sulle nostre macchine |
| Documentazione | bozze di README, specifica, documentazione tecnica | medio | contenuti e struttura; riscrittura del testo quando non era adatto |
| Spiegazioni | chiarimenti su concetti e codice | ricorrente | le domande, e il confronto delle risposte con il codice |

**Scelta della proposta.** L'uso è stato limitato: il confronto tra le proposte
è servito a ordinare gli argomenti (carico di lavoro, rischio, difendibilità
del codice), ma la decisione è nostra e l'abbiamo presa sulla base del tempo
disponibile, delle competenze e di quanto ciascuna proposta avremmo potuto
spiegare all'orale.

**Specifiche.** Il linguaggio di un vecchio progetto fornito con il materiale
ci ha dato il formato; le specifiche del nostro linguaggio, più piccolo, sono
partite da una bozza dell'AI, centrata sul programma calcolatrice. Le scelte
elencate in tabella le abbiamo vagliate e confermate noi.

**Codice.** L'AI ha scritto la prima versione di tutti i moduli (grammatica,
nodi dell'AST, parser, tabelle dei simboli, analisi semantica, generatore di
codice, riga di comando). Il lavoro è andato avanti per passi successivi, e
nessun modulo è stato accettato senza averlo eseguito in locale.

**Test.** È la parte in cui l'AI è stata usata in modo più sistematico: ogni
modulo è stato consegnato insieme ai suoi test, e i test sono stati lo
strumento principale con cui abbiamo controllato il resto. In tutto sono 99,
fra parser, tabelle dei simboli, analisi semantica, generazione del codice,
la calcolatrice compilata ed eseguita con input simulato, gli esempi in
`examples/` e i programmi con errori in `examples/errori/`.

**Documentazione e spiegazioni.** Ci siamo fatti spiegare i punti non chiari
(a cosa serve ogni fase, che cosa sono i token, il `Transformer` di Lark,
come il campo `type` collega la semantica al generatore di codice) e abbiamo
usato l'AI per le bozze dei documenti, che poi abbiamo riletto e corretto.

## 3. Metodo di lavoro

Ci siamo dati alcune regole per non limitarci ad accettare l'output:

- **Un passo alla volta.** Un modulo per richiesta, partendo dal programma
  calcolatrice, in modo che un errore si potesse attribuire a un punto preciso.
- **Codice e test insieme.** Ogni modulo è arrivato con i suoi test, da
  lanciare subito con `python -m pytest -q`.
- **Verifica in locale.** Nessun passo è stato dato per concluso finché i
  test non passavano sulle nostre macchine.
- **Le scelte di progetto sono nostre.** Dove c'erano alternative (che
  linguaggio, quali costrutti, quali regole semantiche) abbiamo valutato le
  opzioni e deciso noi, anche riducendo il linguaggio per poterlo spiegare.
- **Domande sul perché.** Quando una scelta non era chiara abbiamo chiesto la
  motivazione, e l'abbiamo confrontata con il codice.
- **Documenti verificati.** README e documentazione tecnica sono stati
  confrontati con il comportamento reale del programma.

## 4. Ripartizione del lavoro

La prima versione dei moduli è stata ottenuta con l'AI. La ripartizione
riguarda chi risponde di ciascuna parte: la studia fino a saperla spiegare e
modificare senza AI, cura i test e la sezione corrispondente della
documentazione, e la fa rivedere all'altro.

| Area | Responsabile | Revisione |
|---|---|---|
| Grammatica (`grammatica.lark`), nodi dell'AST, parser; test del parser | Alfio | Luca |
| Tabelle dei simboli e analisi semantica; test delle due parti | Luca | Alfio |
| Generatore di codice, prima metà: funzioni, variabili, espressioni, conversioni di tipo | Alfio | Luca |
| Generatore di codice, seconda metà: `if`, `while`, `print`, `read`, stringhe, `main.py` ed esecuzione | Luca | Alfio |
| Test di generazione del codice e esempi validi (`fattoriale`, `fibonacci`, `numeri_primi`, `media`) | Alfio | Luca |
| Calcolatrice, test della calcolatrice, esempi con errori in `examples/errori/` | Luca | Alfio |
| Specifica, sezioni 1 e 2 (lessico e sintassi); README | Alfio | Luca |
| Specifica, sezione 3 (semantica); documentazione tecnica | Luca | Alfio |
| Relazione sull'AI e slide | entrambi, una sezione ciascuno | reciproca |

Ogni area ha un responsabile e un revisore; le due metà del generatore di
codice sono divise in modo da coinvolgere entrambi nella parte più delicata.
Le scelte trasversali (il linguaggio, il type system, l'architettura) le
discutiamo insieme.

## 5. Efficacia

L'AI ha reso possibile impostare e portare a termine in circa due settimane
una pipeline completa: parser, analisi semantica, generazione di LLVM IR,
calcolatrice funzionante, esempi, documentazione e 99 test. Partendo da zero
con strumenti nuovi (Lark e llvmlite) avremmo impiegato molto più tempo.
Il codice è risultato nel complesso corretto e ben strutturato, ma non privo
di errori: quelli che abbiamo incontrato sono nella sezione 7, e li ha
trovati soprattutto l'esecuzione dei test.

## 6. Vantaggi

- Tempi molto più brevi per impostare il progetto e arrivare a una versione
  funzionante.
- Struttura coerente: moduli, nomi e test seguono lo stesso schema, e ogni
  fase si può provare da sola.
- Aiuto nel tenere il linguaggio piccolo e il progetto realizzabile nei tempi.
- Spiegazioni sempre disponibili, utili per studiare le parti nuove.
- Documentazione allineata al codice.

## 7. Svantaggi e problemi incontrati

- **Errore di API.** Nel generatore di codice è stata usata una funzione di
  llvmlite che non esiste (`get_default_process_triple`), con 23 test falliti.
  L'ha individuata l'esecuzione dei test prima della consegna, ed è stata
  sostituita con `get_default_triple`.
- **Importazione dei moduli.** Su una delle nostre macchine pytest non trovava
  i moduli di `src/`; il problema non era emerso nell'ambiente dell'AI. Lo
  abbiamo risolto con un `conftest.py` che aggiunge `src/` al percorso.
- **Esempi non validi nella specifica.** Una prima versione degli esempi
  errati usava una sintassi di commento che il linguaggio non prevede; è stata
  corretta.
- **Documento non adatto.** Il primo testo della documentazione tecnica
  conteneva riferimenti fuori luogo e un tono troppo schematico, e l'abbiamo
  fatto riscrivere.
- **Verifica limitata.** L'esecuzione con il JIT di llvmlite e l'uso di
  `printf` e `scanf` dipendono dalla libreria C della piattaforma. È stato
  provato su Linux nell'ambiente dell'AI; non abbiamo verificato altre
  piattaforme.
- **Rischio di accettare senza capire.** L'AI propone soluzioni complete e
  leggibili, ed è facile approvarle in blocco. Per questo abbiamo
  trasformato il controllo in un'attività esplicita (sezione 8).

## 8. Comprensione e responsabilità sul codice

Un codice generato con l'AI è nostro soltanto se sappiamo spiegarlo e
modificarlo senza di essa. Per questo:

- Ciascuno ha studiato i moduli di cui risponde (sezione 4) e li ha spiegati
  all'altro a voce, in particolare le scelte descritte nella sezione 4 della
  documentazione tecnica: perché un solo scope, perché le variabili stanno in
  memoria con `alloca`, come si genera il codice di `if` e `while`, perché le
  stringhe vengono passate a `printf` come argomento.
- Ciascuno ha ripercorso a mano, con il codice davanti, l'esecuzione della
  calcolatrice dal sorgente fino all'IR generato.
- Ci siamo dati esercizi di modifica da svolgere senza AI e controllare con i
  test. Il più completo è l'operatore `%`: richiede un nuovo token e la
  regola di grammatica, il nodo nel parser, il controllo di tipo nella
  semantica e l'istruzione `srem` nel generatore di codice. Altri esercizi:
  aggiungere un controllo semantico (ad esempio il divisore costante pari a
  zero), cambiare il formato di stampa dei reali, aggiungere un caso di test.
- Abbiamo tenuto una lista delle parti che conosciamo meno e le abbiamo
  riprese con l'altro.

## 9. Lezioni apprese 

- Chiedere sempre il codice insieme ai test, ed eseguirli subito sulla propria
  macchina: la verifica nell'ambiente dell'AI non basta.
- I passi piccoli rendono più facile trovare l'origine di un errore.
- Un linguaggio piccolo e ben delimitato è la condizione per poter spiegare e
  modificare ogni riga.
- Le spiegazioni dell'AI vanno riscritte con parole proprie e confrontate con
  il codice, altrimenti non diventano comprensione.
- Le scelte di progetto non si delegano: l'AI propone, noi decidiamo e
  motiviamo.
- Una buona suite di test è lo strumento che permette di usare l'AI con
  fiducia, perché trasforma "sembra giusto" in "funziona".

## 10. Commenti finali

L'AI ci ha permesso di arrivare a un compilatore completo, con test e
documentazione, in un tempo che da soli non avremmo raggiunto, e ci ha dato
una guida costante per entrare in strumenti nuovi. Il valore non sta però nel
codice generato in sé, ma nel modo in cui lo abbiamo controllato: i test come
metro, le scelte di design prese e motivate da noi, e lo studio di ogni
modulo fino a saperlo spiegare. Con un uso meno attento il rischio sarebbe
stato un progetto che funziona ma che non è davvero nostro.
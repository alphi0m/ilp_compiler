func dividi(a: real, b: real) -> real
    if b == 0.0 then
        print("Errore: divisione per zero");
        return 0.0;
    endif
    return a / b;
endfunc

func calcola(op: integer, a: real, b: real) -> real
    if op == 1 then
        return a + b;
    endif
    if op == 2 then
        return a - b;
    endif
    if op == 3 then
        return a * b;
    endif
    return dividi(a, b);
endfunc

func main()
    var scelta: integer;
    var continua: integer;
    var x: real;
    var y: real;

    continua = 1;
    while continua == 1 do
        print("1) Somma 2) Sottrazione 3) Moltiplicazione 4) Divisione");
        read(scelta);
        print("Primo numero:");
        read(x);
        print("Secondo numero:");
        read(y);
        print("Risultato:");
        print(calcola(scelta, x, y));
        print("Continuare? 1 = si, 0 = no");
        read(continua);
    endwhile
endfunc
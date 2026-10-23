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

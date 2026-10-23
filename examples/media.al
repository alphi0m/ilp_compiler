func main()
    var n: integer;
    var i: integer;
    var x: real;
    var somma: real;
    print("Quanti numeri?");
    read(n);
    while i < n do
        print("Numero:");
        read(x);
        somma = somma + x;
        i = i + 1;
    endwhile
    if n > 0 then
        print("Media:");
        print(somma / n);
    endif
endfunc

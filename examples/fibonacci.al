func fib(n: integer) -> integer
    if n < 2 then
        return n;
    endif
    return fib(n - 1) + fib(n - 2);
endfunc

func main()
    var n: integer;
    var i: integer;
    print("Quanti numeri di Fibonacci?");
    read(n);
    while i < n do
        print(fib(i));
        i = i + 1;
    endwhile
endfunc

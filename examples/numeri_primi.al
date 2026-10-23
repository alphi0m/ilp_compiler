func e_primo(n: integer) -> integer
    var d: integer;
    if n < 2 then
        return 0;
    endif
    d = 2;
    while d * d <= n do
        if n - (n / d) * d == 0 then
            return 0;
        endif
        d = d + 1;
    endwhile
    return 1;
endfunc

func main()
    var limite: integer;
    var i: integer;
    print("Numeri primi fino a:");
    read(limite);
    i = 2;
    while i <= limite do
        if e_primo(i) == 1 then
            print(i);
        endif
        i = i + 1;
    endwhile
endfunc

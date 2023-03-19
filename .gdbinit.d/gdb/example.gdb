define adder
    print $arg0 + $arg1 + $arg2
end

document adder
    Example GDB script from https://sourceware.org/gdb/onlinedocs/gdb/Define.html#Define

    adder ONE TWO THREE
        ONE -- first thing to add
        TWO -- second thing to add
        THREE -- third thing to add
end


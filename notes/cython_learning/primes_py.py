def primes_python(nb_primes):
    p = []
    n = 2
    while len(p) < nb_primes:
        # Is n prime?
        for i in p:
            if n % i == 0:
                break
        # If no break occurred in the loop
        else:
            p.append(n)
        n += 1
    return p

# python -m timeit -s "from primes_py import primes_python" "primes_python(1000)"
# python -m timeit -s "from primes import primes" "primes(1000)"
# python -m timeit -s "from primes_py_no import primes_python" "primes_python(1000)"
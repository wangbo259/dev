def cython_sum():
    cdef int i
    cdef long long total = 0  # 使用 long long 类型
    for i in range(1000000):  # 从 1 到 100000
        total += i
    return total
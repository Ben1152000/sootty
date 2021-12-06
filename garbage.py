from functools import reduce
from itertools import compress, accumulate, chain
from more_itertools import run_length

a = [1, 1, 1, 2, 2, 2, 3, 1, 3, 3, 3, 3]

print(list(map(lambda x: (x[0], x[1][1]), filter(lambda x: x[1][0] != x[1][1], enumerate(reduce(lambda x, y: x + [(x.pop(), y), y], a, [None])[:-1])))))

print([0] + list(accumulate(map(lambda x: x[1], run_length.encode(a))))[:-1])

print(reduce(lambda a, b: a if a[-1][1] == b[1] else a + [b], enumerate(a), [(0, a[0])]))

print(list(compress(range(len(a)), map(lambda a: a[0] != a[1], zip([None] + a, a)))))

print(list(compress(range(len(a)), map(lambda a: a[0] != a[1], zip(chain([None], a), a)))))

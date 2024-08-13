def lSysGenerate(s, n):
    for i in range(n):
        s = lSysCompute(s)
    return s

def _lSysCompute(s):
    d = {'A': 'AB'}
    return ''.join([d.get(c) or c for c in s])

def lSysCompute(s):
    new = ''
    for c in s:
        if c == 'A':
            new += 'AB'
        elif c == 'B':
            new += 'A'
    return new

axiom = 'A'
n = 4
print(lSysGenerate(axiom, n))



def plus(a, b):
    return a+b
def minus(a, b):
    return a-b

def calc(ind):
    return funcs[ind](2, 7) == 9
funcs = [plus, minus]
print(calc(0))
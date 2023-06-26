import numpy as num
from . import geometry as gx
from scipy.optimize import minimize, fmin_cobyla


class cornerCases(Exception):
    def __init__(self, value):
        self.tag = value

    def __str__(self):
        return repr(self.tag)


def Norm(x, y, mode='2D'):
    if mode == '2D':
        return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** .5
    elif mode == '3D':
        return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2) ** .5
    else:
        raise cornerCases('Unknown')


def sum_error(x, c, r, mode):
    l = len(c)
    e = 0
    for i in range(l):
        e = e + (Norm(x, c[i].std(), mode=mode) - r[i]) ** 2
    return e


def is_disjoint(cA):
    l = len(cA)
    for i in range(l):
        for j in range(i + 1, l):
            if not cA[j].touch(cA[i]):
                return True
    return False


def lse(cA, mode='2D', cons=True):
    l = len(cA)
    r = [w.r for w in cA]
    c = [w.c for w in cA]
    S = sum(r)
    W = [(S - w) / ((l - 1) * S) for w in r]
    p0 = gx.point(0, 0, 0)  # Initialized point
    for i in range(l):
        p0 = p0 + W[i] * c[i]
    if mode == '2D':
        x0 = num.array([p0.x, p0.y])
    elif mode == '3D':
        x0 = num.array([p0.x, p0.y, p0.z])
    else:
        raise cornerCases('Mode not supported:' + mode)
    if cons:
        if not is_disjoint(cA):
            cL = []
            for q in range(l):
                def ff(x, q=q):
                    return r[q] - Norm(x, c[q].std(), mode=mode)

                cL.append(ff)
            res = fmin_cobyla(sum_error, x0, cL, args=(c, r, mode), consargs=(), rhoend=1e-5)
            ans = res
        else:
            raise cornerCases('Disjoint')
    else:
        res = minimize(sum_error, x0, args=(c, r, mode), method='BFGS')
        ans = res.x
    return gx.point(ans)

import math

# Global
res = 0.0001
s_res = math.pi / 180.0


class geoError(Exception):
    def __init__(self, value):
        self.tag = value

    def __str__(self):
        return repr(self.tag)


class point:
    def __init__(self, *argv):
        l = len(argv)
        if l == 1:
            self.dim = len(argv[0])
        else:
            self.dim = l
        if l == 1:
            self.x = argv[0][0]
            self.y = argv[0][1]
            try:
                self.z = argv[0][2]
            except IndexError:
                self.z = 0.0
        else:
            if l == 2:
                z = 0
            elif l == 3:
                z = argv[2]
            else:
                raise geoError('Input')
            self.x = float(argv[0])
            self.y = float(argv[1])
            self.z = z

    def __str__(self):
        return 'p(' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ')'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __sub__(self, other):
        if isinstance(other, point):
            tx = self.x - other.x
            ty = self.y - other.y
            tz = self.z - other.z
        else:
            tx = self.x - other.dx
            ty = self.y - other.dy
            tz = self.z - other.dz
        return point(tx, ty, tz)

    def __add__(self, other):
        if isinstance(other, point):
            tx = self.x + other.x
            ty = self.y + other.y
            tz = self.z + other.z
        else:
            tx = self.x + other.dx
            ty = self.y + other.dy
            tz = self.z + other.dz
        return point(tx, ty, tz)

    def __mul__(self, other):
        return point(other * self.x, other * self.y, other * self.z)

    def __rmul__(self, other):
        return point(other * self.x, other * self.y, other * self.z)

    def __div__(self, other):
        return point(self.x / other, self.y / other, self.z / other)

    def __neg__(self):
        x = -self.x
        y = -self.y
        z = -self.z
        return point(x, y, z)

    def area(self):
        return 0.0

    def dist(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5

    def std(self):
        if self.dim == 2:
            return [self.x, self.y]
        return [self.x, self.y, self.z]

    def c2s(self):
        R = self.dist(point(0, 0, 0))
        lg = math.atan(self.y / self.x)
        lat = math.acos(self.z / R)
        return (lg, lat, R)

    def transform(self, p, rot):
        px = math.cos(rot) * self.x + math.sin(rot) * self.y
        py = -math.sin(rot) * self.x + math.cos(rot) * self.y
        p_t = point(px, py)
        return p_t - p

    def rot(self, a):
        px = math.cos(a) * self.x - math.sin(a) * self.y
        py = math.sin(a) * self.x + math.cos(a) * self.y
        return point(px, py)

    def angle(self, p):
        v = vec(self, p)
        return v.angle()


class vec:
    def __init__(self, *argv):
        if len(argv) >= 2:
            if isinstance(argv[0], point) and isinstance(argv[1], point):
                p = argv[1] - argv[0]
                self.dx = float(p.x)
                self.dy = float(p.y)
                self.dz = float(p.z)
            else:
                self.dx = float(argv[0])
                self.dy = float(argv[1])
                try:
                    self.dz = float(argv[2])
                except IndexError:
                    self.dz = 0.0
        else:
            p = argv[0]
            self.dx = float(p.x)
            self.dy = float(p.y)
            self.dz = float(p.z)

    def __str__(self):
        return 'vec(' + str(self.dx) + ',' + str(self.dy) + ',' + str(self.dz) + ')'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __sub__(self, other):
        if isinstance(other, vec):
            tx = self.dx - other.dx
            ty = self.dy - other.dy
            tz = self.dz - other.dz
            return vec(tx, ty, tz)
        else:
            tx = self.dx - other.x
            ty = self.dy - other.y
            tz = self.dz - other.z
            return point(tx, ty, tz)

    def __add__(self, other):
        if isinstance(other, vec):
            tx = self.dx + other.dx
            ty = self.dy + other.dy
            tz = self.dz + other.dz
            return vec(tx, ty, tz)
        else:
            tx = self.dx + other.x
            ty = self.dy + other.y
            tz = self.dz + other.z
            return point(tx, ty, tz)

    def __mul__(self, other):
        if isinstance(other, vec):
            return self.cross(other)
        return vec(other * self.dx, other * self.dy, other * self.dz)

    def __rmul__(self, other):
        if isinstance(other, vec):
            return other.cross(self)
        return vec(other * self.dx, other * self.dy, other * self.dz)

    def __div__(self, other):
        return vec(self.dx / other, self.dy / other, self.dz / other)

    def dot(self, v):
        return self.dx * v.dx + self.dy * v.dy + self.dz * v.dz

    def cross(self, v):
        z = self.dx * v.dy - self.dy * v.dx
        x = self.dy * v.dz - self.dz * v.dy
        y = self.dz * v.dx - self.dx * v.dz
        return vec(x, y, z)

    def mag(self):
        return (self.dx ** 2 + self.dy ** 2 + self.dz ** 2) ** 0.5

    def angle(self, *args):
        x = self.dx
        y = self.dy
        z = self.dz

        if len(args) == 0:
            if self.mag() < res:
                return 0.0
            if x >= 0 and y >= 0:
                try:
                    return math.atan(y / x)
                except ZeroDivisionError:
                    return math.pi / 2
            elif x < 0 and y >= 0:
                return math.pi - math.atan(y / abs(x))
            elif x >= 0 and y < 0:
                try:
                    return -math.atan(abs(y) / x)
                except ZeroDivisionError:
                    return -math.pi / 2
            else:
                return math.atan(abs(y) / abs(x)) - math.pi
        elif len(args) == 1:
            b = args[0]
            try:
                rv = math.acos(self.dot(b) / (self.mag() * b.mag()))
                return rv
            except ZeroDivisionError:
                return 0.0

    def rot(self, a):
        dx_t = self.dx * math.cos(a) - self.dy * math.sin(a)
        dy_t = self.dx * math.sin(a) + self.dy * math.cos(a)
        return vec(dx_t, dy_t)

    def norm(self):
        return self / self.mag()

    def floor(self):
        # return to normal vector in the plane normal to the self for
        # Complete coordinate system
        a = self.dx
        b = self.dy
        c = self.dz
        if self.mag() < res:
            raise geoError('ZeroEntity')
        if (abs(a) < res and abs(b) < res):
            return (vec(0, 0, 1), vec(0, 1, 0), vec(1, 0, 0))
        elif (abs(a) < res and abs(c) < res):
            return (vec(0, 1, 0), vec(1, 0, 0), vec(0, 0, 1))
        elif (abs(c) < res and abs(b) < res):
            return (vec(1, 0, 0), vec(0, 1, 0), vec(0, 0, 1))
        else:
            ex = self
            if abs(c) > res:
                q = 0
                w = .5
                e = -w * b / c
                ey = vec(q, w, e)
            else:
                e = 0
                q = .5
                w = -q * a / b
                ey = vec(q, w, e)
            ez = ex.cross(ey)
        return (ex / ex.mag(), ey / ey.mag(), ez / ez.mag())


class circle:
    def __init__(self, p, r):
        self.c = p
        self.r = float(r)

    def __str__(self):
        return 'Circle[' + self.c.__str__() + ',' + str(self.r) + ']'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def touch(self, o):
        d = self.c.dist(o.c)
        met = self.r + o.r
        if d < met + res:
            return True
        else:
            return False

    def side(self, p):
        d = p.dist(self.c)
        r = self.r
        if d < r:
            return 1
        elif d < r + res:
            return 0
        else:
            return -1

class Constraint():
    def __init__(self):
        pass

    def check(self, obj):
        return False
    
class Enum(Constraint):
    def __init__(self, *options):
        self.options = options
    
    def check(self, obj):
        assert obj in self.options, "[Enum] expected {0} to be in {1}".format(str(obj), str(self.options))

class Type(Constraint):
    def __init__(self, typ):
        self.typ =  typ

    def check(self, obj):
        assert isinstance(obj, self.typ), "[Type] expected {0} to have type {1}".format(str(obj), str(self.typ))
            
class Refine(Type):
    def __init__(self, ic, predicate):
        self.ic = ic
        self.predicate = predicate

    def check(self, obj):
        self.ic.check(obj)
        assert self.predicate(obj), "[Refinement] faild for object " + str(obj)    

class Or(Constraint):
    def __init__(self, *cs):
        self.cs = cs

    def check(self, obj):
        passed = False
        for c in self.cs:
            try: 
                c.check(obj)
                passed = True
                break
            except:
                continue
        assert passed, "Could not find a satisfying disjunct for" + str(obj)
    
class Tuple(Constraint):
    def __init__(self, *ics):
        self.ics = ics

    def check(self, objs):
        assert isinstance(objs, tuple)
        for ic, obj in zip(self.ics, objs):
            ic.check(obj)

class List(Constraint):
    def __init__(self, *ic):
        self.ic = Or(ic)

    def check(self, obj):
        assert isinstance(obj, list)
        for o in obj:
            self.ic.check(o)

class And(Constraint):
    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2
    
    def check(self, obj):
        self.c1.check(obj)
        self.c2.check(obj)
        
class Dict(Constraint):
    def __init__(self, **kwargs):
        self.dictic = kwargs

    def check(self,obj):
        assert isinstance(obj, dict), "[Dict] expected dict got " + str(obj)
        for k in obj:
            self.dictic[k].check(obj[k])


class Pair():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PairIC(Constraint):
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def check(self,pair):
        assert pair.x <= self.max
        assert pair.y <= self.max
        assert pair.x >= self.min
        assert pair.y >= self.min

class Whole(Constraint):
    def __init__(self):
        pass

    def check(self, x):
        assert isinstance(x,int)
        assert x > 0


def invert(p):
    assert PairIC(-1,1).check(p)
    p.x = -p.x
    p.y = -p.y
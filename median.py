class InvalidNode(Exception): pass

class Binary(object):
    def __init__(self):
        self._item = None
        self._num = 0
        self._left, self._right = None, None

    def insert(self, _arrival):
        if not self.valid:
            self._item = _arrival
            self._num += 1
            self._left,self._right = self.__class__(),self.__class__()
        else:
            if _arrival < self._item:
                self._left.insert(_arrival)
            else:
                self._right.insert(_arrival)

    def __cmp__(self, _other):
        return cmp(self._item, _other._item)

    @property
    def min(self):
        if not self.valid: raise InvalidNode()
        if self.left and self.left.valid:
            return self.left.min
        return self._item

    @property
    def max(self):
        if not self.valid: raise InvalidNode()
        if self.right and self.right.valid:
            return self.right.max
        return self._item

    @property
    def get(self):
        return self._item

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def valid(self):
        return self._item is not None

    @property
    def num(self):
        if self._item is not None:
            return self._num + self._left.num + self._right.num
        else:
            return 0

    @property
    def list(self):
        if self.valid:
            return self.left.list+[self._item]+self.right.list
        return []

    def __str__(self):
        if self.valid:
            return " ".join([str(self._left),str(self._item),str(self._right)])
        else:
            return ""


class Median(Binary):
    def leftmax(self):
        if self.left.valid:
            return self.left.max
        return self._item

    def rightmin(self):
        if self.right.valid:
            return self.right.min
        return self._item

    def median(self, _left=0, _right=0, _prev=None):
        lsum,rsum = (self.left.num + _left, self.right.num + _right)
        diff  = lsum - rsum
        if diff == 0:
            child,dl,dr,msg = (self.left,_left,rsum+1,"found")
        if diff < 0:
            child,dl,dr,msg = (self.right,lsum+1,_right, "move right")
            comp = min
        if diff > 0:
            child,dl,dr,msg = (self.left,_left,rsum+1,"move left")
            comp = max

        if diff == 0: # balanced on both sides, we've found the exact median
            child,dl,dr,msg = (self.left,_left,rsum+1,"found")
            return self._item

        if abs(diff) == 1:
            others = ([child.min]) if child._item >= self._item else ([child.max])
            if _prev:
                if diff < 0 and _prev > self:
                    others.append(_prev.rightmin())
                if diff > 0 and _prev <= self:
                    others.append(_prev.leftmax())

            return 0.5*(self._item + comp(others))

        return child.median(dl, dr, self)

from random import randint, seed
from time import time

def run():
    seed(time())
    tree = Median()
    orig = [randint(0,100)for i in xrange(randint(10,21))]
    for num in orig:
        num = randint(0,100)
        tree.insert(num)

    return (orig, tree.list, tree.median() )

def main():
    def lmedian(_list):
        n = len(_list)
        if (n%2)==0:
            return 0.5 * (_list[n/2] + _list[n/2 -1])
        else:
            return _list[n/2]
    for x in xrange(3000):
        orig,tlist,median = run()
        if float(lmedian(tlist))!=float(median):
            print "FAIL:", median,tlist,lmedian(tlist)

if __name__ == '__main__':
    main()

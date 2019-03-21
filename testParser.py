import unittest
from parser import Formula

text = """\
(a)	a
a	a
X(a)	Xa
-G(a)	F-a
-F(True->False)	G(True&True)
-(a&G(b->c))	(-a|F(b&-c))
-(a|b)	(-a&-b)
(a1Ub1)	(a1Ub1)
False & True & -False -> True	(True|(False|False))|True
a&b|c->d	((-a|-b)&-c)|d
-G(-(a&b&c)->d)	F((-a|(-b|-c))&-d)
False & True & ( -False -> True)	False&True&(False|True)
(XFa -> b)	(XG-a|b)
FXa	FXa
-------True	False
-a	-a
-(G(((b))))	F-b
X-(F(a)&-(Gb))	X(G-a|Gb)
-aU(-Gb)	-aUF-b
a|bRc|d	a|bRc|d
a|(b&c)|d	a|(b&c)|d
a&G(a1 -> (-X(-a2) U (-a3)))	a&G(-a1|(Xa2U-a3))
b|G(a2 -> ((-a1) R -G(-a3)))	b|G(-a2|(-a1RFa3))
G(a3 -> (-F(-a1) & -X(-a2)))	G(-a3|(Ga1&Xa2))
aU-G(b  -> ((-a1)  & ((-a2)  & (-a3))))	aUF(b&(a1|(a2|a3)))
G(-a2->-Xe)	G(a2|X-e)
a|b|c|d|e|f->g|h|i	(-a&(-b&(-c&(-d&(-e&-f)))))|g|h|i
(a|b)&(c|d)&e|f->g|h|i	(((-a&-b)|((-c&-d)|-e))&-f)|g|h|i
a|-X(a1 | ((X-(a2)) | (-X(b))))	a|X(-a1&(Xa2&Xb))
GaU(a2 -> ((X(a3)) U (X(b))))	GaU(-a2|(Xa3UXb))
-X(a3 -> ((-X(a1)) R (-X(b))))	X(a3&(Xa1UXb))
G(b  -> (X(b)))	G(-b|Xb)
a1 & (G(a1 -> (X(F(a3)))))	a1&G(-a1|XFa3)
-G(a1 U ((-Fa2) & (-Xa3)))	F(-a1R(Fa2|Xa3))
G(a2 -> -((-Xa1) U (-Ga3)))	G(-a2|(Xa1RGa3))
G(a3 R ((-a1) R (-Ga2)))	G(a3R(-a1RF-a2))
G(b  -> -((-a1)  & ((-a2)  & (-a3))))	G(-b|(a1|(a2|a3)))
-G(-a2)	Fa2
-(a|G(a1 -> -X((X(a2)) | -(F(b)))))	(-a&F(a1&X(Xa2|G-b)))
-G(a2 -> ((X(a3)) | F(G(b))))	F(a2&(X-a3&GF-b))
G(a3 -> ((X(a1)) -> (X(b))))	G(-a3|(X-a1|Xb))
-(aRG(b  -> (X(b))))	(-aUF(b&X-b))
a1 & -(G(a1 -> (X(F(a3)))))	a1&F(a1&XG-a3)
"""

class TestParser(unittest.TestCase):
    def testNnf(self):
   	for line in text.splitlines():
			[f,nnf] = line.split("\t")
			self.assertEqual(Formula(f).nnf(), nnf)

unittest.main(argv=['-v'], exit=False)

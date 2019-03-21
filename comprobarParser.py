from parser import Formula

text = """\
---False
(a)
X(a)
-G(a)
a1&F(a1&XG-a3)
-F(True->False)
-(a&G(b->c))
-(a|b)
(a1Ub1)
False & True & -False -> True
a&b|c->d
-G(-(a&b&c)->d)
False & True & ( -False -> True)
(XFa -> b)
FXa
-------True
-a
-(G(((b))))
X-(F(a)&-(Gb))
-aU(-Gb)
a|bRc|d
a|(b&c)|d
a&G(a1 -> (-X(-a2) U (-a3)))
b|G(a2 -> ((-a1) R -G(-a3)))
G(a3 -> (-F(-a1) & -X(-a2)))
aU-G(b  -> ((-a1)  & ((-a2)  & (-a3))))
G(-a2->-Xe)
a|b|c|d|e|f->g|h|i
(a|b)&(c|d)&e|f->g|h|i
a|-X(a1 | ((X-(a2)) | (-X(b))))
GaU(a2 -> ((X(a3)) U (X(b))))
-X(a3 -> ((-X(a1)) R (-X(b))))
G(b  -> (X(b)))
a1 & (G(a1 -> (X(F(a3)))))
-G(a1 U ((-Fa2) & (-Xa3)))
G(a2 -> -((-Xa1) U (-Ga3)))
G(a3 R ((-a1) R (-Ga2)))
G(b  -> -((-a1)  & ((-a2)  & (-a3))))
-G(-a2)
-(a|G(a1 -> -X((X(a2)) | -(F(b)))))
-G(a2 -> ((X(a3)) | F(G(b))))
G(a3 -> ((X(a1)) -> (X(b))))
-(aRG(b  -> (X(b))))
a1 & -(G(a1 -> (X(F(a3)))))
"""

for line in text.splitlines():
    f=Formula(line)
    if f.isValid:
        print f.text, "\t", f.nnf()
    else:
        print("No valid expression: " + str(f))


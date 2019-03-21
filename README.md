# mal
MAL son las siglas en euskera de TFM


Ejemplos de uso de la clase Formula incluida en el archivo Parser.py

>>> from parser import Formula
>>> f=Formula("a1 & (G(a1 -> (X(F(a3)))))")
>>> print f.no()
-(a1 & (G(a1 -> (X(F(a3))))))
>>> print f.nnf()
a1&G(-a1|XFa3)
>>> print f.no().nnf()
(-a1|F(a1&XG-a3))

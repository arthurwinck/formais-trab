class Nodo:
    CONCAT = '.'
    OR = '+'
    FECHO = '*'
    FOLHA = None

    TIPOS_OPERACAO = [CONCAT, OR, FECHO, FOLHA]

    def __init__(self, c1, c2, simbolo, tipo):
        self.c1 = c1
        self.c2 = c2
        self.simbolo = simbolo
        self.tipo = tipo
        self.index = None

    @property
    def verificarSeEFolha(self):
        return self.c1 is None and self.c2 is None

    @property
    def anulavel(self):
        if self.simbolo == '&':
            return True
        elif self.verificarSeEFolha:
            return False
        elif self.tipo == Nodo.CONCAT:
            return self.c1.anulavel and self.c2.anulavel
        elif self.tipo == Nodo.OR:
            return self.c1.anulavel or self.c2.anulavel
        elif self.tipo == Nodo.FECHO:
            return True

    @property
    def firstpos(self):
        if self.simbolo == '&':
            return set()
        elif self.verificarSeEFolha:
            return {self.index}
        elif self.tipo == self.CONCAT:
            if self.c1.anulavel:
                return self.c1.firstpos.union(self.c2.firstpos)
            else:
                return self.c1.firstpos
        elif self.tipo == self.OR:
            return self.c1.firstpos.union(self.c2.firstpos)
        elif self.tipo == self.FECHO:
            return self.c1.firstpos

    @property
    def lastpos(self):
        if self.simbolo == '&':
            return set()

        elif self.verificarSeEFolha:
            return {self.index}

        elif self.tipo == self.CONCAT:
            if self.c2.anulavel:
                return self.c1.lastpos.union(self.c2.secondpos)

            else:
                return self.c2.lastpos

        elif self.tipo == self.OR:
            return self.c1.lastpos.union(self.c2.secondpos)

        elif self.tipo == self.FECHO:
            return self.c2.lastpos

    def criarIndex(self, index):
        if not self.verificarSeEFolha and self.tipo != self.FECHO:
            index = self.c1.criarIndex(index)
            index = self.c2.criarIndex(index)

        elif self.tipo == self.FECHO:
            index = self.c1.criarIndex(index)

        else:
            self.index = index
            index += 1

        return index

    def pegarAlfabeto(self, alfabeto=None) -> set:
        if alfabeto is None:
            alfabeto = set()

        if self.verificarSeEFolha:
            if self.simbolo != '#':
                alfabeto.add(self.simbolo)

        else:
            alfabeto = self.c1.pegarAlfabeto(alfabeto)
            alfabeto = self.c2.pegarAlfabeto(alfabeto)

        return alfabeto

    def pegarCorrespondentes(self, correspondentes=None):
        if correspondentes is None:
            correspondentes = dict()

        if self.verificarSeEFolha:
            correspondentes[self.index] = self.simbolo

        else:
            correspondentes = self.c1.pegarCorrespondentes(correspondentes)
            correspondentes = self.c1.pegarCorrespondentes(correspondentes)

        return correspondentes


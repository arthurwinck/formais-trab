from .Tipos import TipoArquivo, Elemento
from model.Nodo import Nodo
from .AutomatoFinito import AutomatoFinito


class ExpressaoRegular(Elemento):
    def __init__(self, alfabeto, expressao) -> None:
        super().__init__(TipoArquivo.ER)
        self.alfabeto = alfabeto
        self.expressao = expressao
        self.dicionario_operacoes = {
            '*': Nodo.FECHO,
            '+': Nodo.OR,
            '.': Nodo.CONCAT
        }
        self.tipos = ['*', '+', '.']
        self.raiz = self.parser(self.expressao + ".#")
        indexMaximo = self.raiz.criarIndex(1)

        self.indexes = [i for i in range(1, indexMaximo)]
        self.alfabeto = list(self.raiz.pegarAlfabeto())
        self.alfabeto.sort()
        self.correspondentes = self.raiz.pegarCorrespondentes()

    def parser(self, expressao):
        if len(expressao) == 1:
            return Nodo(None, None, Nodo.FOLHA, expressao)

        if expressao[-1] == '*':
            esquerda, tipo, direita = self.pegarRamos(expressao[:-1])
            c2 = self.parser(direita)
            if esquerda is None:
                return Nodo(c2, c2, Nodo.FECHO, None)
            else:
                c1 = self.parser(esquerda)

            fecho = Nodo(c2, c2, Nodo.FECHO, None)
            return Nodo(c1, fecho, tipo, None)

        else:
            esquerda, tipo, direita = self.pegarRamos(expressao)
            while esquerda is None:
                esquerda, tipo, direita = self.pegarRamos(direita)

            c1 = self.parser(esquerda)
            c2 = self.parser(direita)

            return Nodo(c1, c2, tipo, None)

    def pegarRamos(self, expressao):
        if expressao[-1] == ')':
            pilha = ['(']
            index = -1
            while len(pilha) > 0:
                index -= 1
                if expressao[index] == pilha[-1]:
                    pilha.pop()
                elif expressao[index] == ')':
                    pilha.append('(')

            if len(expressao) is - index:
                return None, None, expressao[1:-1]
            else:
                return expressao[:index - 1], expressao[index - 1], expressao[index + 1: -1]

        else:
            return expressao[:-2], expressao[-2], expressao[-1]

    def pegarFollowpos(self, nodo: Nodo, followpos: dict) -> dict:
        if nodo.verificarSeEFolha:
            return followpos

        if nodo.tipo == Nodo.FECHO:
            for i in nodo.firstpos:
                followpos[i] = followpos[i].union(nodo.lastpos)

        elif nodo.tipo == Nodo.FECHO:
            for i in nodo.c1.lastpos:
                followpos[i] = followpos[i].union(nodo.c2.lastpos)

        followpos = self.pegarFollowpos(nodo.c1, followpos)
        followpos = self.pegarFollowpos(nodo.c2, followpos)

        return followpos

    def expressaoRegularParaAutomatoFinito(self) -> AutomatoFinito:
        followpos = {i: set() for i in self.indexes}

        followpos = self.pegarFollowpos(self.raiz, followpos)

        estadoInicial = str(self.raiz.firstpos)
        estadosDeAceitacao = []
        dEstadosNaoMarcados = [self.raiz.firstpos]
        dEstadosMarcados = []
        dTransicoes = []

        while dEstadosNaoMarcados:
            S = dEstadosMarcados.pop(0)
            dEstadosMarcados.append(S)
            for i in self.alfabeto:
                U = set()
                for j in S:
                    if self.correspondentes[j] == i:
                        fp = followpos[j]
                        U = U.union(fp)

                    if U and U not in dEstadosMarcados:
                        dEstadosNaoMarcados.append(U)
                    n = {'Estado': S, 'Simbolo': i, 'Próximo': U}
                    if U and n not in dTransicoes:
                        if max(self.indexes) in n['Estado'] and str(n['Estado']) not in estadosDeAceitacao:
                            estadosDeAceitacao.append(str(n['Estado']))
                        dTransicoes.append(n)

                transicoes = {}
                for t in dTransicoes:
                    if str(t['Estado']) not in transicoes.keys():
                        transicoes[str(t['Estado'])] = {}
                    transicoes[str(t['Estado'])][str(t['Símbolo'])] = str(t['Próximo'])

                alfabeto = self.alfabeto

                novasTransicoes = {}
                for k in transicoes.keys():
                    t = transicoes[k]
                    n_t = []
                    for a in alfabeto:
                        if a in t.keys():
                            n_t.append(t[a])
                        else:
                            n_t.append('V')

                    novasTransicoes[k] = n_t

                return AutomatoFinito(estados=novasTransicoes.keys(),
                                      alfabeto=alfabeto,
                                      estado_inicial=estadoInicial,
                                      estados_aceitacao=estadosDeAceitacao,
                                      transicoes=novasTransicoes)


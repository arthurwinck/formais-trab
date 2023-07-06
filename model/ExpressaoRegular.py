from .Tipos import TipoArquivo, Elemento
from .Nodo import Nodo
from .Tipos import SimbolosArvore as SIMBOLO

class ExpressaoRegular(Elemento):
    def __init__(self, alfabeto, expressao) -> None:
        super().__init__(TipoArquivo.ER)
        self.alfabeto = alfabeto
        self.expressao = expressao
        # Passamos a expressão adicionando o símbolo para finalizar expressão
        # para descobrirmos a raíz
        self.raiz = None
        self.indices = None
        self.correspondentes = None
        self.inicializarVariaveis(expressao)

    def inicializarVariaveis(self, expressao):
        self.raiz = self.parse(self.expressao + '.#')
        indiceMaximo = self.raiz.criarIndice(1)
        self.indices = [i for i in range(1, indiceMaximo)]
        self.alfabeto = list(self.raiz.pegarAlfabeto())
        self.alfabeto.sort()
        self.correspondentes = self.raiz.pegarCorrespondentes()


    def parse(self, expressao: str) -> Nodo:
        if len(expressao) == 0:
            return Nodo(None, None, SIMBOLO.FOLHA, expressao)
           
        # Caso seja um nodo estrela 
        if expressao[-1] == SIMBOLO.STAR:
            esquerda, tipo, direita = self.pegarRamos(expressao[:-1])
            filho2 = self.parse(direita)

            if esquerda is None:
                return Nodo(filho2, filho2, SIMBOLO.STAR, None)
            else:
                filho1 = self.parse(esquerda)

            # Criamos o nodo estrela a partir dos dois filhos criados
            estrela = Nodo(filho1, filho2, SIMBOLO.STAR, None)
            return Nodo(filho1, SIMBOLO.STAR, tipo, None)
        
    # Pegar ramos retorna o ramo da esquerda, o símbolo que relaciona os dois (pai dos dois)
    # e o ramo da direita
    def pegarRamos(self, expressao) -> tuple:
        if expressao[-1] == ')':
            pilha = ['(']
            i -= 1
            while len(pilha) > 0:
                i -= 1
                if expressao[i] == pilha[-1]:
                    pilha.pop()

                elif expressao[i] == ')':
                    pilha.append('(')

            # So existe ramo da direita
            if len(expressao) is - i:
                return None, None, expressao[1:-1]

            else:
                return expressao[:i-1], expressao[i-1], expressao[i+1: -1]

        
        else:
            # Caso contrário, só pega o símbolo e retorna como
            # o ramo da direita
            return expressao[:-2], expressao[-2], expressao[-1]
        
    def converterParaAFD(self):
        followPos = self.criarFollowPos(self.raiz, {i: set() for i in self.indices})

        estadoInicial = str(self.raiz.firstPos())
        estadosAceitacao = []
        estadosNaoMarcados = [self.raiz.firstPos()]
        estadosMarcados = []
        transicoes = []

        while estadosNaoMarcados:
            estadoAtual = estadosNaoMarcados.pop(0)
            estadosMarcados.append(estadoAtual)

            for simbolo in self.alfabeto:
                setNext = set()
                for firstPosItems in estadoAtual:
                    if self.correspondentes[firstPosItems] == simbolo:
                        followPosTemp = followPos[firstPosItems]
                        setNext = setNext.union(followPosTemp)


                if setNext and setNext not in estadosMarcados:
                    estadosNaoMarcados.append(setNext)

                tuplaEstado = {'estado': estadoAtual, 'simbolo': simbolo, 'next': setNext}
                if setNext and tuplaEstado not in transicoes:
                    if max(self.indices) in tuplaEstado['estado'] and str(tuplaEstado['estado']) not in estadosAceitacao:
                        estadosAceitacao.append(str(tuplaEstado['estado']))
                    transicoes.append(tuplaEstado)

        novasTransicoes = {}
        
        for tuplaEstado in transicoes:
            if str(tuplaEstado['estado']) not in novasTransicoes.keys():
                novasTransicoes[str(tuplaEstado['estado'])] = {}
            novasTransicoes[str(tuplaEstado['estado'])][str(tuplaEstado['simbolo'])] = str(tuplaEstado['next'])

        transicoesFinais = []

        for estado in novasTransicoes.keys():
            transicao = novasTransicoes[estado]

            for simbolo in self.alfabeto:
                if simbolo in transicao.keys():
                    transicoesFinais = f"{estado} {transicao[simbolo]} {simbolo}"

        print(transicoesFinais)

    def criarFollowPos(self, nodo, followPosDict: dict):
        if nodo.isFolha():
            return followPosDict
        if nodo.tipo == SIMBOLO.STAR:
            for pos in nodo.firstPos():
                followPosDict[pos] = followPosDict[pos].union(nodo.secondPos())
        elif nodo.tipo == SIMBOLO.CAT:
            for pos in nodo.filho1.secondPos():
                followPosDict[pos] = followPosDict[pos].union(nodo.filho2.firstPos())

        return self.criarFollowPos(nodo.filho2, self.criarFollowPos(nodo.filho1, followPosDict))
    

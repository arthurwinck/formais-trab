from .Tipos import TipoArquivo, Elemento
from .AutomatoFinito import AutomatoFinito

class GramaticaRegular(Elemento):
    def __init__(self, nao_terminais, terminais, producoes, simbolo_inicial) -> None:
        super().__init__(TipoArquivo.GR)    
        self.nao_terminais = nao_terminais
        self.terminais = terminais
        self.producoes = self.arrumarProducoes(producoes)
        self.simbolo_inicial = simbolo_inicial

    def arrumarProducoes(self, producoes: list) -> dict:
        if isinstance(producoes, dict):
            return producoes
        
        dictProducoes = {}
        
        for producao in producoes:
            listaProducao = producao.split("->")

            if listaProducao[0] not in dictProducoes.keys():
                dictProducoes[listaProducao[0]] = [listaProducao[1]]
            else:
                dictProducoes[listaProducao[0]].append(listaProducao[1])

        print(dictProducoes)
        return dictProducoes
    
    def converterParaAutomato(self):
        # estados
        #self.printar()
        estados = list(self.nao_terminais)
        novoSimboloNaoTerminal = 'Z'
        estados.append(novoSimboloNaoTerminal)

        # alfabeto
        alfabeto = self.terminais

        estadoInicial = self.simbolo_inicial

        estadosAceitacao = [novoSimboloNaoTerminal]

        for naoTerminal, producao in self.producoes.items():
            if naoTerminal == self.simbolo_inicial and '&' in producao:
                estadosAceitacao.append(naoTerminal)
                break

        transicoes = {}

        for naoTerminal, listaProducao in self.producoes.items():
            for producao in listaProducao:
                terminalProd, naoTerminalProd, epsilon = self.pegarSimbolos(producao)

                if not epsilon:
                    
                    if (naoTerminal, terminalProd) not in transicoes.keys():
                        transicoes[(naoTerminal, terminalProd)] = []
                    
                    if naoTerminalProd is None:
                        transicoes[(naoTerminal, terminalProd)].append(novoSimboloNaoTerminal)

                    if naoTerminalProd is not None and naoTerminalProd is not None:
                        transicoes[(naoTerminal, terminalProd)].append(naoTerminalProd)

        listaTransicoes = []
        for tuplaSimbolo, listaDestinos in transicoes.items():
            for destino in listaDestinos:
                listaTransicoes.append(f"{tuplaSimbolo[0]} {destino} {tuplaSimbolo[1]}")

        return AutomatoFinito(
            estados, alfabeto, listaTransicoes, [estadoInicial], estadosAceitacao)

    def pegarSimbolos(self, producao: str, epsilon = False) -> tuple:        
        terminal = None
        naoTerminal = None

        for simbolo in producao:
            if simbolo in self.terminais:
                terminal = simbolo
                break
        
        for simbolo in producao:
            if simbolo in self.nao_terminais:
                naoTerminal = simbolo
                break
        
        if '&' in producao:
            epsilon = True
        
        return terminal, naoTerminal, epsilon
        
    def printar(self):
        print(f"self.nao_terminais: {self.nao_terminais}")
        print(f"self.terminais: {self.terminais}")
        print(f"self.producoes: {self.producoes}")
        print(f"self.simbolo_inicial: {self.simbolo_inicial}")
        
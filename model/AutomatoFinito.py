from .Tipos import TipoArquivo, Tipo
from .Automato import Automato

class AutomatoFinito(Automato):
    def __init__(self, estados=None, alfabeto=None, transicoes=None, estado_inicial=None, estados_aceitacao=None) -> None:
        super().__init__(TipoArquivo.AF, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)
 
    def determinizar(self):
        transicoesAntigas = self.transicoes.copy()
        estadosAntigos = self.estados.copy()

        # eFechoEstadoInicial = self.checarEFechoEstadoInicial(transicoesAntigas)

        dicEstadosEFecho = self.calcularEFecho(transicoesAntigas)
        self.estados = [dicEstadosEFecho[self.estado_inicial]]
        self.estado_inicial = dicEstadosEFecho[self.estado_inicial]

        self.calcularNovasTransicoes(self.estado_inicial, transicoesAntigas, estadosAntigos, dicEstadosEFecho)
        #self.transicoes = novasTransicoes

        self.checarEstadoFinal()
        self.printar()

    def calcularEFecho(self, transicoes: list[list]) -> dict:
        dicEstadosEFecho = {}
        for estado in self.estados:
            listaTransicoesEFecho = self.getEstadosTransicoesEFecho(self.getPos(estado), transicoes)
            dicEstadosEFecho[estado] = listaTransicoesEFecho
        
        return dicEstadosEFecho

    def checarEFechoEstadoInicial(self, transicoes: list[list]) -> str:
        if '&' in transicoes[self.getPos(self.estado_inicial)]:
            novoEstadoInicial = self.getEstadosTransicoesEFecho(self.getPos(self.estado_inicial), transicoes)
            print(novoEstadoInicial)
            return self.packSimbolos(novoEstadoInicial)
        else:
            return self.estado_inicial

    def getEstadosTransicoesEFecho(self, estado: int, transicoes: list[list]) -> str:
        transicoesEFecho = [self.getElement(estado)]
        filaProxEstado = []

        # Buscar por todos os estados alcançaveis por transições & 
        while True:
            for i in range(len(transicoes[estado])):
                if '&' in transicoes[estado][i] and self.getElement(i) not in transicoesEFecho:
                    transicoesEFecho.append(self.getElement(i))
                    filaProxEstado.append(i)

            try:
                estado = filaProxEstado.pop()
            except IndexError:
                break

        return self.packSimbolos(transicoesEFecho)

    def calcularNovasTransicoes(self, novoEstadoInicial: str, transicoes: list[list], estados: list[str], dicEstadosEFecho: dict) -> None:
        # Lista de novos estados. Cada novo estado é uma lista
        self.transicoes = [['']]
        listaEstadosAlcancados = [novoEstadoInicial]
        filaEstados = [novoEstadoInicial]
        
        # Percorre todas as transições dos estados pelo mesmo símbolos
        # transição por x:
        #   estado a -x-> b
        #   estado b -x-> c
        #   estado c -x-> c
        # novo estado: a,b,c -> colocar esse estado na fila para mesmo método

        while True:
            try:
                estado = filaEstados.pop()
                estado = dicEstadosEFecho[estado]
            except IndexError:
                self.log("calcularNovasTransicoes", "Acabaram os estados da fila")
                break
            except KeyError:
                self.log("calcularNovasTransicoes", f"Não foi possível encontrar estado fecho de {estado}")
                pass
            
            for simbolo in self.alfabeto:
                estadoAlcancavel = self.getEstadoAlcancavel(estado, transicoes, simbolo, estados)

                try:
                    estadoAlcancavel = dicEstadosEFecho[estadoAlcancavel]
                except KeyError:
                    self.log("calcularNovasTransicoes", f"Não foi possível encontrar estado fecho de {estadoAlcancavel}")
                    pass

                if estadoAlcancavel != '':
                    if estadoAlcancavel not in listaEstadosAlcancados:
                        listaEstadosAlcancados.append(estadoAlcancavel)
                        filaEstados.append(estadoAlcancavel)

                    if estadoAlcancavel not in self.estados:
                        self.addEstado(estadoAlcancavel)
                        self.log("calcularNovasTransicoes", f"Adicionando novo estado: {estadoAlcancavel}")
                    
                    self.marcarTransicao(estado, estadoAlcancavel, simbolo)

        
    def addEstado(self, estado: str) -> None:
        for i in range(len(self.estados)):
            self.transicoes[i].append('')

        self.estados.append(self.packSimbolos(estado))
        self.transicoes.append(['']*len(self.estados))
    
    def marcarTransicao(self, estado: str, estadoAlcancavel: str, simbolo: str) -> None:
        try:
            transicaoExistente = self.transicoes[self.getPos(estado)][self.getPos(estadoAlcancavel)] 
            
            if transicaoExistente == '':
                self.transicoes[self.getPos(estado)][self.getPos(estadoAlcancavel)] = simbolo
            else:
                listaTransicaoExistente = self.appendIfNotExists(self.unpackSimbolos(transicaoExistente), simbolo)
                listaTransicaoExistente.sort()
                
                self.transicoes[self.getPos(estado)][self.getPos(estadoAlcancavel)] = self.packSimbolos(listaTransicaoExistente)

        except IndexError:
            self.log("marcarTransicao", f"Erro de índice ao tentar acessar {estado} ou {estadoAlcancavel}")
    
    def getEstadoAlcancavel(self, estadoOrigem: str, transicoes: list[list], simbolo: str, listaEstados: list[str]) -> str:
        setEstadoAlcancavel = set()
        parteEstados = self.unpackSimbolos(estadoOrigem) 
        
        for estado in parteEstados:
            for i in range(len(listaEstados)):
                transicao = transicoes[self.getPosLista(estado, listaEstados)][i]

                if simbolo in self.unpackSimbolos(transicao) and simbolo != '':
                    setEstadoAlcancavel.add(self.getElementLista(i, listaEstados))

        listaEstadoAlcancavel = list(setEstadoAlcancavel)
        listaEstadoAlcancavel.sort()

        return self.packSimbolos(listaEstadoAlcancavel)

    def checarEstadoFinal(self):
        for estado in self.estados:
            listaEstado = self.unpackSimbolos(estado)

            for parteEstado in listaEstado:
                if parteEstado in self.estados_aceitacao and estado not in self.estados_aceitacao:
                    self.estados_aceitacao.append(estado)

    def minimizar(self) -> None:
        self.removerInalcancaveis()
        print(f"transições por s: {self.transicoes[self.getPos('s')]}")
        self.removerMortos()
        print(f"transições por s: {self.transicoes[self.getPos('s')]}")

    def removerInalcancaveis(self) -> None:
        alcancaveis = [self.estado_inicial]

        while True:
            mudanca = False

            for estado in alcancaveis:
                novosAlcancaveis = []
                transicoes = self.transicoes[self.getPos(estado)]

                for estadoDestino, simboloTransicao in enumerate(transicoes):
                    if simboloTransicao != '' and self.getElement(estadoDestino) not in alcancaveis and self.getElement(estadoDestino) not in novosAlcancaveis:
                        mudanca = True
                        novosAlcancaveis.append(self.getElement(estadoDestino))

                alcancaveis.extend(novosAlcancaveis)

            if not mudanca:
                break
        
        #Não sei porque mas dar sort nos alcancaveis dá erro. So é necessário dar sort nos mortos
        #alcancaveis.sort()
        self.atualizarEstadosETransicoes(alcancaveis)

    def removerMortos(self) -> None:
        vivos = self.estados_aceitacao

        while True:
            mudanca = False

            for estado in self.estados:
                novosVivos = []
                transicoes = self.transicoes[self.getPos(estado)]

                for estadoDestino, simboloTransicao in enumerate(transicoes):
                    if simboloTransicao != '' and self.getElement(estadoDestino) in vivos and estado not in vivos and estado not in novosVivos:
                        mudanca = True
                        novosVivos.append(estado)

                vivos.extend(novosVivos)

            if not mudanca:
                break

        print(f"Vivos: {vivos}")
        vivos.sort()
        self.atualizarEstadosETransicoes(vivos)


    def atualizarEstadosETransicoes(self, estadosAlcancaveis: list[str]) -> None:
        transicoes = self.transicoes.copy()
        listaEstadosRemovidos = []

        for estadoOrigem, listaTransicao in enumerate(self.transicoes):
            if self.getElement(estadoOrigem) not in estadosAlcancaveis:
                listaEstadosRemovidos.append(self.getElement(estadoOrigem))

        for estadoARemover in listaEstadosRemovidos:
            for i in range(len(self.estados)):
                transicoes[i][self.getPos(estadoARemover)] = '!'
            transicoes[self.getPos(estadoARemover)] = ['!']*len(self.estados)


        i = 0
        numeroEstadosRemovidos = len(listaEstadosRemovidos)
        estadosRemovidos = 0

        while True:
            if numeroEstadosRemovidos == estadosRemovidos:
                break

            if transicoes[i].count('!') > 0 and transicoes[i].count('!') == len(transicoes[i]) and transicoes[i]:
                estadosRemovidos += 1

                try:
                    transicoes.pop(i)

                    for j in range(len(transicoes)):
                        transicoes[j].pop(i)

                except IndexError:
                    self.log("atualizarEstadosETranscioes", f"i = {i} | j = {j}")
                    print(self.transicoes)
            else:
                i += 1


        #self.log("atualizarEstadosETranscioes", f"Tamanho da matriz de transições: {transicoes}. Abaixo, tamanho de cada lista de transição:")

        self.transicoes = transicoes
        self.estados = estadosAlcancaveis
        self.estados_aceitacao = self.interseccao(self.estados_aceitacao, estadosAlcancaveis)

    def criarTransicoesVazias(self, estadosAlcancaveis: list[str]) -> list[list]:
        transicoes = []
        for i in range(len(estadosAlcancaveis)):
            transicoes[i] = ['']*len(estadosAlcancaveis)                
        return transicoes
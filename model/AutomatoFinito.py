from .Tipos import TipoArquivo, Tipo
from .Automato import Automato

class AutomatoFinito(Automato):
    def __init__(self, estados=None, alfabeto=None, transicoes=None, estado_inicial=None, estados_aceitacao=None) -> None:
        super().__init__(TipoArquivo.AF, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)
 
    # Fazer no papel uma determinazação pra ver se tá certo
    def determinizar(self) -> None:
        # Armazenar transicoes originais do automato
        refTransicoes = self.transicoes.copy()
        refEstados = self.estados.copy()
        novasTransicoes = None

        # Checar se existem transições por E fecho
        if self.checkFor('&'):
            # Dicionario que para cada estado do automato atual temos uma lista de estados e-fecho
            transicoesEFecho = self.calcularEFecho()
            
            for estado in transicoesEFecho:
                # Para cada um do estados originais, temos um novo estado que se denonima
                # sigma fecho daquele estado
                novoEstadoEF = list(transicoesEFecho[estado])
                novoEstadoEF.sort()
                
                self.calcularNovasTransicoes(novoEstadoEF, refEstados)
                self.removerTransicoesEF()
                self.printDebug()
            
        listaNovasTransicoes = self.obterNovasTransicoes()

    # def obterNovasTransicoes(self) -> list:
    #     # Passar por cada lista de transição de estado desempacotando os símbolos e
    #     # checando se existe alguma replicação. Se for verdade, adicionar a linha e coluna
    #     # e o elemento para ser retornado
    #     listaSimbolos = []

    #     # Cada iteração do loop de fora é uma iteração sobre uma lista de transições de um símbolo
    #     for i in range(len(self.estados)):
    #         setSimbolosEstado = set()

    #         for j in range(len(self.estados)):
    #             listaSimbolosTemp = list(filter(lambda x: x != '', self.unpackSimbolos(self.transicoes[i][j])))
                
    #             # Jeito mais elegante para checar replicações na lista
    #             if len(listaSimbolosTemp) > 0:
    #                 tam = len(setSimbolosEstado)
    #                 setSimbolosEstado.update(listaSimbolosTemp)
    #                 novoTam = len(setSimbolosEstado)

    #                 if tam == novoTam:



    def removerTransicoesEF(self):
        for i in range(len(self.estados)):
            for j in range(len(self.estados)):
                if '&' in self.transicoes[i][j]:
                    novaTransicao = self.unpackSimbolos(self.transicoes[i][j]).remove('&')
                    self.transicoes[i][j] = self.packSimbolos(novaTransicao)

    def calcularNovasTransicoes(self, novoEstadoEF: list, refEstados: list) -> None:
        listaNovosEstadosOriginados = []
        novoEstadoEFString = self.packSimbolos(novoEstadoEF)
        
        if novoEstadoEFString not in refEstados:
            if novoEstadoEFString not in self.estados:
                self.addEstado(novoEstadoEFString)

            for simbolo in self.alfabeto:
                #Para cada símbolo, teremos um novo estado destino
                novoEstadoOriginado = []
            
                # iterar sobre as transições dos estados que estão lista procurando por transições com esse símbolo.
                # se essa transição existir, o estado irá para um conjunto do novo estado
                for i in range(len(self.estados)):
                    for j in range(len(self.estados)):
                        # Existe uma transição por esse símbolo e que o estado origem dessa transição está presente no conjunto do novoEstadoEF
                        if simbolo in self.transicoes[i][j] and self.getElement(i) in novoEstadoEF:
                            novoEstadoOriginado.append(self.estados[j])
                
                # Se eu consegui gerar um novo estado não vazio, preciso adicionar esse novo estado a lista de estados e também gerar as suas transições
                # Além de atualizar as transições do novoEstadoEF que tem esse novo estado como destino 
                if len(novoEstadoOriginado) != 0:
                    estadoOriginadoString = self.packSimbolos(novoEstadoOriginado)
                
                    if estadoOriginadoString not in self.estados: 
                        self.addEstado(estadoOriginadoString)
                        listaNovosEstadosOriginados.append(novoEstadoOriginado)
                    else:
                        simboloAntigo = self.transicoes[self.getPos(novoEstadoEFString)][self.getPos(estadoOriginadoString)]
                        # Se já existir uma transição, apenas adicionamos essa nova transição, caso contrário, setamos a transição para esse símbolo
                        if simboloAntigo == '':
                            self.transicoes[self.getPos(novoEstadoEFString)][self.getPos(estadoOriginadoString)] = simbolo
                        else:
                            novosSimbolos = [simbolo, simboloAntigo]
                            self.transicoes[self.getPos(novoEstadoEFString)][self.getPos(estadoOriginadoString)] = self.packSimbolos(novosSimbolos)
                        
            for estado in listaNovosEstadosOriginados:
                self.calcularNovasTransicoes(estado, refEstados)
        
        
    def addEstado(self, novoEstado: str) -> None:
        for i in range(len(self.estados)):
            self.transicoes[i].append('')
        
        self.transicoes.append(['']*len(self.transicoes[0]))
        if novoEstado == '':
            self.estados.append(novoEstado)
        else:
            self.estados.append(novoEstado)
        self.printDebug()

    # Calcular novas transições e adicionar novos estados caso não existam  
    def calcularTransicoes(self, novoEstadoEF: list) -> None:
        # Lista de listas onde cada elemento (lista) é um novo estado
        novosEstados = []

        for estado in novoEstadoEF:
            listaTransicoes = self.transicoes[self.getPos(estado)]
            listaNovoEstado = []
            

            for pos in range(len(listaTransicoes)):
                if listaTransicoes[pos] != "":
                    listaNovoEstado.append(listaTransicoes[pos])

        novosEstados.append(listaNovoEstado)

    # Sigma Fecho de um estado é o próprio estado + todos os estados 
    # que eu alcanço de um modo recursivo a partir de transições & 
    def checkFor(self, simbol: str) -> bool:
        for i in range(len(self.estados)):
            for j in range(len(self.estados)):
                if simbol in self.transicoes[i][j]:
                    return True

        return False
    
    def calcularEFecho(self) -> dict:
        dicEstadosEFecho = {}
        for estado in self.estados:
            setEstadosEFecho = set()
            setEstadosEFecho.add(estado)
            dicEstadosEFecho[estado] = self.findETransicao(estado, setEstadosEFecho)

        return dicEstadosEFecho

    def checkEstadoFinal(self, estadoSet: set) -> bool:
        for final in self.estados_aceitacao:
            return True
        return False

    def findETransicao(self, estado: str, setEstadosEFecho: set) -> set:
        for i in range(len(self.estados)):
            for j in range(len(self.estados)):
                if '&' in self.transicoes[i][j] and self.estados[i] == estado:
                    # Adiciono o estado destino pois fará parte do conjunto sigma fecho desse estado
                    setEstadosEFecho.add(self.estados[j])
                    # Parte da função recursiva que irá testar novamente todas as transições pro novo estado capturado
                    setEstadosEFecho.union(self.findETransicao(self.estados[j], setEstadosEFecho))

        return setEstadosEFecho
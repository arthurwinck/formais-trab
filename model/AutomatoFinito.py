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

        #self.printar()
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
                self.removerTransicoes('&')
                #self.printDebug()

        # Calcular novos estados e transições a partir de transições replicadas (mesmo estado origem e mesmo símbolo)
        self.calcularTransicoesADeterminizar()
        print("Automato determinizado")

    # Obter todos os estados destinos tendo um símbolo de transição e um estado origem
    def getEstadosDestinosPorSimbolo(self, estadoOrigem: str, simbolo: str) -> list:
        return [i for i, simboloTransicao in enumerate(self.transicoes[self.getPos(estadoOrigem)]) if simboloTransicao == simbolo]

    # Buscar todas as transições pelo mesmo símbolo e estado de origem, a ponto de determinizá-las
    def calcularTransicoesADeterminizar(self) -> None:
        dictTransicoesPorMesmoSimbolo = self.findTransicoesPorMesmoSimbolo()
        print(f"Transicoes por mesmo símbolo: {dictTransicoesPorMesmoSimbolo}")

        # Passo por todos símbolos de cada dicionário. Para cada tupla de símbolo e estado, obter o novo estado determinizado
        for key in dictTransicoesPorMesmoSimbolo:
            for simbolo in dictTransicoesPorMesmoSimbolo[key]:
                estadosDestinoPorSimbolo = self.getEstadosDestinosPorSimbolo(key, simbolo)
                self.calcularNovasTransicoesDet(key, estadosDestinoPorSimbolo, simbolo)

    # Função principal para criar novas transições determinizadas (usa calcularNovasTransicoes)
    def calcularNovasTransicoesDet(self, estadoOrigem: str, estadoDestinoPorSimbolo: list, simbolo: str):
        print(f"estadoOrigem: {estadoOrigem}, estadoDestinoPorSimbolo: {list(map(self.getElement, estadoDestinoPorSimbolo))}, simbolo: {simbolo}")

        # Converter lista númerica de estados em uma lista de strings
        if len(estadoDestinoPorSimbolo) != 0:
            if isinstance(estadoDestinoPorSimbolo[0], int):
                estadoDestinoPorSimbolo = list(map(self.getElement, estadoDestinoPorSimbolo))
            
            # Novo estado que agrupa estados originais
            estadoDestinoPorSimboloStr = self.packSimbolos(estadoDestinoPorSimbolo)
            
            #if estadoDestinoPorSimboloStr in self.estados:
            self.calcularNovasTransicoes(estadoDestinoPorSimbolo, self.estados)
            
            simbolosTransicao = self.transicoes[self.getPos(estadoOrigem)][self.getPos(estadoDestinoPorSimboloStr)]
            
            listaSimbolosTransicao = self.unpackSimbolos(simbolosTransicao)

            print(f"listaSimbolosTransicao: {listaSimbolosTransicao}")
            
            self.removeTransicoesDeterminizadas(estadoOrigem, estadoDestinoPorSimbolo, simbolo)

            if listaSimbolosTransicao == ['']:
                self.transicoes[self.getPos(estadoOrigem)][self.getPos(estadoDestinoPorSimboloStr)] = simbolo
            elif simbolo not in listaSimbolosTransicao:
                self.transicoes[self.getPos(estadoOrigem)][self.getPos(estadoDestinoPorSimboloStr)] = self.packSimbolos(listaSimbolosTransicao.append(simbolo))                
            
            print(f"Símbolo: {self.transicoes[self.getPos(estadoOrigem)][self.getPos(estadoDestinoPorSimboloStr)]} | estado origem: {estadoOrigem} | estado destino {self.getPos(estadoDestinoPorSimboloStr)}")

    # Buscar todas transições por mesmo símbolo
    def findTransicoesPorMesmoSimbolo(self) -> dict:
        dicEstadoTransicoes = {}
        
        for i in range(len(self.estados)):
            simboloIgualSet = set()
            simbolosNovaTransicao = []
            
            for j in range(len(self.estados)):

                if self.transicoes[i][j] != '':
                    simbolos = self.unpackSimbolos(self.transicoes[i][j])
                    
                    for simbolo in simbolos:
                        tam = len(simboloIgualSet)
                        simboloIgualSet.add(simbolo)

                        if tam == len(simboloIgualSet):
                            simbolosNovaTransicao.append(simbolo)
            
            # dicEstadosTransicoes[estadoOrigem] = simbolosNovaTransicao
            dicEstadoTransicoes[self.getElement(i)] = simbolosNovaTransicao

        return dicEstadoTransicoes

    # Remover as transições que foram determinizadas
    def removeTransicoesDeterminizadas(self, estadoOrigem: str, listEstadosDeterminizados: list, simbolo: str) -> None:
        for i in range(len(self.estados)):
            if simbolo in self.transicoes[self.getPos(estadoOrigem)][i]:
                novaTransicao = self.unpackSimbolos(self.transicoes[self.getPos(estadoOrigem)][i]).remove(simbolo)

                if novaTransicao == None:
                    novaTransicao = ''

                self.transicoes[self.getPos(estadoOrigem)][i] = novaTransicao

    # Remover transições por símbolo (usado com '&')
    def removerTransicoes(self, simbolo: str) -> None:
        for i in range(len(self.estados)):
            for j in range(len(self.estados)):
                if simbolo in self.transicoes[i][j]:
                    novaTransicao = self.unpackSimbolos(self.transicoes[i][j]).remove(simbolo)
                    self.transicoes[i][j] = self.packSimbolos(novaTransicao)

    # Método recursivo para criação de novos estados e suas transições
    def calcularNovasTransicoes(self, novoEstadoEF: list, refEstados: list) -> None:
        listaNovosEstadosOriginados = []

        if isinstance(novoEstadoEF[0], int):
            novoEstadoEF = list(map(self.getElement, (novoEstadoEF)))

        novoEstadoEFString = self.packSimbolos(novoEstadoEF)
        
        #print(f"[]Executando calcularNovasTransicoes para: {novoEstadoEFString}")
        self.log("calcularNovasTransicoes", f"Executando pra {novoEstadoEFString}")

        if novoEstadoEFString not in refEstados:
            if novoEstadoEFString not in self.estados:
                self.addEstado(novoEstadoEFString)

        for simbolo in self.alfabeto:
            #Para cada símbolo, teremos um novo estado destino
            novoEstadoOriginado = set()
        
            # iterar sobre as transições dos estados que estão lista procurando por transições com esse símbolo.
            # se essa transição existir, o estado irá para um conjunto do novo estado
            for i in range(len(self.estados)):
                for j in range(len(self.estados)):
                    # Existe uma transição por esse símbolo e que o estado origem dessa transição está presente no conjunto do novoEstadoEF
                    if simbolo in self.transicoes[i][j] and self.getElement(i) in novoEstadoEF:
                        self.printTransitions()
                        self.log("calcularNovasTransicoes", f"Simbolo {simbolo} existe na transição {self.transicoes[i][j]} do estado origem {self.estados[i]}, dentro de {novoEstadoEF} para {self.estados[j]}")
                        novoEstadoOriginado.add(self.estados[j])
            
            # Se eu consegui gerar um novo estado não vazio, preciso adicionar esse novo estado a lista de estados e também gerar as suas transições
            # Além de atualizar as transições do novoEstadoEF que tem esse novo estado como destino 
            if len(novoEstadoOriginado) != 0:
                estadoOriginadoString = self.packSimbolos(list(novoEstadoOriginado))
            
                if estadoOriginadoString not in self.estados:
                    self.log("calculaNovasTransicoes", f"Adicionando estado {estadoOriginadoString}")
                    self.addEstado(estadoOriginadoString)
                    listaNovosEstadosOriginados.append(list(novoEstadoOriginado))
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
        
    # Adicionar um estado vazio
    def addEstado(self, novoEstado: str) -> None:
        for i in range(len(self.estados)):
            self.transicoes[i].append('')
        
        self.transicoes.append(['']*len(self.transicoes[0]))
        if novoEstado == '':
            self.estados.append(novoEstado)
        else:
            self.estados.append(novoEstado)

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

    # Sigma Fecho de um estado é o próprio estado + todos os estados que eu alcanço de um modo recursivo a partir de transições & 
    def checkFor(self, simbol: str) -> bool:
        for i in range(len(self.estados)):
            for j in range(len(self.estados)):
                if simbol in self.transicoes[i][j]:
                    return True

        return False
    
    # Calcular conjunto de estado & fecho para cada estado
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

    # Função recursiva para buscar todos os possíveis estados realizando as transições por &
    def findETransicao(self, estado: str, setEstadosEFecho: set) -> set:
        estadosProcurados = []
        
        return self.findETransicaoRec(estado, setEstadosEFecho, estadosProcurados)

    def findETransicaoRec(self, estado: str, setEstadosEFecho: set, estadosProcurados: list) -> set:
        for i in range(len(self.estados)):
            for j in range(len(self.estados)):
                if '&' in self.transicoes[i][j] and self.estados[i] == estado:
                    # Adiciono o estado destino pois fará parte do conjunto sigma fecho desse estado
                    setEstadosEFecho.add(self.estados[j])
                    # Parte da função recursiva que irá testar novamente todas as transições pro novo estado capturado
                    if self.estados[j] not in estadosProcurados:
                        estadosProcurados.append(self.estados[j])
                        setEstadosEFecho.union(self.findETransicaoRec(self.estados[j], setEstadosEFecho, estadosProcurados))

        return setEstadosEFecho
        
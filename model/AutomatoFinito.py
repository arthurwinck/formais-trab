from .Tipos import TipoArquivo, Tipo
from .Automato import Automato

class AutomatoFinito(Automato):
    def __init__(self, estados=None, alfabeto=None, transicoes=None, estado_inicial=None, estados_aceitacao=None) -> None:
        super().__init__(TipoArquivo.AF, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)
 
    # DETERMINIZAÇÂO
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------

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

    # MINIMIZAÇÃO
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------

    def minimizar(self) -> None:
        alcancaveis = self.removerInalcancaveis()
        #print(f"Depois de inalcancaveis: estados aceitacao: {self.estados_aceitacao} | alcancaveis: {alcancaveis}")
        vivos = self.removerMortos()
        #print(f"Depois de mortos: estados aceitacao: {self.estados_aceitacao} | vivos: {vivos}")
        self.unirEquivalentes()

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

        return alcancaveis

    def removerMortos(self) -> None:
        vivos = self.estados_aceitacao.copy()

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

        #print(f"Vivos: {vivos}")
        vivos.sort()
        self.atualizarEstadosETransicoes(vivos)

        return vivos


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

    # Estados de equivalentes somente se dividem. Divide & Conquer
    # fazer as divisões localmente (para cada classe) e depois disso atualizar o dicionário
    def unirEquivalentes(self):
        
        dictClasses = {"q0": self.estados_aceitacao, "q1": self.diferenca(self.estados, self.estados_aceitacao)}
        # print ("Antes da união --------------")
        # print(f"dictClasses: {dictClasses}")
        # print(f"self.estados: {self.estados}")

        dictClassesDestino = {}
        i = 2
        mudanca = False
        dictClassesCompare = {}

        while True:
            mudanca = False
            dictClassesCompare = dictClasses.copy()
            for simbolo in self.alfabeto:
                listaClasses = list(dictClasses.keys())
                for classe in listaClasses:
                    listaEstados = dictClasses[classe]
                    if len(listaEstados) > 1:
                        dictClassesAtual = {}
                        dictClassesDestinoAtual = {}

                        for estado in listaEstados:
                            # Criar dict de classes temporário. Estados podem entrar em classes
                            # de estados que estejam na mesma classe 
                            
                            estadoDestino = self.procurarTransicaoPorSimbolo(estado, simbolo)

                            if estadoDestino is not None:
                                # Procura pelo dicionário geral
                                classeDestino = self.procurarClassePorEstado(estadoDestino, dictClasses)
                            else:
                                classeDestino = "MORTO"
                            
                            # se não existe a classe destino ainda, crio ela. Não é preciso fazer mais nada
                            if classe not in dictClassesDestinoAtual.keys():
                                dictClassesDestinoAtual[classe] = classeDestino
                                dictClassesAtual[classe] = [estado]
                                mudanca = True
                            else:
                                classeDestinoExistente = dictClassesDestinoAtual[classe]

                                # A minha classe destino é diferente da classe destino da minha classe original, vou precisar
                                # ser remanejado 
                                #if classeDestino != classeDestinoExistente:

                                # Consigo encontrar uma nova classe criada para essa CLASSE (linha 276) que estou
                                # iterando? Se sim não é necessário criar uma nova classe  
                                acomodarNovaClasse = None
                                
                                # Já que vou precisar trocar de classe, existe uma classe para eu ir já?
                                for classeAtual, classeDestinoAtual in dictClassesDestinoAtual.items():
                                    if classeDestino == classeDestinoAtual:
                                        acomodarNovaClasse = classeAtual

                                # Sim, só coloco o meu estado nessa nova classe
                                if acomodarNovaClasse is not None:
                                    dictClassesAtual[acomodarNovaClasse].append(estado)

                                # Não, preciso criar uma nova classe para mim
                                else: 
                                    #listaEstados.remove(estado)
                                    dictClassesAtual[f"q{i}"] = [estado]
                                    dictClassesDestinoAtual[f"q{i}"] = classeDestino
                                    i += 1

                                mudanca = True

                                                
                        # Atualizar dicionário global com as infos atualizadas do dicionário local
                        dictClasses.update(dictClassesAtual)
                        dictClassesDestino.update(dictClassesDestinoAtual)

            # Realizei toda a iteração e não tive nenhuma mudança? Termino o processo
            if dictClassesCompare == dictClasses:
                break

        # print ("Depois da união --------------")
        # print(f"dictClasses: {dictClasses}")
        # print(f"self.estados: {self.estados}")
        self.calcularNovasTransicoesUnificados(dictClasses)



    def procurarTransicaoPorSimbolo(self, estado: str, simbolo: str) -> str:
        # em um afd existe apenas uma transição por estado origem por simbolo
        for estadoDestino, transicao in enumerate(self.transicoes[self.getPos(estado)]):
            if simbolo in transicao:
                return self.getElement(estadoDestino)

    def procurarClassePorEstado(self, estado: str, dictClasses: dict):
        for classe, listaEstados in dictClasses.items():
            if estado in listaEstados:
                return classe

    # Iterar sobre todas as classes. Pegando todas as transições e ajeitando o automato para
    # somente iterar sobre as classes, criando assim um novo automato
    def calcularNovasTransicoesUnificados(self, dictEstados: dict[str]) -> None:
        listaEstados = self.estados.copy()
        listaEstadosVisitados = []
        transicoes = []
        novaListaEstados = []

        for classe, listaEstadosClasse in dictEstados.items():
            
            listaEstadosClasse.sort()
            
            novoEstadoUnificado = classe
            #novoEstadoUnificado = self.packSimbolos(listaEstadosClasse)

            if novoEstadoUnificado not in novaListaEstados:
                self.addEstadoTransicaoLista(novoEstadoUnificado, novaListaEstados, transicoes)
                listaEstadosVisitados.append(novoEstadoUnificado)
                
            for estadoExemplo in listaEstadosClasse:

                for estadoDestino, listaTransicao in enumerate(self.transicoes[self.getPos(estadoExemplo)]):
                    estadoDestinoStr = self.getElement(estadoDestino)

                    classeDestino = self.procurarClassePorEstado(estadoDestinoStr, dictEstados)

                    if classeDestino != classe and classeDestino not in novaListaEstados:
                        #novoEstadoClasseDestino = self.packSimbolos(dictEstados[classeDestino])
                        novoEstadoClasseDestino = classeDestino
                        self.addEstadoTransicaoLista(novoEstadoClasseDestino, novaListaEstados, transicoes)

                    if listaTransicao != '':   
                        self.editarTransicao(novoEstadoUnificado, novaListaEstados, transicoes, classeDestino, dictEstados, listaTransicao)



        listaEstadosAceitacao = []

        for novoEstado, listaEstados in dictEstados.items():
            if listaEstados == [self.estado_inicial]:
                self.estado_inicial = novoEstado
            if len(self.interseccao(listaEstados, self.estados_aceitacao)) > 0:
                listaEstadosAceitacao.append(novoEstado)
                
        self.estados = novaListaEstados
        self.estados_aceitacao = listaEstadosAceitacao
        self.transicoes = transicoes

    def addEstadoTransicaoLista(self, estado: str, listaEstados: list, transicoes: list[list]) -> None:
        listaEstados.append(estado)
        transicoes.append(['']*len(listaEstados))

        for i in range(len(listaEstados)):
            transicoes[i].append("")
        

    def editarTransicao(self, estado: str, listaEstados: list, transicoes: list[list], classeDestino: str, dictEstados: dict[str], listaTransicao: str) -> None:
        pos = self.getPosLista(estado, listaEstados)
        posDestino = self.getPosLista(classeDestino, listaEstados)
        #posDestino = self.getPosLista(self.packSimbolos(dictEstados[classeDestino]), listaEstados)

        if transicoes[pos][posDestino] == '':
            transicoes[pos][posDestino] = listaTransicao
        else:
            itensListaTransicao = self.unpackSimbolos(listaTransicao)
            transicaoLista = self.unpackSimbolos(transicoes[pos][posDestino])
            for item in itensListaTransicao:
                if item not in transicoes[pos][posDestino]:
                    transicaoLista.append(item)

                transicaoLista.sort()
                transicoes[pos][posDestino] = self.packSimbolos(transicaoLista)


    # ---------------------- INTERSEÇÃO --------------------

    def intersecao(self, automato2:Automato):
        self.unirPropriedades(automato2)
        self.criarTransicao(automato2)
        self.criarEstadoAceitacao(automato2, False)
        
    def criarTransicao(self, automato2:Automato):
        # Obtém o estado inicial do segundo autômato
        estadoInicial2 = int(automato2.estado_inicial)
        # Obtém os estado de aceitação do primeiro autômato
        estadosAceitacao = self.getEstadoAceitacao()
        
        # Insere as transições, dos estados de aceitação do 
        # primeiro para o estado inicial do segundo autômato,
        # na matriz de transições
        for i in range(len(estadosAceitacao)):
            indice = int(estadosAceitacao[i])
            self.transicoes[indice-1][estadoInicial2-1] = '&'

        # Remove os estados de aceitação antigos
        self.estados_aceitacao = automato2.estados_aceitacao

    def criarEstadoAceitacaoInter(self,automato2:Automato):
        pass

    # ------------------------ UNIÃO -----------------------

    def unir(self, automato2:Automato):
        self.unirPropriedades(automato2)
        self.criarEstadoIncial(automato2)
        self.criarEstadoAceitacao(automato2, True)

    def criarEstadoIncial(self, automato2:Automato):

        # Obtém as transições do automato
        transicoes = self.getTransicoes()

        # Cria uma lista vazia, que será a lista de transições do novo estado
        listaVazia = []
        for i in range(len(self.estados)):
            listaVazia.append('')
        # Adiciona a lista vazia à matriz de transições
        transicoes = [listaVazia] + transicoes

        # Desloca as linhas da matriz para criar novo estado
        for i in range(len(transicoes)):
            transicoes[i] = [''] + transicoes[i]

        # Acrescenta o novo estado à lista de estados
        self.estados = ['0'] + self.estados
        self.transicoes = transicoes

        # Insere as transições do novo estado inicial 
        # para os antigos por épsilon
        indice = int(self.estado_inicial)
        self.transicoes[0][indice] = '&'
        indice = int(automato2.estado_inicial)
        self.transicoes[0][indice] = '&'

        # Define o novo estado inicial
        self.estado_inicial = '0'

    def criarEstadoAceitacao(self, automato2:Automato, uniao):
        # Faz uma cópia da lista de estados
        estados = self.getEstados()[:]
        # Obtém as transições do automato
        transicoes = self.getTransicoes()

        # Cria uma lista vazia, que será a lista de transições do novo estado
        listaVazia = []
        for i in range(len(estados)):
            listaVazia.append('')
        # Adiciona a lista vazia à matriz de transições
        transicoes = transicoes + [listaVazia]

        # Acrescenta as linhas da matriz para criar o novo estado
        for i in range(len(transicoes)):
            transicoes[i] = transicoes[i] + ['']

        # Adiciona o novo estado à lista de estados
        if uniao:
            estados.append(str(len(estados)))
        else:
            estados.append(str(len(estados)+1))

        # Define as novas transições do autômato
        self.transicoes = transicoes

        # Soma os estados de aceitação dos dois autômatos
        estadosAceitacao = self.estados_aceitacao + automato2.estados_aceitacao

        # Insere as transições para o novo estado de aceitação na matriz
        for i in range(len(estadosAceitacao)):
            if uniao:
                indice = int(estadosAceitacao[i])
            else:
                indice = int(estadosAceitacao[i]) -1
            self.transicoes[indice][len(self.estados)] = '&' 

        # Define a nova lista de estados do autômato
        self.estados = estados

        # Define a nova lista de estados de aceitação do autômato
        if uniao:
            self.estados_aceitacao = [str(len(self.estados)-1)]
        else:
            self.estados_aceitacao = [str(len(self.estados))]


    def unirPropriedades(self, automato2:Automato):
        # Obtém os estados dos dois automatos
        estados = self.getEstados()[:] # Faz uma cópia da lista
        estados2 = automato2.getEstados()

        # Verifica se os nomes dos estados são repetidos e troca, para não dar confusão nas transições 
        for i in range(len(estados2)):
            # Se o nome for igual
            if estados2[i] in estados:
                # Calcula o novo nome
                simb = str(len(estados2) + i + 1)
                
                # Verifica se é inicial e e modifica
                if estados2[i] == automato2.getEstadoInicial():
                    automato2.estado_inicial = simb

                # Verificar se é de aceitação e modifica
                for j in range(len(automato2.estados_aceitacao)):
                    if automato2.getEstados()[i] == automato2.estados_aceitacao[j]:
                        automato2.estados_aceitacao[j] = simb

                # Atribui o novo nome 
                estados2[i] = simb
                # Adiciona à lista de estados
                estados.append(estados2[i])
                
        # --- UNIÃO DAS TRANSIÇÕES ---
       
        # Obtém as transições dos autômatos
        transicoes1 = self.getTransicoes()
        transicoes2 = automato2.getTransicoes()
        
        # Cria os espaços nas transiçoes do primeiro, para adicioanar as transições do segundo
        for i in range(len(automato2.estados)):
            for j in range(len(automato2.estados)):
                transicoes1[i].append('')

        # Cria uma lista vazia que serve de offset
        listaVazia = []
        for i in range(len(automato2.estados)):
            listaVazia.append('')

        # Adiciona as trasnsições do segundo autômato ao primeiro
        for i in range(len(transicoes2)):
            transicoes1.append(listaVazia + transicoes2[i])
        
        # Une os estados dos dois autômatos
        self.estados = estados

        # Faz a união do alfabetos, removendo os símbolos duplicados
        self.alfabeto = sorted(set(self.getAlfabeto() + automato2.getAlfabeto()))

    def reconhecer(self, sentenca: str) -> bool:
        # Primeiro passo determinizar automato
        self.determinizar()

        if len(self.interseccaoLista(self.alfabeto, list(sentenca))) != len(self.alfabeto):
            return False
        
        estadoAtual = self.estado_inicial
        for simbolo in sentenca:
            for estadoPos, listaTransicao in enumerate(estadoAtual):
                breakEstado = False
                
                for transicao in listaTransicao:
                    if transicao == simbolo:
                        estadoAtual = self.getElement(estadoPos)
                        breakEstado = True
                        break

                if breakEstado:
                    break

        return estadoAtual in self.estados_aceitacao
    
    def converterParaGR(self):
        # Criando um dicionário para relacionar os novos
        # símbolos da gramática com o autômato
        alias = {self.estado_inicial: "S"}
        listaEstados = list(self.estados)
        listaEstados.remove(self.estado_inicial)
        letra = "A"
        i = 0

        for estado in listaEstados:
            alias[estado] = letra            
            letra = chr(ord(letra) + 1)
            
        # Não terminais são todos os estados do nosso autômato 
        naoTerminais = list(alias.values())
        
        # terminais são os símbolos que são consumidos nas transições de estados
        terminais = self.alfabeto

        # Símbolo inicial
        simboloInicial = alias[self.estado_inicial]

        # Produções
        producoes = {}

        for posEstadoOrigem, listaTransicoes in enumerate(self.transicoes):
            for posEstadoDestino, listaSimbolos in enumerate(listaTransicoes):
                if listaSimbolos == '':
                    continue
                
                for simbolo in self.unpackSimbolos(listaSimbolos):
                    producoes[alias[self.getElement(posEstadoOrigem)]] = f"{simbolo}{alias[self.getElement(posEstadoDestino)]}"

                    if self.getElement(posEstadoDestino) in self.estados_aceitacao:
                        producoes[alias[self.getElement(posEstadoOrigem)]] = f"{simbolo}"

        if self.estado_inicial in self.estados_aceitacao:
            simboloInicial = chr(ord(letra) + 1)
            naoTerminais.append(simboloInicial)

            novasProducoes = dict(producoes)

            for naoTerminal, producao in novasProducoes.items():
                if naoTerminal == alias[self.estado_inicial]:
                    producoes[simboloInicial] = producao
                    
        return {
            "naoTerminais": naoTerminais,
            "terminais": terminais,
            "producoes": producoes,
            "simboloInicial": simboloInicial
        }
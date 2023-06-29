from .Tipos import TipoArquivo, Elemento
from random import randint


class GramaticaLC(Elemento):
    def __init__(self, nao_terminais, terminais, producoes, simbolo_inicial) -> None:
        super().__init__(TipoArquivo.GLC)
        self.nao_terminais = nao_terminais
        self.terminais = terminais
        self.producoes = self.arrumarProducoes(producoes)
        self.simbolo_inicial = simbolo_inicial
        self.tabelaAnalise = None
        self.listaSimbolos = None

    def printar(self):
        print(f"self.nao_terminais: {self.nao_terminais}")
        print(f"self.terminais: {self.terminais}")
        print(f"self.producoes: {self.producoes}")
        print(f"self.simbolo_inicial: {self.simbolo_inicial}")

    def arrumarProducoes(self, producoes: list) -> dict:
        dictProducoes = {}
        
        for producao in producoes:
            listaProducao = producao.split("->")

            if listaProducao[0] not in dictProducoes.keys():
                dictProducoes[listaProducao[0]] = [listaProducao[1]]
            else:
                dictProducoes[listaProducao[0]].append(listaProducao[1])

        return dictProducoes

    # Uma gramática é LL1 se e somente se para cada produção A -> a|b temos que:
    # 1) - First(a) e First(b) são conjuntos disjuntos
    #    - (ou) A intersecção de First (b) e First(a) é vazia
    # 2) - se & está em First(b) então First(a) e Follow(A) são conjuntos disjuntos
    #    - se & estiver em First(a) então a intersecção de First(a) e Follow(A) é vazia,
    #    - da mesma forma que First(b) e Follow(A) possuem interseccção vazia
    def checarLL1(self, dictFirst: dict, dictFollow: dict):
        for simbolo in self.nao_terminais:
            if dictFirst[simbolo].intersection(dictFollow[simbolo]) != set():
                return False

        return True

    def criarTabelaAnalise(self):
        dictFirst = self.calcularFirst()
        dictFollow = self.calcularFollow(dictFirst)

        if not self.checarLL1(dictFirst, dictFollow):
            self.log("criarTabelaAnalise", "A gramática não é LL1!")

        self.mapearProducoes()
        self.criarTabelaAnaliseVazia(self.terminais, self.nao_terminais)

        for naoTerminal in self.tabelaAnalise.keys():
            for producao in self.producoes[naoTerminal]:
                numero = self.dictMapaProducoes[naoTerminal+'->'+producao]
                simbolos = [*producao]
                primeiroSimbolo = simbolos[0]
                primeiroDaSequencia = self.getPrimeiroSimboloSequencia(dictFirst, simbolos)

                # Tudo menos & entra em follow do simbolo em sequência
                for simbolo in (primeiroDaSequencia - set('&')):
                    # Se ainda não foi escrito (-1) vamos sobreescrever
                    if self.tabelaAnalise[naoTerminal][simbolo] == -1:
                        # Por qual produção iremos continuar
                        self.tabelaAnalise[naoTerminal][simbolo] = numero
                    # Se não, quer dizer que deu conflito
                    else:
                        self.log("criarTabelaAnalise", "Conflito em tabela de análise")

                # Se & está em first, quer dizer que teremos que ver todos o follows
                if '&' in primeiroDaSequencia:
                    for simboloFollow in dictFollow[naoTerminal]:
                        # Se não existe, podemos sobreescrever
                        if self.tabelaAnalise[naoTerminal][simboloFollow] == -1:
                            self.tabelaAnalise[naoTerminal][simboloFollow] = numero
    
    def fatorarGramatica(self):
        i = 0
        tentativas = 5

        for i in range(tentativas):
            for naoTerminal in self.nao_terminais:
                # resolver não determinismo direto
                # não determinismo direto pode ser de um número variável de símbolos
                dictEstadosPrefixo = self.verificarNaoDeterminismoDireto()
                resolverNDDireto = self.resolverNaoDeterminismoDireto(dictEstadosPrefixo)

            for naoTerminal in self.nao_terminais:
                # if tentativas > 5:
                #     self.log("fatorarGramatica", "Não foi possível fatorar a gramática")
                #     break
                
                dictEstadosPrefixo = self.resolverNaoDeterminismoIndireto(naoTerminal, i)
                resolverNDDireto = self.resolverNaoDeterminismoDireto(dictEstadosPrefixo)


    def procurarPorNovoSimbolo(self) -> str:
        # tentar sempre pegar letras
        if self.listaSimbolos is None:
            self.listaSimbolos = [
            # '!', '@', '#', '$', '%',
            # '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            # 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            # 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            # 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z'
            ]

        while True:
            if len(self.listaSimbolos) < 1:
                raise Exception("Não foi possível criar um novo símbolo")

            simbolo = self.listaSimbolos[randint(0, len(self.listaSimbolos) - 1)]
            if simbolo in self.terminais or simbolo in self.nao_terminais:
                self.listaSimbolos.remove(simbolo)
            else:
                return simbolo

    def resolverNaoDeterminismoDireto(self, dictEstadosPrefixo: dict):
        k = 0
        #dictEstadosPrefixo = self.verificarNaoDeterminismoDireto()
        novasProducoes = None

        if len(dictEstadosPrefixo) > 0:
            # {'S': {'a': [0, 1]}, 'A': {}, 'B': {}, 'C': {'cdAab': [0, 1]}}
            # {estado: dictPrefixo -> {'prefixo': produções que possuem esse prefixo}}
            for naoTerminal, dictPrefixo in dictEstadosPrefixo.items():
                if len(dictPrefixo) > 0:
                    # criar um novo estado sempre no padrão Z(k) onde K é um inteiro
                    novoNaoTerminal = self.procurarPorNovoSimbolo()

                    if novoNaoTerminal is None:
                        raise Exception("Acabaram os símbolos!")

                    self.nao_terminais.append(novoNaoTerminal)
                    self.producoes[novoNaoTerminal] = []
                    novasProducoes = self.copiarDictProducoes(self.producoes)

                    for prefixo, listaPosProducoes in dictPrefixo.items():
                        for posProducao in listaPosProducoes:
                            producao = self.producoes[naoTerminal][posProducao]
                            restoProducao = producao.removeprefix(prefixo)

                            if restoProducao == '':
                                restoProducao = '&'

                            # removendo a produção com não-determinismo
                            novasProducoes[naoTerminal].remove(producao)

                            # adicionando a nova produção
                            if (prefixo + novoNaoTerminal) not in novasProducoes[naoTerminal]:
                                #self.producoes[naoTerminal].append(prefixo + novoNaoTerminal)
                                novasProducoes[naoTerminal].append(prefixo + novoNaoTerminal)

                            # colocando no novo símbolo as produções para o resto do corpo sentencial
                            if restoProducao not in novasProducoes[novoNaoTerminal]:
                                #self.producoes[novoNaoTerminal].append(restoProducao)
                                novasProducoes[novoNaoTerminal].append(restoProducao)

            if novasProducoes is not None:
                self.producoes = novasProducoes

                        
    def copiarDictProducoes(self, dict) -> dict:
        novoDict = {}
        for key, value in dict.items():
            novoDict[key] = list(value)

        return novoDict


    def verificarNaoDeterminismoDireto(self) -> dict:
        # Encontrar prefixo em comum em duas produções que possuem a mesma cabeça

        # Se conseguirmos criar um prefixo maior que ''
        # colocamos em um dicionário o prefixo e as produções
        # que a criam
        listaPrefixo = []
        dictEstadosPrefixo = {}

        for naoTerminal in self.nao_terminais:
            dictPrefixo = {}
            producoes = self.producoes[naoTerminal]
            
            # Iterar sobre cada produção tentando criar um prefixo em comum
            # com outra produção
            for i, corpoProducao in enumerate(producoes):
                # Iterar sobre as outras produções buscando aumentar o prefixo
                for j, corpoOutraProducao in enumerate(producoes):
                    if i < j:
                        prefixo = self.buscarMaiorPrefixo(corpoProducao, corpoOutraProducao)
                    
                        if prefixo != '':
                            if prefixo not in dictPrefixo:
                                dictPrefixo[prefixo] = [i,j]
                            else:
                                dictPrefixo[prefixo].append(j)

                            listaPrefixo.append(prefixo)

            dictEstadosPrefixo[naoTerminal] = dictPrefixo

        return dictEstadosPrefixo

    # Busca maior prefixo de duas produções
    def buscarMaiorPrefixo(self, corpoProducao: str, corpoOutraProducao: str):
        prefixo = []
        pular = False
        
        for i, charCorpo in enumerate(corpoProducao):
            charOutraProducao = None
            
            try:
                charOutraProducao = corpoOutraProducao[i]
            except IndexError:
                return prefixo

            if charCorpo == charOutraProducao:
                prefixo.append(charCorpo)
            else:
                prefixo = "".join(prefixo)
                return prefixo

    def resolverNaoDeterminismoIndireto(self, naoTerminal: str, i: int):
        self.verificarNaoDeterminismoIndireto(naoTerminal, i)

    def verificarNaoDeterminismoIndireto(self, naoTerminal: str, i: int):
        producoesTemp = []
        relacoes = []

        for producao in self.producoes[naoTerminal]:
            # buscamos o primeiro símbolo para checarmos se existe um não det. indireto por ele
            primeiroSimbolo = producao[0]

            # produção é vazia
            if primeiroSimbolo is None:
                continue

            # Produção pode ser do tipo 'a&' onde será necessário ajustar produções
            # caso haja outra produção do tipo 'aX'
            if primeiroSimbolo in self.terminais and producao not in producoesTemp:
                producoesTemp.append(producao)

                if primeiroSimbolo not in relacoes:
                    # producao se relaciona com ela mesma
                    relacoes.append((producao, producao))

            # Se o primeiro símbolo que estamos vendo é um não terminal
            # podemos estar lidando com um ND indireto mesmo
            if primeiroSimbolo in self.nao_terminais:
                # buscar produções do não terminal
                producoesPrimeiroSimbolo = self.producoes[primeiroSimbolo]

                # Sabemos que os símbolos só possuem um caractere -> não é necessário índice
                producoesDerivadas, relacaoDerivadaOrigem = self.obterProducoesDerivadas(producao, producoesPrimeiroSimbolo)

                for producaoDerivada in producoesDerivadas:
                    if producaoDerivada not in producoesTemp:
                        producoesTemp.append(producaoDerivada)

                for relDerivadaOrigem in relacaoDerivadaOrigem:
                    if relDerivadaOrigem not in relacoes:
                        relacoes.append(relDerivadaOrigem)

        
        # Alterar função de verificar não determinismo direto para que seja por parametro e
        # nao atributo de classe
        self.transformarNDIndiretoEmDireto(producoesTemp, relacoes, naoTerminal)

    def transformarNDIndiretoEmDireto(self, producoes: list, relacoes: list[tuple], estadoOrigem: str):
        novasProducoes = self.copiarDictProducoes(self.producoes)
        listaProducoesRemover = []
        dictPrefixo = {}

        for i, corpoProducao in enumerate(producoes):
            # Iterar sobre as outras produções buscando aumentar o prefixo
            for j, corpoOutraProducao in enumerate(producoes):
                if i < j:
                    prefixo = self.buscarMaiorPrefixo(corpoProducao, corpoOutraProducao)
                
                    if prefixo != '':
                        if prefixo not in dictPrefixo:
                            dictPrefixo[prefixo] = [i,j]
                        else:
                            dictPrefixo[prefixo].append(j)

        for prefixo, listaPosProducao in dictPrefixo.items():
            for posProducao in listaPosProducao:
                novaProducao = producoes[posProducao]
                producaoOrigem = self.procurarProducaoOrigem(novaProducao, relacoes)

                if producaoOrigem not in listaProducoesRemover:
                    listaProducoesRemover.append(producaoOrigem)
                
                self.producoes[estadoOrigem].append(novaProducao)

        for producaoOrigem in listaProducoesRemover:
            self.producoes[estadoOrigem].remove(producaoOrigem)

        
    def procurarProducaoOrigem(self, producao: str, relacoes: list[tuple]):
        for relacao in relacoes:
            if relacao[0] == producao:
                return relacao[1]

    # A ideia é derivar até encontrarmos (ou terminarmos de ver as produções)
    def obterProducoesDerivadas(self, producaoOrigem: str, producoesPrimeiroSimbolo: list[str]) -> tuple[list, list]:
        producoesDerivadas = []
        relacaoDerivadaOrigem = []

        for producaoPrimeiroSimbolo in producoesPrimeiroSimbolo:
            
            # Como somente possuimos símbolos de 1 caractere, pegamos sempre o primeiro
            # caractere da producao origem 
            producaoDerivada = producaoPrimeiroSimbolo + producaoOrigem[0]
            relacao = (producaoDerivada, producaoOrigem)

            if producaoDerivada not in producoesDerivadas:
                producoesDerivadas.append(producaoDerivada)

            if relacao not in relacaoDerivadaOrigem:
                relacaoDerivadaOrigem.append(relacao)

        return (producoesDerivadas, relacaoDerivadaOrigem)

    def removerRecursaoIndireta(self):
        novasProducoes = {S: [] for S in self.nao_terminais}
        for posI, naoTerminalI in enumerate(self.nao_terminais):
            
            for posJ in range(posI):
                naoTerminalJ = self.nao_terminais[posJ]
                
                for producaoI in self.producoes[naoTerminalI]:    
                    if naoTerminalJ == producaoI[0]:
                        self.producoes[naoTerminalI].remove(producaoI)
                        
                        for producaoJ in self.producoes[naoTerminalJ]:
                            producao = producaoJ + producaoI[0:]
                            if producao not in novasProducoes[naoTerminalI]:
                                novasProducoes[naoTerminalI].append(producao)

                        
                    else:
                        producao = producaoI
                        if producao not in novasProducoes[naoTerminalI]:
                            novasProducoes[naoTerminalI].append(producao)

            else:
                for producaoI in self.producoes[naoTerminalI]:
                    producao = producaoI
                    if producao not in novasProducoes[naoTerminalI]:
                        novasProducoes[naoTerminalI].append(producao)

        self.producoes = novasProducoes


    def removerRecursaoDireta(self):
        novasProducoes = {}
        
        for cabeca, listaCorpos in self.producoes.items():
            listaCorpoRecursivo = []
            for corpo in listaCorpos:
                if corpo[0] == cabeca:
                    listaCorpoRecursivo.append(corpo)

            if len(listaCorpoRecursivo) > 0:
                novaCabeca = self.procurarPorNovoSimbolo()
                novosCorpos = ['&']
                cabecaCorpo = []

                for corpo in listaCorpos:
                    # A -> Aa | B
                    
                    if corpo in listaCorpoRecursivo:
                        # A' -> aA' 
                        novosCorpos.append(corpo[1:] + novaCabeca)
                    else:
                        # A -> BA'
                        cabecaCorpo.append(corpo + novaCabeca)

                novasProducoes[cabeca] = cabecaCorpo
                novasProducoes[novaCabeca] = novosCorpos

            else:
                novasProducoes[cabeca] = listaCorpos

        self.nao_terminais = list(set(novasProducoes.keys()))
        self.producoes = novasProducoes


    def calcularFirst(self) -> dict:
        # If x is a terminal, then FIRST(x) = { ‘x’ }
        dictFirst = {s: set((s,)) for s in self.terminais + ['&']}
        print(dictFirst)

        #If x-> &, is a production rule, then add Є to FIRST(x)
        for naoTerminal in self.nao_terminais:
            dictFirst[naoTerminal] = set()

        # If X->Y1 Y2 Y3….Yn is a production,
        # 1) If x is a terminal, then FIRST(x) = { ‘x’ }
        # 2) FIRST(X) = FIRST(Y1)
        # First de uma produção que tem um corpo que começa com Y1 é Y1 (caso First(Y1) não tenha &)

        # 3) If FIRST(Y1) contains & then FIRST(X) = { FIRST(Y1) – Є } U { FIRST(Y2) }
        # 4) If FIRST (Yi) contains & for all i = 1 to n, then add Є to FIRST(X).

        novoSimbolo = True

        while novoSimbolo:
            novoSimbolo = False

            # self.producoes é um dicionário em que cada
            # produção é uma entrada da lista, que o seu corpo é a chave do item
            # {'A': [aAb, b]} => A -> aAb | b 
            for cabeca, listaCorpo in self.producoes.items():
                for corpo in listaCorpo:
                    simbolo = self.buscarPrimeiroSimbolo(corpo, self.nao_terminais, self.terminais)

                    #1) If x is a terminal, then FIRST(x) = { ‘x’ }
                    if simbolo in self.terminais + ['&']:
                        novoFirst = dictFirst[cabeca].union(dictFirst[simbolo])

                    # 2) First(x) = first(y1)
                    elif simbolo in self.nao_terminais:
                        simboloToAdd = dictFirst[simbolo]
                        novoFirst = dictFirst[cabeca].union(simboloToAdd - set('&'))

                        # Se o primeiro simbolo da produção possui & temos que pegar o próximo símbolo
                        while '&' in simboloToAdd:
                            corpo = corpo[1:]
                            if corpo == '':
                                novoFirst = novoFirst.union('&')
                                break

                            simbolo = self.buscarPrimeiroSimbolo(corpo, self.nao_terminais, self.terminais)
                            simboloToAdd = dictFirst[simbolo]
                            novoFirst = novoFirst.union(simboloToAdd - set('&'))
                    
                    else:
                        self.log("calcularFirst", f"Não foi possível encontrar o símbolo {simbolo}")

                    if novoFirst != dictFirst[cabeca]:
                        novoSimbolo = True
                        dictFirst[cabeca] = novoFirst

        return dictFirst
                
    # Função para buscar o primeiro símbolo para o algoritmo de first
    # Funciona somente para gramáticas LC que possuem símbolos de 1 caractere
    def buscarPrimeiroSimbolo(self, corpo: str, naoTerminais: list, terminais: list) -> str:
        simbolos = naoTerminais + terminais + ['&']

        for simbolo in corpo:
            if simbolo in simbolos:
                return simbolo
        return corpo

    def calcularFollow(self, dictFirst: dict) -> dict:
        if dictFirst is None:
            dictFirst = self.calcularFirst()

        # 1) FOLLOW(S) = { $ }   // where S is the starting Non-Terminal

        # 2) If A -> pBq is a production, where p, B and q are any grammar symbols,
        # then everything in FIRST(q)  except Є is in FOLLOW(B).

        # 3) If A->pB is a production, then everything in FOLLOW(A) is in FOLLOW(B).

        # 4) If A->pBq is a production and FIRST(q) contains Є, 
        # then FOLLOW(B) contains { FIRST(q) – Є } U FOLLOW(A)

        dictFollow = {s: set(()) for s in self.nao_terminais}
        dictFollow[self.simbolo_inicial] = set('$')
        
        # Usado para guardar a referência quando um simbolo recebe o follow de outro simbolo
        # e esse outro simbolo pode ser atualizado
        dictFollowIn = {s: set(()) for s in self.nao_terminais}

        novoSimbolo = True

        while novoSimbolo:
            novoSimbolo = False

            # self.producoes é um dicionário em que cada
            # produção é uma entrada da lista, que o seu corpo é a chave do item
            # {'A': [aAb, b]} => A -> aAb | b 
            for cabeca, listaCorpo in self.producoes.items():
                for corpo in listaCorpo:
                    simbolosLista = [x for x in corpo]

                    for i, simbolo in enumerate(simbolosLista):
                        
                        # Se ele for não terminal precisamos checar quais são seus possíveis símbolos de first
                        # e também se um dos possíveis firsts dele é o '&'
                        if simbolo in self.nao_terminais:
                            alvo = simbolo
                            followAntigo = dictFollow[alvo]

                            # procurando o próximo símbolo depois desse não terminal
                            proxSimbolos = simbolosLista[i+1:]

                            if proxSimbolos != []:
                                firstProx = self.buscarFirstLista(proxSimbolos, dictFirst)

                                dictFollow[alvo].update((firstProx - set('&')))

                                # Se no first do próximo símbolo existe um '&'

                                if '&' in firstProx:
                                    if cabeca != alvo:
                                        dictFollowIn[cabeca].add(alvo)
                            
                            # Se o próximo simbolo for vazio
                             # 3) If A->pB is a production, then everything in FOLLOW(A) is in FOLLOW(B).
                            else:
                                if cabeca != alvo:
                                    dictFollowIn[cabeca].add(alvo)

                            if followAntigo != dictFollow[alvo]:
                                novoSimbolo = True

        novoSimbolo = True
        while(novoSimbolo):
            novoSimbolo = False
            for simboloNaoTerminal, listaIn in dictFollowIn.items():
                for simboloIn in listaIn:
                    followAntigo = dictFollow[simboloIn]
                    dictFollow[simboloIn].update(dictFollow[simboloNaoTerminal])

                    if followAntigo != dictFollow[simboloIn]:
                        novoSimbolo = True

        return dictFollow


    def buscarFirstLista(self, proxSimbolos: list[str], dictFirst: dict) -> set:
        firstProx = set()
        for i, simbolo in enumerate(proxSimbolos):
            # Caso estejamos iterando sobre um simbolo que não possui & em seu first, quer dizer que
            # paramos a atualização do first. 
            if '&' not in dictFirst[simbolo]:
                firstProx.update(dictFirst[simbolo])
                break
            # 4) If A->pBq is a production and FIRST(q) contains Є, 
            # then FOLLOW(B) contains { FIRST(q) – Є } U FOLLOW(A)
            firstProx.update(dictFirst[simbolo] - set('&'))
            
            # Se tivermos no último símbolo e temos '&' na produção, adicionamos no first da produção
            if i == len(proxSimbolos) - 1:
                firstProx.add('&')

        return firstProx

    def getPrimeiroSimboloSequencia(self, dictFirst, simbolos) -> set:
        primeiroSimboloSeq = set()
        for i in range(len(simbolos)):
            if '&' not in dictFirst[simbolos[i]]:
                primeiroSimboloSeq.update(dictFirst[simbolos[i]])
                break

            # Tudo menos o vazio
            primeiroSimboloSeq.update((dictFirst[simbolos[i]] - set('&')))
            if i == len(simbolos) - 1:
                primeiroSimboloSeq.add('&')

        return primeiroSimboloSeq

    def mapearProducoes(self):
        dictMapaProducoes = {}
        i = 0

        for naoTerminal in self.nao_terminais:
            for producao in self.producoes[naoTerminal]:
                item = naoTerminal+'->'+producao
                dictMapaProducoes[item] = i
                dictMapaProducoes[i] = item
                i+= 1
        
        self.dictMapaProducoes = dictMapaProducoes

    def criarTabelaAnaliseVazia(self, terminais: list, naoTerminais: list):
        self.tabelaAnalise = {}
        terminais.append('$')

        for naoTerminal in naoTerminais:
            self.tabelaAnalise[naoTerminal] = dict()
            for terminal in terminais:
                self.tabelaAnalise[naoTerminal][terminal] = -1


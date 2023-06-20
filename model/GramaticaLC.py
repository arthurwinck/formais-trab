from .Tipos import TipoArquivo, Elemento


class GramaticaLC(Elemento):
    def __init__(self, nao_terminais, terminais, producoes, simbolo_inicial) -> None:
        super().__init__(TipoArquivo.GLC)
        self.nao_terminais = nao_terminais
        self.terminais = terminais
        self.producoes = self.arrumarProducoes(producoes)
        self.simbolo_inicial = simbolo_inicial
        self.tabelaAnalise = self.criarTabelaAnalise()

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
    
    def criarTabelaAnalise(self):
        dictFirst = self.calcularFirst()
        dictFollow = self.calcularFollow(dictFirst)


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

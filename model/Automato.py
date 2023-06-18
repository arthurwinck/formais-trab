from .Tipos import TipoArquivo, Elemento

#[[], [], []]
class Automato(Elemento):
    def __init__(self, tipo, estados=None, alfabeto=None, transicoes=None, estado_inicial=None, estados_aceitacao=None) -> None:
        super().__init__(tipo)
        self.estados = estados
        self.alfabeto = alfabeto
        # Matriz NxN onde N = número de estados
        self.transicoes = [['' for column in range(len(self.estados))] for row in range(len(self.estados))]
        self.criarTransicoes(transicoes)
        self.estado_inicial = estado_inicial.pop()
        self.estados_aceitacao = estados_aceitacao

    def getPos(self, simbolo: str) -> int:
        return self.estados.index(simbolo)

    def getPosLista(self, simbolo: str, lista: list) -> int:
        return lista.index(simbolo)

    def getElement(self, index: int) -> str:
        return self.estados[index]

    def getElementLista(self, index: int, lista: list) -> str:
        return lista[index]
    
    def getTransicoes(self):
        return self.transicoes

    # Transforma string de simbolos "a,b,c" em lista 
    def unpackSimbolos(self, simbolos: str) -> list:
        return simbolos.split(",")

    # Transforma lista de símbolos [a,b,c] em string
    def packSimbolos(self, simbolos: list) -> str:
        if simbolos != None:
            if isinstance(simbolos, list):
                if len(simbolos) > 0:
                    simbolosSorted = simbolos.copy()
                    simbolosSorted.sort()
                    
                    return ",".join(simbolosSorted)
                else:
                    return ""
            elif isinstance(simbolos, str):
                return simbolos
        else:
            return ""      

    def printarTransicoes(self):
        for i in range(len(self.transicoes)):
            for j in range(len(self.transicoes[0])):
                if self.transicoes[i][j] != '':
                    print(f"{self.estados[i]} --{self.transicoes[i][j]}--> {self.estados[j]}")

    # Realizamos um mapeamento usando a lista de estados ordenada para criar 
    # a matriz de transições -> origemXdestino onde o elemento i[origem][destino]
    # é igual aos simbolos por qual a transição origem->destino acontecem 
    def criarTransicoes(self, listaTransicoes: list) -> None:
        for transicao in listaTransicoes:
            listaTransicao = transicao.split(" ")

            if len(listaTransicao) < 3:
                raise Exception("Uma transição possui menos que os 3 elementos (origem, destino, símbolo(s) separados por vírgula)")

            origem = listaTransicao[0]
            destino = listaTransicao[1]
            simbolos = listaTransicao[2]

            #self.log("criarTransicoes", f"criando transição para {origem} -{simbolos}-> {destino}")

            # Teste para ver se símbolos estão bem estruturados
            simbolos = self.unpackSimbolos(simbolos)
            transicaoExistente = self.transicoes[self.getPos(origem)][self.getPos(destino)] 

            if transicaoExistente != '':
                listaTransicaoExistente = self.unpackSimbolos(transicaoExistente)
                listaTransicaoExistente.extend(simbolos)
                self.transicoes[self.getPos(origem)][self.getPos(destino)] = self.packSimbolos(listaTransicaoExistente)
            else:
                self.transicoes[self.getPos(origem)][self.getPos(destino)] = self.packSimbolos(simbolos)


    def printar(self):
        print("------------------------------------")
        if self.tipo == TipoArquivo.AF:
            print("Automato Finito:")
        else:
            print("Automato de Pilha:")
        if isinstance(self.estado_inicial, list):
            print(f"Estado inicial: ({','.join(self.estado_inicial)})")
        else:
            print(f"Estado inicial: ({self.estado_inicial})")

        print(f"Estados: {self.estados}")
        print(f"Estado(s) de aceitação: ({' | '.join(self.estados_aceitacao)})")
        print(f"Alfabeto: ({','.join(self.alfabeto)})")
        
        print("Transições:")
        self.printarTransicoes()
        print("------------------------------------")

    def printDebug(self) -> None:
        print("--------------- [DEBUG] - AUTOMATO ---------------")
        print(f"Estados: {self.estados}")
        print(f"Alfabeto: {self.alfabeto}")
        print(f"Tamanho da lista de estados: {len(self.estados)}")
        print(f"Tamanho da lista de lista de transições: {len(self.transicoes)}")
        print(f"Tamanho da lista de transições de cada elemento:")
        try:
            for i in range(len(self.estados)):
                print(f"    Estado {self.getElement(i)}: {len(self.transicoes[i])}")
        except IndexError:
            print("Erro ao tentar printar - a lista de estados e a lista de transições possuem valores diferentes")

        # try:
        #     for i in range(len(self.estados)):
        #         print(f"    Lista de transições de {self.getElement(i)} ---")
        #         for j in range(len(self.estados)):
        #             print(f"        {self.estados[i]} -> {self.estados[j]} por {self.transicoes[i][j]}")
        # except IndexError:
        #     print("Index erro ao tentar printar transições - lista de estados e lista de transições possuem tamanhos diferentes")
        print("--------------- [DEBUG] - AUTOMATO ---------------")

    def printTransitions(self) -> None:
        # Calculate the maximum width of each column
        column_widths = [max(len(estado), max(len(str(transicoes)) for transicoes in self.transicoes[i])) for i, estado in enumerate(self.estados)]

        # Print the header row with state labels and dividers
        header_row = "     " + " | ".join(f"[{estado.center(width)}]" for estado, width in zip(self.estados, column_widths))
        divider_row = "-----+" + "+".join("-" * width for width in column_widths)
        print(header_row)
        print(divider_row)

        # Print each row of the transition matrix with dividers
        for i, row in enumerate(self.transicoes):
            estado_label = self.estados[i]
            transicoes = " | ".join(str(transicoes).center(width) if transicoes else "" for transicoes, width in zip(row, column_widths))
            row_str = f"[{estado_label}] | {transicoes}"
            print(row_str)

    # Retorna o estado inicial do autômato
    def getEstadoInicial(self):
        return self.estado_inicial

    # Retorna os estados finais do autômato
    def getEstadoAceitacao(self):
        return self.estados_aceitacao

    # Retorna a lista de estados do autômato
    def getEstados(self):
        return self.estados

    # Retorna o alfabeto do autômato
    def getAlfabeto(self):
        return self.alfabeto
from .Tipos import TipoArquivo, Elemento, Tipo

#[[], [], []]
class Automato(Elemento):
    def __init__(self, tipo, estados=None, alfabeto=None, transicoes=None, estado_inicial=None, estados_aceitacao=None) -> None:
        super().__init__(tipo)
        self.estados = estados
        self.alfabeto = alfabeto
        # Matriz NxN onde N = número de estados
        self.transicoes = [['' for column in range(len(self.estados))] for row in range(len(self.estados))]
        self.criarTransicoes(transicoes)
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao

    def getPos(self, simbolo: str) -> int:
        return self.estados.index(simbolo)

    def getElement(self, index: int) -> str:
        return self.estados[index]

    # Transforma string de simbolos "a,b,c" em lista 
    def unpackSimbolos(self, simbolos: str) -> list:
        return simbolos.split(",")

    # Transforma lista de símbolos [a,b,c] em string
    def packSimbolos(self, simbolos: list) -> str:
        if simbolos != None:
            if len(simbolos) != 0:
                simbolosSorted = simbolos.copy()
                simbolosSorted.sort()
            return ",".join(simbolosSorted)
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

            # Teste para ver se símbolos estão bem estruturados
            simbolos = self.packSimbolos(self.unpackSimbolos(simbolos))

            self.transicoes[self.getPos(origem)][self.getPos(destino)] = simbolos


    def printar(self):
        print("------------------------------------")
        if self.tipo == TipoArquivo.AF:
            print("Automato Finito:")
        else:
            print("Automato de Pilha:")
        print(f"Estado inicial: ({','.join(self.estado_inicial)})")
        print(f"Estado(s) de aceitação: ({','.join(self.estados_aceitacao)})")
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
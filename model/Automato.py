from .Tipos import TipoArquivo, Elemento, Transicao

class Automato(Elemento):
    def __init__(self, tipo, estados=None, alfabeto=None, transicoes=None, estado_inicial=None, estados_aceitacao=None) -> None:
        super().__init__(tipo)
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.criarTransicoes(self.transicoes)
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao

        # [[1 2 a], [2 3 b], [4 5 a,b,c]]
    def criarTransicoes(self, matriz):
        novasTransicoes = []

        for transicao in matriz:
            novaTransicao = Transicao()
            listaTransicao = transicao.split(" ")

            if len(listaTransicao) < 3:
                raise Exception("Uma transição possui menos que os 3 elementos (origem, destino, símbolo(s) separados por vírgula")

            novaTransicao.origem = listaTransicao[0]
            novaTransicao.destino = listaTransicao[1]

            simbolos = listaTransicao[2].split(",")

            for simbolo in simbolos:
                novaTransicao.simbolos.append(simbolo)

            novasTransicoes.append(novaTransicao)

        self.transicoes = novasTransicoes
            
    def printar(self):
        print("------------------------------------")
        if self.tipo == TipoArquivo.AF:
            print("Automato Finito:")
        else:
            print("Automato de Pilha:")
        print(f"Estado inicial: ({','.join(self.estado_inicial)})")
        print(f"Estados de aceitação: ({','.join(self.estados_aceitacao)})")
        print(f"Alfabeto: ({','.join(self.alfabeto)})")
        
        print("Transições:")
        for transicao in self.transicoes:
            transicao.printar()
        print("------------------------------------")

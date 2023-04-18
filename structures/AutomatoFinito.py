from Tipos import TipoArquivo, Elemento

class AutomatoFinito(Elemento):
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao) -> None:
        super().__init__(TipoArquivo.AF)
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao
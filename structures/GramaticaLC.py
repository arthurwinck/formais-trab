from Tipos import TipoArquivo, Elemento

class GramaticaLC(Elemento):
    def __init__(self, nao_terminais, terminais, producoes, simbolo_inicial) -> None:
        super().__init__(TipoArquivo.GLC)
        self.nao_terminais = nao_terminais,
        self.terminais = terminais,
        self.producoes = producoes,
        self.simbolo_inicial = simbolo_inicial
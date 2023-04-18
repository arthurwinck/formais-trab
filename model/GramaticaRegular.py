from Tipos import TipoArquivo, Elemento

class GramaticaRegular(Elemento):
    def __init__(self, nao_terminais, terminais, producoes, simbolo_inicial) -> None:
        super().__init__(TipoArquivo.GR)    
        self.nao_terminais = nao_terminais,
        self.terminais = terminais,
        self.producoes = producoes,
        self.simbolo_inicial = simbolo_inicial
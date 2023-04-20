from enum import Enum

class TipoArquivo(Enum):
    AF = 1
    AFP = 2
    GR = 3
    GLC = 4
    ER = 5

    def convertTipo(texto: str):
        if texto[0] == "<AF>":
            return TipoArquivo.AF
        elif texto[0] == "<AFP>":
            return TipoArquivo.AFP
        elif texto[0] == "<GR>":
            return TipoArquivo.GR
        elif texto[0] == "<GLC>":
            return TipoArquivo.GLC
        elif texto[0] == "<ER>":
            return TipoArquivo.ER

class Elemento():
    def __init__(self, tipo: TipoArquivo) -> None:
        self.tipo = tipo

    def getTipo(self) -> TipoArquivo:
        return self.tipo

class Transicao():
    def __init__(self, origem=None, destino=None, simbolos=None) -> None:
        self.origem = origem
        self.destino = destino
        if simbolos is None:
            self.simbolos = []

    def printar(self):
        print(f"{self.origem} -({','.join(self.simbolos)})-> {self.destino}")
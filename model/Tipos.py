from enum import Enum
from datetime import datetime

class Tipo(Enum):
    VAZIO = 1
    NULO = 2

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

    def log(self, classe: str, msg: str):
        currentDateAndTime = datetime.now().strftime("%H:%M:%S")
        print(f"{currentDateAndTime} - [{classe}]  - {msg}")

    # Adiciona um elemento em uma lista somente se ele não existe
    # (Usado pra não precisar transformar toda lista em set e vice-versa)
    def appendIfNotExists(self, lista: list, element) -> list:
        setFromLista = set(lista)
        setFromLista.add(element)
        return list(setFromLista)

    def interseccao(self, lista1: list, lista2: list) -> list:
        lista = []
        for item1 in lista1:
            if item1 in lista2:
                lista.append(item1)

        return lista
    
    def interseccaoLista(self, lista1: list, lista2: list) -> list:
        lista = []
        for item1 in lista1:
            if item1 in lista2:
                lista.append(item1)

        return lista

    def diferenca(self, lista1: list, lista2: list) -> list:
        lista = []
        for item1 in lista1:
            if item1 not in lista2:
                lista.append(item1)
        return lista

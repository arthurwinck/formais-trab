from Tipos import TipoArquivo, Elemento

class ExpressaoRegular(Elemento):
    def __init__(self) -> None:
        super().__init__(TipoArquivo.ER)
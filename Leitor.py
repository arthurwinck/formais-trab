from structures.Tipos import TipoArquivo, Elemento
from structures import GramaticaRegular, AutomatoFinito, AutomatoPilha, GramaticaLC, ExpressaoRegular

class Leitor:
    def __init__(self, arquivo: str):
        self.arquivo = arquivo

    def ler(self) -> Elemento:
        arquivo = open(self.arquivo)
        texto = arquivo.read().split("\n")
        tipo = self.pegarTipo(texto)
        
        #TODO - Criar Elemento -> (AF, AFP, ER, GR, GLC) e devolver

    def pegarTipo(self, texto) -> TipoArquivo:
        TipoArquivo.convertTipo(texto)

leitor = Leitor(".arquivos/dale.txt")
leitor.ler()
from .Tipos import TipoArquivo
from .Automato import Automato

class AutomatoPilha(Automato):
    def __init__(self, estados=None, alfabeto=None, transicoes=None, estado_inicial=None, estados_aceitacao=None) -> None:
        super().__init__(TipoArquivo.AFP, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)
        
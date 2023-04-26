from .Tipos import TipoArquivo, Tipo
from .Automato import Automato

class AutomatoFinito(Automato):
    def __init__(self, estados=None, alfabeto=None, transicoes=None, estado_inicial=None, estados_aceitacao=None) -> None:
        super().__init__(TipoArquivo.AF, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)
 
    def determinizar(self) -> None:
        # Armazenar transicoes originais do automato
        refTransicoes = self.transicoes
        novasTransicoes = None

        if self.checkEFecho():
            transicoesEFecho = self.calcularEFecho()
            
            for estado in transicoesEFecho:
                listaEstadosEF = list(transicoesEFecho[estado])
                listaEstadosEF.sort()
                
                novoEstado = ",".join(listaEstadosEF)
                

                # Com o novo estado, calcular novas transições e estados. Caso o estado não exista, adicionar ela na lista de estados.
                #checkTransicoesEFecho

    # Sigma Fecho de um estado é o próprio estado + todos os estados 
    # que eu alcanço de um modo recursivo a partir de transições & 
    def checkEFecho(self) -> bool:
        for i in range(len(self.estados)):
            for j in range(len(self.estados)):
                if '&' in self.transicoes[i][j]:
                    return True

        return False
    
    def calcularEFecho(self) -> dict:
        dicEstadosEFecho = {}
        for estado in self.estados:
            setEstadosEFecho = set()
            setEstadosEFecho.add(estado)
            dicEstadosEFecho[estado] = self.findETransicao(estado, setEstadosEFecho)

        return dicEstadosEFecho

    def checkEstadoFinal(self, estadoSet: set) -> bool:
        for final in self.estados_aceitacao:
            return True
        return False

    def findETransicao(self, estado: str, setEstadosEFecho: set) -> set:
        for i in range(len(self.estados)):
            for j in range(len(self.estados)):
                if '&' in self.transicoes[i][j] and self.estados[i] == estado:
                    # Adiciono o estado destino pois fará parte do conjunto sigma fecho desse estado
                    setEstadosEFecho.add(self.estados[j])
                    # Parte da função recursiva que irá testar novamente todas as transições pro novo estado capturado
                    setEstadosEFecho.union(self.findETransicao(self.estados[j], setEstadosEFecho))

        return setEstadosEFecho
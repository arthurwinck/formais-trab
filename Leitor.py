from model.Tipos import Elemento, TipoArquivo
from model.GramaticaLC import GramaticaLC
from model.GramaticaRegular import GramaticaRegular
from model.AutomatoFinito import AutomatoFinito
from model.ExpressaoRegular import ExpressaoRegular
from model.AutomatoPilha import AutomatoPilha


class Leitor:
    def __init__(self, arquivo: str):
        self.arquivo = arquivo

    def ler(self) -> Elemento:
        arquivo = open(self.arquivo)
        texto = arquivo.read().split("\n")
        tipo = self.pegarTipo(texto)
        elemento = self.criarElemento(tipo, texto)

        return elemento

    def pegarTipo(self, texto) -> TipoArquivo:
        return TipoArquivo.convertTipo(texto)

    def criarElemento(self, tipo: TipoArquivo, texto: str) -> Elemento:
        if tipo == TipoArquivo.AF or tipo == TipoArquivo.AFP:
            return self.criarAutomato(tipo, texto)
        elif tipo == TipoArquivo.GLC or tipo == TipoArquivo.GR:
            return self.criarGramatica(tipo, texto)
        elif tipo == TipoArquivo.ER:
            return self.criarExpressao(tipo, texto)
        else:
            raise Exception("Esse elemento não é de nenhum tipo")

    def criarAutomato(self, tipo: TipoArquivo, texto: str) -> Elemento:
        estados = self.pegarEstados(texto)
        alfabeto = self.pegarAlfabeto(texto)
        transicoes = self.pegarTransicoes(texto)
        estado_inicial = self.pegarEstadoInicial(texto)
        estados_aceitacao = self.pegarEstadosAceitacao(texto)
        automato = None

        if tipo == TipoArquivo.AF:
            automato = AutomatoFinito(
                estados, alfabeto, transicoes,
                estado_inicial, estados_aceitacao)
        elif tipo == TipoArquivo.AFP:
            automato = AutomatoPilha(
                estados, alfabeto, transicoes, 
                estado_inicial, estados_aceitacao)

        return automato

    def criarGramatica(self, tipo: TipoArquivo, texto: str) -> Elemento:
        nao_terminais = self.pegarNaoTerminais(texto)
        terminais = self.pegarTerminais(texto)
        producoes = self.pegarProducoes(texto)
        simbolo_inicial = self.pegarSimboloInicial(texto)

        gramatica = None

        if (tipo == TipoArquivo.GR):
            gramatica = GramaticaRegular(
                nao_terminais, terminais, producoes, simbolo_inicial)
        elif (tipo == TipoArquivo.GLC):
            gramatica = GramaticaLC(
                nao_terminais, terminais, producoes, simbolo_inicial)

        return gramatica

    def criarExpressao(self, tipo: TipoArquivo, texto: str) -> Elemento:
        alfabeto = self.pegarAlfabeto(texto)
        expressao = self.pegarExpressao(texto)

        expressaoRegular = ExpressaoRegular(alfabeto, expressao)

        return expressaoRegular

    def pegarEstados(self, texto):
        indice = texto.index('<estados>')
        return texto[indice+1].split()

    def pegarEstadoInicial(self, texto):
        indice = texto.index('<estado_inicial>')
        return texto[indice+1].split()

    def pegarEstadosAceitacao(self, texto):
        indice = texto.index('<estados_aceitacao>')
        return texto[indice+1].split()

    def pegarAlfabeto(self, texto):
        indice = texto.index('<alfabeto>')
        return texto[indice+1].split()

    def pegarTransicoes(self, texto):
        indice = texto.index('<transicoes>')
        return texto[indice+1:]

    # Gramáticas

    def pegarNaoTerminais(self, texto):
        indice = texto.index('<nao_terminais>')
        return texto[indice+1].split()

    def pegarTerminais(self, texto):
        indice = texto.index('<terminais>')
        return texto[indice+1].split()

    def pegarSimboloInicial(self, texto):
        indice = texto.index('<simbolo_inicial>')
        return texto[indice+1]

    # Porque aqui é -1?
    def pegarProducoes(self, texto):
        indice = texto.index('<producoes>')
        return texto[indice+1:]

    # Expressões Regulares

    def pegarExpressao(self, texto):
        indice = texto.index('<expressao>')
        return texto[indice+1]


if __name__ == "__main__":

    # AF -----------------------------
    # leitorAFND = Leitor("./arquivos/automatos/afnd_moodle_1.txt")
    # afnd = leitorAFND.ler()
    # print("AFND Inicial ---------------")
    # afnd.printar()
    # afnd.determinizar()
    # print("AFD Determinizado ---------------")
    # afnd.printar()
    # afnd.minimizar()
    # print("AFD MINIMIZADO ---------------")
    # afnd.printar()

    # GLC -----------------------------
    leitorGLC = Leitor("./testes/gramaticas/glc.txt")
    glc = leitorGLC.ler()
    
    print(glc.calcularFollow(dictFirst=None))
    #print(glc.resolverNaoDeterminismoDireto())
    #glc.printar()
    
    #glc.printar()

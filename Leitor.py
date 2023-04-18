from model.Tipos import TipoArquivo, Elemento
from model import GramaticaRegular, AutomatoFinito, AutomatoPilha, GramaticaLC, ExpressaoRegular

class Leitor:
    def __init__(self, arquivo: str):
        self.arquivo = arquivo

    def ler(self) -> Elemento:
        arquivo = open(self.arquivo)
        texto = arquivo.read().split("\n")
        tipo = self.pegarTipo(texto)
        automato = self.criarElemento(tipo, texto)
        
    def pegarTipo(self, texto) -> TipoArquivo:
        TipoArquivo.convertTipo(texto)

    def criarElemento(self, tipo: TipoArquivo, texto: str) -> Elemento:
        if tipo == TipoArquivo.AF or tipo == TipoArquivo.AFP:
            return self.criarAutomato(tipo, texto)
        elif tipo == TipoArquivo.GLC or tipo == TipoArquivo.GR:
            return self.criarGramatica(tipo, texto)
        elif tipo == TipoArquivo.ER:
            return self.criarExpressao(tipo, texto)

    def criarAutomato(self, tipo: TipoArquivo, texto: str) -> Elemento:
        estados = self.pegarEstados(texto)
        alfabeto = self.pegarAlfabeto(texto)
        transicoes = self.pegarTransicoes(texto)
        estado_inicial = self.pegarEstadoInicial(texto)
        estados_aceitacao = self.pegarEstadosAceitacao(texto)

        automato = None

        if tipo == TipoArquivo.AF:
            automato = AutomatoFinito(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)           
        elif tipo == TipoArquivo.AFP:
            automato = AutomatoPilha(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)

        return automato

    def criarGramatica(self, tipo: TipoArquivo, texto: str) -> Elemento:
        nao_terminais = self.pegarNaoTerminais(texto)
        terminais = self.pegarTerminais(texto)
        producoes = self.pegarProducoes(texto)
        simbolo_inicial = self.pegarSimboloInicial(texto)

        gramatica = None

        if (tipo == TipoArquivo.GR):
            gramatica = GramaticaRegular(nao_terminais, terminais, producoes, simbolo_inicial)
        elif (tipo == TipoArquivo.GLC):
            gramatica = GramaticaLC(nao_terminais, terminais, producoes, simbolo_inicial)

        return gramatica

    def criarExpressao(self, tipo: TipoArquivo, texto: str) -> Elemento:
        alfabeto = self.pegarAlfabeto(texto)
        expressao = self.pegarExpressao(texto)

        expressaoRegular = ExpressaoRegular(alfabeto,expressao)

        return expressaoRegular

    def pegarEstados(self, texto):
        indice = texto.index('<estados>')
        return texto[indice+1].split()

    def pegarEstadoInicial(self, texto):
        indice = texto.index('<estado_inicial>')
        return texto[indice+1].split()

    def pegarEstadoAceitacao(self, texto):
        indice = texto.index('<estados_aceitacao>')
        return texto[indice+1].split()

    def pegarAlfabeto(self, texto):
        indice = texto.index('<alfabeto>')
        return texto[indice+1].split()

    def pegarTransicoes(self, texto):
        indice = texto.index('<transicoes>')
        return texto[indice+1:].split()

    # Gramáticas

    def pegarNaoTerminais(self, texto):
        indice = texto.index('*<nao_terminais>')
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
        return texto[indice+1:-1]
    
    # Expressões Regulares

    def pegarExpressao(self, texto):
        indice = texto.index('<expressao>')
        return texto[indice+1]
    


leitor = Leitor(".arquivos/dale.txt")
leitor.ler()
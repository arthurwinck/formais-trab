import os
import Leitor
from model.Tipos import Elemento, TipoArquivo
from model.GramaticaLC import GramaticaLC
from model.GramaticaRegular import GramaticaRegular
from model.AutomatoFinito import AutomatoFinito
from model.ExpressaoRegular import ExpressaoRegular
from model.AutomatoPilha import AutomatoPilha

class Menu():
    def __init__(self) -> None:
        arquivo = ""
        arquivo2 = ""

    def getArquivo(self):
        return self.arquivo
    
    def getArquivo2(self):
        return self.arquivo2

menu = Menu()

def espera():
    print()
    print("--------------------------------")
    enter = input("Pressione ENTER para retornar ao menu.")
    print("\n")

def escolherArquivo(principal, operacao):
    if principal:
        nome = input("\nDigite o nome do arquivo (sem a extensão):\n")
        menu.arquivo = (nome + ".txt")
        print("\nArquivo escolhido:", menu.arquivo, "\n")
    else:
        print("\nDigite o nome do segundo arquivo para realizar", operacao, "(sem a extensão):")
        nome = input()
        menu.arquivo2 = (nome + ".txt")
        print("\nArquivo escolhido:", menu.arquivo2, "\n")

def verificaArquivosAutomatos():
    pasta = './testes/automatos'
    for diretorio, subpastas, arquivos in os.walk(pasta):
        print("Autômatos de teste disponíveis:")
        for arquivo in arquivos:
            print(arquivo)

def verificaArquivosGramaticas():
    pasta = './testes/gramaticas'
    for diretorio, subpastas, arquivos in os.walk(pasta):
        print("Gramáticas de teste disponíveis:")
        for arquivo in arquivos:
            print(arquivo)

def verificaTodosArquivos():
    print("Arquivos:\n")
    verificaArquivosAutomatos()
    print()
    verificaArquivosGramaticas()

#verificaTodosArquivos()

# ------------- MENU PRINCIPAL --------------

while True:

    print("---------------------- MENU ----------------------\n")

    print("Digite o número correspondente à operação")
    print("1 - Autômatos") # - Vericar e selecionar arquivos de teste de autômatos disponíveis")
    print("2 - Gramáticas") # - Vericar e selecionar arquivos de teste de gramáticas disponíveis")
    #print("3 - Vericar todos os arquivos de teste disponíveis")
    print("0 - Sair")
    

    n = int(input("\nDigite:"))
    print()
    print("--------------------------------\n")

    if n == 0:
        break

    # -------- MENU AUTÔMATOS ---------
    elif n == 1:
        
        verificaArquivosAutomatos()
        escolherArquivo(True, None)

        while True:
            print("\n------------ MENU AUTÔMATOS -------------\n")
            print("1 - Determinização")
            print("2 - Converter para Gramática")
            print("3 - Minimização")
            print("4 - União")
            print("5 - Interseção")
            print("0 - Retornar ao Menu Principal\n")
            na = int(input("Digite o número da operação desejada:\n"))
            print()

            if na == 0:
                break
            elif na == 1:
                # Chamar determinização
                # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO
                pass
            elif na == 2:
                # Chamar conversão para gramática
                # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO
                pass
            elif na == 3:
                # Chamar minimização
                # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO
                pass
            elif na == 4:
                verificaArquivosAutomatos()
                escolherArquivo(False, "união")

                l1 = Leitor.Leitor("./testes/automatos/"+ str(menu.getArquivo()))
                automato = l1.ler()
                l2 = Leitor.Leitor("./testes/automatos/"+ str(menu.getArquivo2()))
                automato2 = l1.ler()

                automato.unir(automato2)
                automato.printar()
                espera()
                # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO

            elif na == 5:
                verificaArquivosAutomatos()
                escolherArquivo(False, "interseção")

                l1 = Leitor.Leitor("./testes/automatos/"+ str(menu.getArquivo()))
                automato = l1.ler()
                l2 = Leitor.Leitor("./testes/automatos/"+ str(menu.getArquivo2()))
                automato2 = l1.ler()

                automato.intersecao(automato2)
                automato.printar()
                espera()
                # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO

            else:
                print("Opção não disponível. Verifique o número digitado.")
                espera()
    
    # -------- MENU GRAMÁTICAS ---------
    elif n == 2:

        verificaArquivosGramaticas()
        escolherArquivo(True, None)

        while True:
            print("\n------------ MENU GRAMÁTICAS -------------\n")
            print("1 - Converter para AFND")
            print("2 - Reconhecimento de Sentenças")
            print("0 - Retornar ao Menu Principal\n")
            na = int(input("Digite o número da operação desejada:\n"))

            if na == 0:
                break
            elif na == 1:
                # Chamar conversão para AFND
                pass
            elif na == 2:
                # Chamar Reconheicmento de Sentenças
                pass
            else:
                print("Opção não disponível. Verifique o número digitado.")
                espera()

    elif n == 3:
        verificaTodosArquivos()
        espera()
    elif n == 4:
        pass
    elif n == 5:
        pass
    elif n == 6:
        pass
    elif n == 7:
        pass
    elif n == 8:
        pass
    elif n == 9:
        pass
    else:
        print("Opção não disponível. Verifique o número digitado.")
        espera()
    
    

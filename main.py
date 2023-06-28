import os
import Leitor


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
    enter = input("Pressione ENTER para retornar ao menu.\n")

def erro():
    print("Não foi possível realizar a operação, verifique os arquivos de entrada e tente novamente.")

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

            elif na == 1: # Determinização
                try:
                    print("\n--- Determinização ---\n")
                    l1 = Leitor.Leitor("./testes/automatos/"+ str(menu.getArquivo()))
                    automato = l1.ler()
                    automato.determinizar()
                    espera()
                    #automato.printar() # não precisa printar, determinizar() já está printando
                    # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO
                except:
                    erro()
                    espera()
                
            elif na == 2: # Conversão para Gramática
                try:
                    print("\n--- Conversão para Gramática ---\n")
                    l1 = Leitor.Leitor("./testes/automatos/"+ str(menu.getArquivo()))
                    automato = l1.ler()
                    espera()
                    # Chamar conversão para gramática
                    # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO
                except:
                    erro()
                    espera()

            elif na == 3: # Minimização
                try:
                    print("\n--- Minimização ---\n")
                    l1 = Leitor.Leitor("./testes/automatos/"+ str(menu.getArquivo()))
                    automato = l1.ler()
                    automato.minimizar()
                    automato.printar()
                    espera()
                    # Chamar minimização
                    # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO
                except:
                    erro()
                    espera()

            elif na == 4: # União
                try:
                    print("\n--- União ---\n")
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
                except:
                    erro()
                    espera()

            elif na == 5: # Interseção
                try:
                    print("\n--- Interseção ---\n")
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
                except:
                    erro()
                    espera()

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
            print("2 - Eliminação de Não-determinismo")
            print("3 - Fatoração")
            print("4 - Eliminação de Recursão à Esquerda")
            print("5 - Firsts e Follows")
            print("6 - Construção da Tabela LL(1)")
            print("7 - Simulação de Pilha")
            print("0 - Retornar ao Menu Principal\n")
            na = int(input("Digite o número da operação desejada:\n"))

            if na == 0:
                break

            elif na == 1: # Conversão para AFND
                try:
                    print("\n--- Conversão para AFND ---\n")
                    # Chamar conversão para AFND
                    espera()
                    # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO
                except:
                    erro()
                    espera()

            elif na == 2: # Eliminação de Não-determinismo
                try:
                    print("\n--- Eliminação de Não-determinismo ---\n")
                    # Chamar 
                    espera()
                    # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO
                except:
                    erro()
                    espera()

            elif na == 3: # Fatoração
                try:
                    print("\n--- Fatoração ---\n")
                    # Chamar 
                    espera()
                    # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO
                except:
                    erro()
                    espera()

            elif na == 4: # Eliminação de Recursão à Esquerda
                try:
                    print("\n--- Eliminação de Recursão à Esquerda ---\n")
                    # Chamar 
                    espera()
                    # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO
                except:
                    erro()
                    espera()

            elif na == 5: # Firsts e Follows
                try:
                    print("\n--- Firsts e Follows ---\n")
                    leitorGLC = Leitor.Leitor("./testes/gramaticas/"+ str(menu.getArquivo()))
                    glc = leitorGLC.ler()
                    glc.printar()
                    espera()
                    # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO
                except:
                    erro()
                    espera()

            elif na == 6: # Construção da Tabela LL(1)
                try:
                    print("\n--- Construção da Tabela LL(1) ---\n")
                    # Chamar 
                    espera()
                    # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO
                except:
                    erro()
                    espera()

            elif na == 7: # Simulação de Pilha
                try:
                    print("\n--- Simulação de Pilha ---\n")
                    # Chamar 
                    espera()
                    # ADICIONAR OPÇÃO DE EXPORTAR RESULTADO
                except:
                    erro()
                    espera()

            else:
                print("Opção não disponível. Verifique o número digitado.")
                espera()

    else:
        print("Opção não disponível. Verifique o número digitado.")
        espera()
    
    

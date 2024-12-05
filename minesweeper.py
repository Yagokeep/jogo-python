import random
import os

def salvar_pontuacao(nome, pontuacao):
    """Salva o nome e a pontuação no arquivo de ranking."""
    with open("ranking_campo_minado.txt", "a") as arquivo:
        arquivo.write(f"{nome},{pontuacao}\n")

def exibir_ranking():
    """Exibe o ranking de jogadores."""
    try:
        with open("ranking_campo_minado.txt", "r") as arquivo:
            pontuacoes = [linha.strip().split(",") for linha in arquivo.readlines()]
        pontuacoes.sort(key=lambda x: int(x[1]), reverse=True)  # Ordena pelo maior número de pontos
        print("\nRanking dos Jogadores:")
        for i, (nome, pontos) in enumerate(pontuacoes, 1):
            print(f"{i}. {nome} - {pontos} pontos")
    except FileNotFoundError:
        print("\nNenhum ranking disponível. Jogue para criar um!")

def inicializar_tabuleiro(tamanho, minas):
    """Inicializa o tabuleiro e coloca as minas."""
    tabuleiro = [[" " for _ in range(tamanho)] for _ in range(tamanho)]
    minas_posicoes = set()

    while len(minas_posicoes) < minas:
        linha = random.randint(0, tamanho - 1)
        coluna = random.randint(0, tamanho - 1)
        minas_posicoes.add((linha, coluna))

    for linha, coluna in minas_posicoes:
        tabuleiro[linha][coluna] = "*"

    return tabuleiro, minas_posicoes

def exibir_tabuleiro(tabuleiro, visivel, revelar=False):
    """Exibe o tabuleiro."""
    os.system("cls" if os.name == "nt" else "clear")
    tamanho = len(tabuleiro)
    print("   " + "   ".join(map(str, range(tamanho))))
    for i in range(tamanho):
        linha_exibida = []
        for j in range(tamanho):
            if revelar or visivel[i][j]:
                linha_exibida.append(tabuleiro[i][j])
            else:
                linha_exibida.append(" ")
        print(f"{i}  " + " | ".join(linha_exibida))
        if i < tamanho - 1:
            print("  " + "---|" * (tamanho - 1) + "---")

def contar_minas_vizinhas(tabuleiro, linha, coluna):
    """Conta o número de minas ao redor de uma célula."""
    tamanho = len(tabuleiro)
    direcoes = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1),          (0, 1),
                (1, -1),  (1, 0), (1, 1)]
    contador = 0

    for d_linha, d_coluna in direcoes:
        nova_linha, nova_coluna = linha + d_linha, coluna + d_coluna
        if 0 <= nova_linha < tamanho and 0 <= nova_coluna < tamanho:
            if tabuleiro[nova_linha][nova_coluna] == "*":
                contador += 1

    return contador

def revelar_celula(tabuleiro, visivel, linha, coluna):
    """Revela uma célula do tabuleiro."""
    if visivel[linha][coluna]:
        return 0  # Célula já revelada

    visivel[linha][coluna] = True
    if tabuleiro[linha][coluna] == "*":
        return -1  # Acertou uma mina

    # Contar minas vizinhas e atualizar a célula
    minas_vizinhas = contar_minas_vizinhas(tabuleiro, linha, coluna)
    tabuleiro[linha][coluna] = str(minas_vizinhas) if minas_vizinhas > 0 else " "

    # Se não há minas vizinhas, revelar células adjacentes
    if minas_vizinhas == 0:
        tamanho = len(tabuleiro)
        direcoes = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),          (0, 1),
                    (1, -1),  (1, 0), (1, 1)]
        for d_linha, d_coluna in direcoes:
            nova_linha, nova_coluna = linha + d_linha, coluna + d_coluna
            if 0 <= nova_linha < tamanho and 0 <= nova_coluna < tamanho:
                revelar_celula(tabuleiro, visivel, nova_linha, nova_coluna)

    return 1  # Célula revelada com sucesso

def jogo_campo_minado():
    """Executa o jogo do Campo Minado."""
    print("Bem-vindo ao Campo Minado!")
    nome = input("Digite seu nome: ").strip()

    while True:
        print("\nEscolha o modo de jogo:")
        print("1. Fácil (5x5 com 5 minas)")
        print("2. Difícil (9x9 com 10 minas)")
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == "1":
            tamanho, minas = 5, 5
            break
        elif escolha == "2":
            tamanho, minas = 9, 10
            break
        else:
            print("Opção inválida. Tente novamente.")

    while True:  # Laço para permitir reiniciar o jogo após acertar uma mina
        tabuleiro, minas_posicoes = inicializar_tabuleiro(tamanho, minas)
        visivel = [[False for _ in range(tamanho)] for _ in range(tamanho)]

        pontos = 0
        perdeu = False
        while not perdeu:
            exibir_tabuleiro(tabuleiro, visivel)
            print(f"Pontos: {pontos}")
            try:
                entrada = input("Digite a linha e a coluna (separadas por espaço): ").split()
                if len(entrada) != 2:
                    raise ValueError
                linha, coluna = map(int, entrada)
                if not (0 <= linha < tamanho and 0 <= coluna < tamanho):
                    print("Coordenadas fora do tabuleiro. Tente novamente.")
                    continue
                if visivel[linha][coluna]:
                    print("Essa célula já foi revelada. Tente outra.")
                    continue
                resultado = revelar_celula(tabuleiro, visivel, linha, coluna)
                if resultado == -1:
                    exibir_tabuleiro(tabuleiro, visivel, revelar=True)
                    print("\nVocê acertou uma mina! Fim de jogo.")
                    perdeu = True
                    break
                pontos += resultado
                # Verificar se o jogador ganhou
                if all(visivel[i][j] or tabuleiro[i][j] == "*" for i in range(tamanho) for j in range(tamanho)):
                    exibir_tabuleiro(tabuleiro, visivel, revelar=True)
                    print("\nParabéns! Você revelou todas as células sem minas!")
                    break
            except ValueError:
                print("Entrada inválida. Digite dois números inteiros separados por espaço.")

        salvar_pontuacao(nome, pontos)
        print(f"Pontuação final: {pontos}")
        continuar = input("\nDeseja tentar novamente? (s/n): ").strip().lower()
        if continuar != "s":
            break

def main():
    """Menu principal do jogo."""
    while True:
        print("\nMenu do Campo Minado")
        print("1. Jogar")
        print("2. Exibir Ranking")
        print("3. Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            jogo_campo_minado()
        elif escolha == "2":
            exibir_ranking()
        elif escolha == "3":
            print("Obrigado por jogar.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

#considerações para o Edécio: o jogo usa listas e matrizes para estruturar o tabuleiro do Campo Minado, 
#rastrear os espaços visiveis e manipular as posições das minas, 
#"""""" foram usados para explicar funções e # para o resto
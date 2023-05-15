import pygame
import sys
from mapa import mapa
import math
from collections import deque
import pygame.font

# Configurações do mapa
LARGURA_TELA = 800
ALTURA_TELA = 600
COR_FUNDO = (255, 255, 255)
COR_NOS = (255, 0, 0)
COR_PAREDES = (0, 0, 255)
COR_ARESTAS = (0, 0, 0)
TAMANHO_CELULA = 20

# Inicializa o Pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Mapa")

# Calcula o tamanho do mapa
largura_mapa = len(mapa[0])
altura_mapa = len(mapa)

# Calcula o deslocamento necessário para centralizar o mapa
deslocamento_x = (LARGURA_TELA - largura_mapa * TAMANHO_CELULA) // 2
deslocamento_y = (ALTURA_TELA - altura_mapa * TAMANHO_CELULA) // 2

# Variáveis para armazenar os nós selecionados como início e final
no_inicio = None
no_final = None

nos_grafo = []

# Função para obter o peso de uma aresta no grafo
def obter_peso_aresta_grafo(x1, y1, x2, y2):
    if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
        # Aresta diagonal (√2)
        return math.sqrt(2)
    else:
        # Aresta vertical ou horizontal (1)
        return 1

# Função para obter os vizinhos de um nó
def obter_vizinhos(x, y):
    vizinhos = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx = x + dx
            ny = y + dy
            if 0 <= nx < largura_mapa and 0 <= ny < altura_mapa and mapa[ny][nx] != "#":
                vizinhos.append((nx, ny))
    return vizinhos

# Função para calcular o caminho mínimo entre o nó de início e o nó final
def dijkstra():
    fila = deque([(no_inicio, 0)])  # Fila de nós a serem visitados
    visitados = set()  # Conjunto de nós visitados
    predecessores = {}  # Dicionário de predecessores para reconstruir o caminho mínimo
    pesos = {}  # Dicionário de pesos acumulados para cada nó

    while fila:
        no, peso_acumulado = fila.popleft()
        x, y = no

        if no == no_final:
            # Encontrou o nó final, retorna o caminho mínimo
            caminho_minimo = []
            while no in predecessores:
                caminho_minimo.append(no)
                no = predecessores[no]
            caminho_minimo.append(no_inicio)
            caminho_minimo.reverse()
            return caminho_minimo

        if no in visitados:
            continue

        visitados.add(no)
        pesos[no] = peso_acumulado

        vizinhos = obter_vizinhos(x, y)
        for vizinho in vizinhos:
            if vizinho not in visitados:
                nx, ny = vizinho
                peso_aresta = obter_peso_aresta_grafo(x, y, nx, ny)
                novo_peso = peso_acumulado + peso_aresta

                if vizinho not in pesos or novo_peso < pesos[vizinho]:
                    predecessores[vizinho] = no
                    pesos[vizinho] = novo_peso
                    fila.append((vizinho, novo_peso))

    return []  # Caso não encontre um caminho mínimo, retorna uma lista vazia

fonte_mensagem = pygame.font.Font(None, 18)

# Loop principal do programa
while True:
    # Preenche a tela com a cor de fundo
    tela.fill(COR_FUNDO)

    # Desenha o mapa
    for y in range(altura_mapa):
        for x in range(largura_mapa):
            if (x, y) == no_inicio:
                # Nó de início selecionado, cor verde
                pygame.draw.circle(tela, (0, 255, 0), ((x * TAMANHO_CELULA) + deslocamento_x + TAMANHO_CELULA // 2, (y * TAMANHO_CELULA) + deslocamento_y + TAMANHO_CELULA // 2), TAMANHO_CELULA // 2)
            elif (x, y) == no_final:
                # Nó final selecionado, cor amarela
                pygame.draw.circle(tela, (255, 255, 0), ((x * TAMANHO_CELULA) + deslocamento_x + TAMANHO_CELULA // 2, (y * TAMANHO_CELULA) + deslocamento_y + TAMANHO_CELULA // 2), TAMANHO_CELULA // 2)
            elif mapa[y][x] == "O":
                # Desenha o nó
                pygame.draw.circle(tela, COR_NOS, ((x * TAMANHO_CELULA) + deslocamento_x + TAMANHO_CELULA // 2, (y * TAMANHO_CELULA) + deslocamento_y + TAMANHO_CELULA // 2), TAMANHO_CELULA // 2)
                nos_grafo.append((x, y))
            elif mapa[y][x] == "#":
                # Desenha a parede
                pygame.draw.rect(tela, COR_PAREDES, ((x * TAMANHO_CELULA) + deslocamento_x, (y * TAMANHO_CELULA) + deslocamento_y, TAMANHO_CELULA, TAMANHO_CELULA))
            else:
                # Desenha as arestas com o peso
                if mapa[y][x] == ".":
                    # Aresta com peso 1
                    pygame.draw.line(tela, COR_ARESTAS, ((x * TAMANHO_CELULA) + deslocamento_x, (y * TAMANHO_CELULA) + deslocamento_y),
                                     (((x + 1) * TAMANHO_CELULA) + deslocamento_x, (y * TAMANHO_CELULA) + deslocamento_y), 1)

    # Verifica se o nó de início e o nó final estão selecionados
    if no_inicio is not None and no_final is not None:
        # Calcula o caminho mínimo
        caminho_minimo = dijkstra()

        # Desenha o caminho mínimo
        for i in range(len(caminho_minimo) - 1):
            x1, y1 = caminho_minimo[i]
            x2, y2 = caminho_minimo[i+1]
            pygame.draw.line(tela, (255, 0, 0), ((x1 * TAMANHO_CELULA) + deslocamento_x + TAMANHO_CELULA // 2, (y1 * TAMANHO_CELULA) + deslocamento_y + TAMANHO_CELULA // 2),
                             ((x2 * TAMANHO_CELULA) + deslocamento_x + TAMANHO_CELULA // 2, (y2 * TAMANHO_CELULA) + deslocamento_y + TAMANHO_CELULA // 2), 10)

        # Calcula o peso das arestas somadas
        peso_total = sum(obter_peso_aresta_grafo(x1, y1, x2, y2) for (x1, y1), (x2, y2) in zip(caminho_minimo, caminho_minimo[1:]))
        # Renderiza e desenha a mensagem na tela
        mensagem = "Caminho mínimo encontrado! (Aperte espaço para resetar)"
        texto_mensagem = fonte_mensagem.render(mensagem, True, (255, 0, 0))
        posicao_mensagem = texto_mensagem.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA - 20))
        tela.blit(texto_mensagem, posicao_mensagem)

    # Atualiza a tela
    pygame.display.flip()

    # Verifica eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Clique do mouse esquerdo
            pos = pygame.mouse.get_pos()
            x = (pos[0] - deslocamento_x) // TAMANHO_CELULA
            y = (pos[1] - deslocamento_y) // TAMANHO_CELULA
            if (0 <= x < largura_mapa) and (0 <= y < altura_mapa) and (x, y) in nos_grafo:
                if no_inicio is None:
                    # Selecionar o nó de início
                    no_inicio = (x, y)
                elif no_final is None and (x, y) != no_inicio:
                    # Selecionar o nó final (diferente do nó de início)
                    no_final = (x, y)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # Pressionar a tecla Enter
            if no_inicio is not None and no_final is not None:
                # Calcular e imprimir o caminho mínimo
                caminho_minimo = dijkstra()
                print("Caminho mínimo:", caminho_minimo)

                # Calcular e imprimir o peso das arestas somadas
                peso_total = sum(obter_peso_aresta_grafo(x1,  y1, x2, y2) for (x1, y1), (x2, y2) in zip(caminho_minimo, caminho_minimo[1:]))
                print("Peso total do caminho mínimo:", peso_total)
            else:
                print("É necessário selecionar o nó de início e o nó final antes de calcular o caminho mínimo.")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Pressionar a tecla Espaço
            no_inicio = None
            no_final = None
            nos_grafo = []
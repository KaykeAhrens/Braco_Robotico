import math
from algoritmos.a_estrela import a_estrela
from algoritmos.dijkstra import dijkstra
from algoritmos.ganancioso import ganancioso
from algoritmos.auxiliar import vertice_caminho
from problemas.braco_robotico import BracoRobotico

def ler_arquivo(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    
    num_bases = int(linhas[0].strip())
    max_pilha = int(linhas[1].strip())
    bases = []
    braco_posicao = None
    
    for i, linha in enumerate(linhas[2:]):
        valores = linha.strip().split()
        if valores[0] == 'B':
            braco_posicao = i
            bases.append([])
        else:
            bases.append([int(x) for x in valores])
    
    return num_bases, max_pilha, bases, braco_posicao

def calcular_custo_movimento(distancia):
    return math.ceil(distancia * 0.75) if distancia >= 3 else distancia

def calcular_custo_caixa(peso):
    return math.ceil(peso / 10)

def movimentar_braco(braco_pos, destino):
    distancia = abs(braco_pos - destino)
    energia = calcular_custo_movimento(distancia)
    direcao = 'E' if destino < braco_pos else 'D'
    return energia, destino, direcao, distancia

def pegar_caixa(bases, braco_pos):
    for i in range(len(bases[braco_pos]) - 1, -1, -1):
        if bases[braco_pos][i] > 0:
            peso = bases[braco_pos].pop(i)
            return peso, calcular_custo_caixa(peso)
    return None, 0

def soltar_caixa(bases, braco_pos, peso):
    bases[braco_pos].append(peso)
    return calcular_custo_caixa(peso)

def organizar_caixas(num_bases, max_pilha, bases, braco_pos):
    movimentos = []
    todas_caixas = []
    for pilha in bases:
        todas_caixas.extend(pilha)
    todas_caixas.sort(reverse=True)
    
    nova_bases = [[] for _ in range(num_bases)]
    destino = 0
    energia_total = 0
    
    for peso in todas_caixas:
        while len(nova_bases[destino]) >= max_pilha:
            destino += 1
        
        energia_mov, braco_pos, direcao, distancia = movimentar_braco(braco_pos, destino)
        energia_total += energia_mov
        movimentos.append(f"{direcao} {distancia} P {energia_mov} # move {direcao} {distancia} casas. Gastou {energia_mov} de energia")
        
        energia_peso = soltar_caixa(nova_bases, destino, peso)
        energia_total += energia_peso
        movimentos.append(f"{direcao} 0 S {peso} {energia_peso} # soltou {peso}kg. Gastou {energia_peso} de energia")
    
    return nova_bases, movimentos, energia_total

def salvar_saida(arquivo_saida, bases, movimentos, energia_total):
    with open(arquivo_saida, 'w') as f:
        for pilha in bases:
            f.write(" ".join(map(str, pilha)) + "\n")
        f.write("# Movimentos do braco\n")
        for mov in movimentos:
            f.write(mov + "\n")
        f.write(f"# Energia total gasta: {energia_total}\n")

def executar_algoritmo(nome, algoritmo, problema):
    print(f"Executando {nome}:\n")
    
    qtd_estados_visitados, no_solucao = algoritmo(problema)

    if no_solucao is None:
        print("Não houve solução para o problema!")
    else:
        caminho = vertice_caminho(no_solucao)
        print("Solução:")
        print(caminho)
        
        custo = no_solucao.custo_total()
        print(f"Custo total do caminho: {custo}")

    print(f"Estados visitados: {qtd_estados_visitados}")
    print("Estado Inicial:")
    problema.imprimir(problema.no_raiz)
    
    if no_solucao is not None:
        print("Estado Final:")
        problema.imprimir(no_solucao)
    print("="*30)

if __name__ == "__main__":
    num_bases, max_pilha, bases, braco_pos = ler_arquivo("entrada.txt")
    nova_bases, movimentos, energia_total = organizar_caixas(num_bases, max_pilha, bases, braco_pos)
    salvar_saida("saida.txt", nova_bases, movimentos, energia_total)

    problema = BracoRobotico()
    executar_algoritmo("A*", a_estrela, problema)
    executar_algoritmo("Dijkstra", dijkstra, problema)
    executar_algoritmo("Greedy", ganancioso, problema)
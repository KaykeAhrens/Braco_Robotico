import random
import numpy as np
from no import No


class BracoRobotico:

    def __init__(self):
      self.caixas = None
      self.no_raiz = None
      self.custo_direita = 0.0
      self.custo_esquerda = 0.0
      self.estado_inicial = np.array([
        3, 0, 0,
        10, 0, 0,
        30, 0, 0,
        0, 0, 0,
        10, 0, 0,
        0, 0, 0,
        40, 0, 0,
        0, 0, 0,
        20, 0, 0,
        0, 0, 0,
        30, 0, 0
      ])

    def iniciar(self):
        self.no_raiz = No(self.estado_inicial)
        self.procurar_caixa(self.no_raiz.estado)
        return self.no_raiz

    def procurar_caixa(self, estado_atual):
        self.caixas = []
        for i in range(3, len(estado_atual)):
            caixa_peso = estado_atual[i]
            if caixa_peso != 0:
                self.caixas.append((i, caixa_peso))

    def imprimir(self, no):
        est = no.estado

        e = "  "
        u = "_"
        e2 = " "
        print(f"""
        \r{e2}{est[5]}{e2}{e}{e2}{est[8]}
        \r{e2}{est[4]}{e2}{e}{e2}{est[7]}
        \r{u}{est[3]}{u}{e}{u}{est[6]}{u}{e}{u}{est[9]}{u}{e}{u}{est[12]}{u}{e}{u}{est[15]}{u}{e}{u}{est[18]}{u}{e}{u}{est[21]}{u}{e}{u}{est[24]}{u}{e}{u}{est[27]}{u}{e}{u}{est[30]}{u}
        """)

    def testar_objetivo(self, no):

        teste = no.estado
        resposta = 0

        for i in range(0, (len(self.caixas)) // 3):
            if teste[(3 * i) + 3] > teste[(3 * i) + 4] > teste[(3 * i) + 5] != 0:
                resposta += 1

        return resposta == (len(self.caixas)) // 3

    def gerar_sucessores(self, no):
        estado = no.estado
        nos_sucessores = []

        posicao = estado[0]  # posicao do braco do robo
        self.custo_direita = 0.0
        self.custo_esquerda = 0.0 # É necessário zerar os custos a cada nova geração para que não acumulem.

        expansoes = [self._direita, self._esquerda]
        random.shuffle(expansoes)

        for expansao in expansoes:
            no_sucessor = expansao(posicao, no)
            if no_sucessor is not None: nos_sucessores.append(no_sucessor)

        return nos_sucessores

    def _direita(self, posicao, no):

        sucessor = np.copy(no.estado)
        self.procurar_caixa(sucessor) # atualizar as posições das caixas

        valores_direita = [tupla[0] for tupla in self.caixas if tupla[0] > 8] # olha para valores depois do espaço reservado para empilhamento
        if valores_direita:

            random.shuffle(valores_direita)
            posicao_nova_caixa = valores_direita[0]
            self.custo_direita += self.pegar_caixa(sucessor, posicao_nova_caixa)

            self.colocar_caixa(sucessor)

            return No(sucessor, no, f"""{no.estado[posicao_nova_caixa]}➡️""")
        else:
            None

    def _esquerda(self, posicao, no):

        sucessor = np.copy(no.estado)
        self.procurar_caixa(sucessor)

        valores_esquerda = [tupla[0] for tupla in self.caixas if tupla[0] < 9] # olha para os valores reservados para empilhamento
        if valores_esquerda:

            posicao_nova_caixa = max(valores_esquerda)
            self.custo_esquerda += self.pegar_caixa(sucessor, posicao_nova_caixa)

            self.desempilhar_caixa(sucessor)

            return No(sucessor, no, f"""{no.estado[posicao_nova_caixa]}⬅️""")
        else:
            None

    def pegar_caixa(self, no_sucessor, nova_posicao):

        custo = 0.0

        custo += self.calculo_custo(no_sucessor, nova_posicao)
        custo += no_sucessor[nova_posicao] / 10  # custo do peso da caixa

        no_sucessor[0] = nova_posicao
        no_sucessor[1], no_sucessor[nova_posicao] = no_sucessor[nova_posicao], no_sucessor[1]

        return custo

    def colocar_caixa(self, no_sucessor):
        posicao_livre = None

        for i in range(3, 9):
            if no_sucessor[i] == 0:  # procura o próximo valor livre pra empilhar
                posicao_livre = i
                break

        self.custo_direita += self.calculo_custo(no_sucessor, posicao_livre)

        no_sucessor[0] = posicao_livre

        no_sucessor[posicao_livre], no_sucessor[1] = no_sucessor[1], no_sucessor[posicao_livre]

    def desempilhar_caixa(self, no_sucessor):
        posicao_livre = None

        for i in range(9, 31, 3):
            if no_sucessor[i] == 0:  # procura o espaço vazio na esteira mais proximo à direita para deixar a caixa
                posicao_livre = i
                break

        self.custo_esquerda += self.calculo_custo(no_sucessor, posicao_livre)

        no_sucessor[0] = posicao_livre

        no_sucessor[posicao_livre], no_sucessor[1] = no_sucessor[1], no_sucessor[posicao_livre]

    def calculo_custo(self, pos_atual, pos_meta):  # calcula o custo do movimento
        if abs((pos_atual[0] // 3) - (pos_meta // 3)) == 1: 
            return 1.0  # retorna custo 1 se o braço só andar uma posição em relação a esteira
        else:
            return abs((pos_atual[0] // 3) - (pos_meta // 3)) * 0.75  # retorna a quantidade de posições de ESTEIRA que ele andou * 0,75

    def custo(self, no, no_sucessor):

        custo_total = 0.0

        if no_sucessor.estado[0] > 8:  # se o braço estiver DEPOIS das pilhas reservadas para empilhamento, significa que ele DESEMPILHOU uma caixa, ou seja, se atribui o custo do movimento para esquerda.
            custo_total = self.custo_esquerda
            self.custo_esquerda = 0.0
        else:
            custo_total = self.custo_direita  # se o braço estiver DENTRO das pilhas reservadas para empilhamento, significa que ele acabou de EMPILHAR uma caixa, ou seja, se atribui o custo do movimento para direita.
            self.custo_direita = 0.0

        return custo_total

    def heuristica(self, no):
        estado = no.estado
        resultado = [[40, 30, 10], [30, 20, 10], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                     [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        estado_matriz = [estado[3:6], estado[6:9], estado[9:12], estado[12:15], estado[15:18],
                         estado[18:21], estado[21:24], estado[24:27], estado[27:30], estado[30:33]]

        soma = 0

        for i in range(len(resultado)):
            for j in range(len(resultado[i])):
                valor = resultado[i][j]
                soma = soma + self._distancia_manhattan(valor, estado_matriz, i, j)

        return soma

    # Distância de Manhattan: d = |xi-xj| + |yi-yj|
    def _distancia_manhattan(self, valor, estado, i, j):
      for k in range(len(estado)):
        for h in range(len(estado[k])):
          if valor == estado[k][h]: return abs(i - k) + abs(j - h)

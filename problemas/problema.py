class Problema:
  # Função auxiliar para imprimir
  # deve retornar o nó raiz
  def iniciar(self):
    raise NotImplementedError

  # Função auxiliar para imprimir
  # deve retornar uma string de como
  # imprimir cada estado
  def imprimir(self, no):
    estado = no.estado
    return estado

  # Função booleana que verifica se o estado atual
  # é o estado objetivo do problema
  def testar_objetivo(self, no):
    raise NotImplementedError

  # Função que gera os sucessores válidos
  # a partir de um estado válido
  # deve retornar uma lista de nós sucessores
  def gerar_sucessores(self, no):
    raise NotImplementedError

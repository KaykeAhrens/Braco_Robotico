class Pilha:
    def __init__(self):
        self.pilha = []

    def push(self, item):
        self.pilha.append(item)

    def pop(self):
        if (self.esta_vazio()):
            return None
        else:
            return self.pilha.pop()

    def esta_vazio(self):
        return len(self.pilha) == 0

    def esta_sem_caixa(self):
        for item in self.pilha:
            if item is not None:
                return False
        return True

    def tamanho(self):
        return len(self.pilha)

    def ultimo_valor(self):
        return self.pilha[self.tamanho() - 1]

    def primeiro_valor(self):
        return self.pilha[0]

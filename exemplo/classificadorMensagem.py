import random

def loadComent():
    depre = open('depressao.txt', 'r', encoding='utf8')
    naoDepre = open('naodepressao.txt', 'r', encoding='utf8')
    depressao = depre.read().split('\n')
    naoDepressao = naoDepre.read().split('\n')
    return depressao, naoDepressao

if __name__ == '__main__':
    depressao, naoDepressao = loadComent()

    comentarios = (
        [(coment, 'sim') for coment in depressao] +
        [(coment, 'nao') for coment in naoDepressao]
    )
    random.shuffle(comentarios)
    print(comentarios)

import os

PASTA = 'uploads'

def tentar_matriz(bloco):
    possiveis = [(8,8),(10,10),(12,12),(16,16),(16,8),(8,16)]
    resultados = []

    for x,y in possiveis:
        if x*y == len(bloco):
            resultados.append(f'{x}x{y}')

    return resultados

for nome in os.listdir(PASTA):
    if nome.lower().endswith('.bin'):
        print('\n📁 Arquivo:', nome)

        with open(os.path.join(PASTA, nome), 'rb') as f:
            dados = list(f.read())

        for offset in range(0, len(dados)-256, 256):
            bloco = dados[offset:offset+256]
            formatos = tentar_matriz(bloco)

            if formatos:
                print(f'  📐 0x{offset:X} → possível mapa {formatos}')

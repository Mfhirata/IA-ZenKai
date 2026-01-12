import os

PASTA = 'uploads'

def parece_mapa(bloco):
    diffs = []
    for i in range(len(bloco)-1):
        diffs.append(abs(bloco[i+1] - bloco[i]))

    media = sum(diffs) / len(diffs)
    return media < 20  # limiar empírico

for nome in os.listdir(PASTA):
    if nome.lower().endswith('.bin'):
        print('\n📁 Arquivo:', nome)
        caminho = os.path.join(PASTA, nome)
        with open(caminho, 'rb') as f:
            dados = list(f.read())

        tamanho_bloco = 256
        encontrados = 0

        for i in range(0, len(dados)-tamanho_bloco, tamanho_bloco):
            bloco = dados[i:i+tamanho_bloco]
            if parece_mapa(bloco):
                print(f'  🧩 Possível mapa em 0x{i:X}')
                encontrados += 1

        if encontrados == 0:
            print('  ❌ Nenhuma estrutura clara de mapa encontrada')

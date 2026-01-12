import os

PASTA = 'uploads'

def classificar(bloco):
    diffs = []
    for i in range(len(bloco)-1):
        diffs.append(bloco[i+1] - bloco[i])

    positivos = sum(1 for d in diffs if d > 0)
    negativos = sum(1 for d in diffs if d < 0)
    zeros = sum(1 for d in diffs if d == 0)

    total = len(diffs)

    if zeros / total > 0.4:
        return 'Limitador'
    if positivos / total > 0.6:
        return 'Progressivo / Torque'
    if negativos / total > 0.6:
        return 'Mistura / Correção'

    return 'Suave / Ignição'

for nome in os.listdir(PASTA):
    if nome.lower().endswith('.bin'):
        print('\n📁 Arquivo:', nome)
        with open(os.path.join(PASTA, nome), 'rb') as f:
            dados = list(f.read())

        tamanho = 256

        for i in range(0, len(dados)-tamanho, tamanho):
            bloco = dados[i:i+tamanho]
            tipo = classificar(bloco)
            print(f'  🧠 0x{i:X} → {tipo}')

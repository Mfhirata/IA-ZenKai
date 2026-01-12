import os

PASTA = 'uploads'

def analisar_eixo(valores):
    diffs = [valores[i+1] - valores[i] for i in range(len(valores)-1)]
    if all(d >= 0 for d in diffs):
        return 'crescente'
    if all(d <= 0 for d in diffs):
        return 'decrescente'
    if max(diffs) - min(diffs) < 3:
        return 'quase constante'
    return 'variável'

for nome in os.listdir(PASTA):
    if nome.lower().endswith('.bin'):
        print('\n📁 Arquivo:', nome)

        with open(os.path.join(PASTA, nome), 'rb') as f:
            dados = list(f.read())

        for offset in range(0, len(dados)-256, 256):
            bloco = dados[offset:offset+256]

            eixo_x = bloco[:16]
            eixo_y = bloco[::16][:16]

            tipo_x = analisar_eixo(eixo_x)
            tipo_y = analisar_eixo(eixo_y)

            if tipo_x != 'variável' or tipo_y != 'variável':
                print(f'  📐 0x{offset:X} → eixo X: {tipo_x} | eixo Y: {tipo_y}')

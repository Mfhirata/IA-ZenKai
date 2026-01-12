import os
PASTA = 'uploads'
TAMANHO_BLOCO = 64

def classificar(bloco):
    media = sum(bloco)/len(bloco)
    if media < 40:
        return 'Provável Ignição'
    elif media < 90:
        return 'Provável Combustível / Carga'
    else:
        return 'Provável Torque / Limitador'

for nome in os.listdir(PASTA):
    if nome.lower().endswith('.bin'):
        print('\n📁 Arquivo:', nome)
        with open(os.path.join(PASTA, nome), 'rb') as f:
            dados = f.read()

        for i in range(0, len(dados), TAMANHO_BLOCO):
            bloco = dados[i:i+TAMANHO_BLOCO]
            if len(bloco) < TAMANHO_BLOCO:
                continue
            tipo = classificar(bloco)
            print(f'  Offset 0x{i:X} → {tipo}')

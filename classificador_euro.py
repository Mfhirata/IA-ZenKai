import os

PASTA = 'uploads'

def classificar_ecu(dados):
    tamanho = len(dados)

    score = {
        'Motronic Gasolina (90s)': 0,
        'EDC15 Diesel': 0,
        'EDC16 Diesel': 0,
        'ECU Genérica': 0
    }

    # Tamanho típico
    if tamanho <= 8192:
        score['Motronic Gasolina (90s)'] += 2

    if 65536 <= tamanho <= 262144:
        score['EDC15 Diesel'] += 2

    if tamanho >= 524288:
        score['EDC16 Diesel'] += 2

    # Presença de valores típicos de turbo
    if max(dados) - min(dados) > 120:
        score['EDC15 Diesel'] += 1
        score['EDC16 Diesel'] += 1

    # Injeção simples (gasolina antiga)
    if dados.count(255) > tamanho * 0.05:
        score['Motronic Gasolina (90s)'] += 1

    # Escolha final
    return max(score, key=score.get)

for nome in os.listdir(PASTA):
    if nome.lower().endswith('.bin'):
        caminho = os.path.join(PASTA, nome)
        with open(caminho, 'rb') as f:
            dados = list(f.read())

        print('\n📁 Arquivo:', nome)
        print('🧠 ECU provável:', classificar_ecu(dados))

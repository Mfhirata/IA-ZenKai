import os
import math

PASTA = 'uploads'

def entropia(dados):
    freq = [0]*256
    for b in dados:
        freq[b] += 1
    ent = 0
    for f in freq:
        if f > 0:
            p = f / len(dados)
            ent -= p * math.log2(p)
    return ent

def score_seguranca(dados, combustivel, turbo):
    score = 100

    if combustivel == 'Diesel':
        score -= 15

    if turbo:
        score -= 25

    e = entropia(dados)
    if e > 7.5:
        score -= 20
    elif e > 6.8:
        score -= 10

    if len(dados) < 8192:
        score -= 5

    return max(score, 0)

for nome in os.listdir(PASTA):
    if nome.lower().endswith('.bin'):
        with open(os.path.join(PASTA, nome), 'rb') as f:
            dados = list(f.read())

        combustivel = 'Gasolina'
        turbo = False

        score = score_seguranca(dados, combustivel, turbo)

        print('\n📁 Arquivo:', nome)
        print('🧠 Safety Score:', score, '/ 100')

        if score >= 80:
            print('🟢 Perfil seguro para remap leve')
        elif score >= 60:
            print('🟡 Apenas ajustes conservadores')
        else:
            print('🔴 Alto risco – não recomendado')

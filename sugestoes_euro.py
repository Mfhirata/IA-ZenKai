import os

PASTA = 'uploads'

def gerar_sugestoes(ecu, combustivel, turbo, score):
    sugestoes = []

    if score >= 80:
        nivel = 'leve'
    elif score >= 60:
        nivel = 'conservador'
    else:
        nivel = 'bloqueado'

    if nivel == 'bloqueado':
        sugestoes.append('❌ Remap não recomendado para este arquivo')
        return sugestoes

    if combustivel == 'Gasolina':
        sugestoes.append('⛽ Mistura: +2% a +4% em carga média')
        sugestoes.append('🔥 Ignição: +2° a +4° em alta carga (mapa principal)')

    if combustivel == 'Diesel':
        sugestoes.append('⛽ Injection Quantity: +3% a +6%')
        sugestoes.append('🧯 Smoke Limiter: ajuste proporcional à IQ')

    if turbo:
        sugestoes.append('🌀 Boost: +50 a +120 mbar (máx. europeu seguro)')
        sugestoes.append('🛡️ Torque Limiter: +5% a +10%')

    if nivel == 'conservador':
        sugestoes.append('⚠️ Manter todos os ajustes no limite inferior das faixas')

    return sugestoes

for nome in os.listdir(PASTA):
    if nome.lower().endswith('.bin'):
        print('\n📁 Arquivo:', nome)
        ecu = 'Motronic Gasolina (90s)'
        combustivel = 'Gasolina'
        turbo = False
        score = 85

        sugestoes = gerar_sugestoes(ecu, combustivel, turbo, score)
        for s in sugestoes:
            print('  ➜', s)

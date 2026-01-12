import os

PASTA = 'uploads'

def perfil_motor(dados, ecu):
    perfil = {}

    # Turbo real?
    if max(dados) - min(dados) > 120:
        perfil['turbo'] = True
    else:
        perfil['turbo'] = False

    # Tipo combustível
    if 'Diesel' in ecu:
        perfil['combustivel'] = 'Diesel'
    else:
        perfil['combustivel'] = 'Gasolina'

    # Risco
    if perfil['combustivel'] == 'Gasolina' and not perfil['turbo']:
        perfil['risco'] = '🟢 Baixo'
    elif perfil['turbo']:
        perfil['risco'] = '🟡 Moderado'
    else:
        perfil['risco'] = '🔴 Alto'

    # Recomendações
    if perfil['combustivel'] == 'Gasolina' and not perfil['turbo']:
        perfil['permitido'] = ['Ignição leve', 'Mistura parcial', 'Resposta acelerador']
        perfil['evitar'] = ['Avanço excessivo', 'Mistura pobre', 'Corte de segurança']

    elif perfil['turbo']:
        perfil['permitido'] = ['Boost controlado', 'IQ moderado', 'Torque limiter']
        perfil['evitar'] = ['Boost agressivo', 'Desativar proteções']

    return perfil

for nome in os.listdir(PASTA):
    if nome.lower().endswith('.bin'):
        caminho = os.path.join(PASTA, nome)
        with open(caminho, 'rb') as f:
            dados = list(f.read())

        # ECU já classificada manualmente aqui
        ecu = 'Motronic Gasolina (90s)'
        perfil = perfil_motor(dados, ecu)

        print('\n📁 Arquivo:', nome)
        print('⚙️ Combustível:', perfil['combustivel'])
        print('🌀 Turbo:', 'Sim' if perfil['turbo'] else 'Não')
        print('⚠️ Risco:', perfil['risco'])
        print('✅ Permitido:', ', '.join(perfil['permitido']))
        print('❌ Evitar:', ', '.join(perfil['evitar']))

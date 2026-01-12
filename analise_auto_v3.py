import os, shutil
PASTA_UPLOADS = 'uploads'

arquivos = [f for f in os.listdir(PASTA_UPLOADS) if f.lower().endswith('.bin')]

print('📁 Arquivos disponíveis:')
for i, nome in enumerate(arquivos):
    print(f'{i}: {nome}')

idx = int(input('Escolha o arquivo pelo número: '))
arquivo = arquivos[idx]
caminho = os.path.join(PASTA_UPLOADS, arquivo)

backup = caminho + '.backup'
shutil.copy(caminho, backup)
print('✅ Backup criado:', backup)

with open(caminho, 'rb') as f:
    dados = bytearray(f.read())

def detectar_mapas(dados):
    mapas = []
    # Exemplo de padrão simples: Torque Limiter (valores altos consecutivos)
    for i in range(len(dados)-2):
        if dados[i] > 200 and dados[i+1] > 200:
            mapas.append(('Torque Limiter?', i))
        elif 50 < dados[i] < 100:
            mapas.append(('IQ?', i))
    return mapas

mapas_encontrados = detectar_mapas(dados)
print('🔎 Possíveis mapas encontrados:')
for tipo, off in mapas_encontrados:
    print(f'{tipo} no offset {off:#04X}, valor atual {dados[off]:02X}')

def sugerir_alteracao(tipo, valor_atual):
    if tipo == 'Torque Limiter?':
        return max(0, valor_atual - 10)
    elif tipo == 'IQ?':
        return max(0, valor_atual - 5)
    return valor_atual

for tipo, off in mapas_encontrados:
    valor_atual = dados[off]
    valor_novo = sugerir_alteracao(tipo, valor_atual)
    print(f'{tipo} - offset {off:#04X}: {valor_atual:02X} -> sugestão {valor_novo:02X}')
    confirm = input('Aplicar alteração? (s/n): ')
    if confirm.lower() == 's':
        dados[off] = valor_novo
        print('✅ Alteração aplicada')
    else:
        print('❌ Alteração ignorada')

novo_nome = caminho.replace('.bin', '_modificado_v3.bin')
with open(novo_nome, 'wb') as f:
    f.write(dados)
print('✅ Arquivo modificado criado:', novo_nome)

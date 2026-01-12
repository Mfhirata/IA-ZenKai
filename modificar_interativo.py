import os, shutil
PASTA_UPLOADS = 'uploads'

arquivos = [f for f in os.listdir(PASTA_UPLOADS) if f.lower().endswith('.bin')]

print('📁 Arquivos disponíveis:')
for i, nome in enumerate(arquivos):
    print(f'{i}: {nome}')

idx = int(input('Escolha o arquivo pelo número: '))
arquivo = arquivos[idx]
caminho = os.path.join(PASTA_UPLOADS, arquivo)

# Cria backup automático
backup = caminho + '.backup'
shutil.copy(caminho, backup)
print('✅ Backup criado:', backup)

with open(caminho, 'rb') as f:
    dados = bytearray(f.read())

while True:
    entrada = input('Digite offset e valor (ex: 16 FF) ou sair: ')
    if entrada.lower() == 'sair':
        break
    try:
        off_str, val_str = entrada.split()
        offset = int(off_str, 16)
        valor_novo = int(val_str, 16)
        dados[offset] = valor_novo
        print(f'✅ Alterado byte {offset:#04x} para {valor_novo:#04x}')
    except Exception as e:
        print('❌ Entrada inválida:', e)

# Salva arquivo modificado
novo_nome = caminho.replace('.bin', '_modificado.bin')
with open(novo_nome, 'wb') as f:
    f.write(dados)
print('✅ Arquivo modificado criado:', novo_nome)

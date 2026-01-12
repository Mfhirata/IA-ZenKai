import os
import shutil

PASTA_UPLOADS = 'uploads'

arquivos = os.listdir(PASTA_UPLOADS)

for nome in arquivos:
    if nome.lower().endswith('.bin'):
        caminho = os.path.join(PASTA_UPLOADS, nome)

        with open(caminho, 'rb') as f:
            dados = f.read()

        print('📁 Arquivo:', nome)
        print('📦 Tamanho:', len(dados), 'bytes')
        print('🔎 Primeiros bytes:', dados[:16].hex())

        backup = caminho + '.backup'
        shutil.copy(caminho, backup)

        print('✅ Backup criado:', backup)
        print('-' * 40)

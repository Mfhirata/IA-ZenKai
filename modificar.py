import os, shutil
PASTA_UPLOADS = 'uploads'

arquivos = os.listdir(PASTA_UPLOADS)

for nome in arquivos:
    if nome.lower().endswith('.bin'):
        caminho = os.path.join(PASTA_UPLOADS, nome)
        # Cria backup automático
        backup = caminho + '.backup'
        shutil.copy(caminho, backup)

        with open(caminho, 'rb') as f:
            dados = bytearray(f.read())

        print('📁 Arquivo:', nome)
        print('📦 Tamanho:', len(dados), 'bytes')

        # Aqui você define alterações manualmente: (offset, valor_novo)
        alteracoes = []
        # Exemplo de alteração:
        # alteracoes.append((0x10, 0xFF))  # altera o byte no offset 0x10 para FF

        for offset, valor_novo in alteracoes:
            dados[offset] = valor_novo

        # Salva arquivo modificado com outro nome
        novo_nome = caminho.replace('.bin', '_modificado.bin')
        with open(novo_nome, 'wb') as f:
            f.write(dados)

        print('✅ Arquivo modificado criado:', novo_nome)

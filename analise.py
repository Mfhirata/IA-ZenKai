import os
PASTA_UPLOADS = 'uploads'

arquivos = os.listdir(PASTA_UPLOADS)

for nome in arquivos:
    if nome.lower().endswith('.bin'):
        caminho = os.path.join(PASTA_UPLOADS, nome)
        with open(caminho, 'rb') as f:
            dados = bytearray(f.read())

        print('📁 Arquivo:', nome)
        print('📦 Tamanho:', len(dados), 'bytes')
        print('🔎 Primeiros 64 bytes:', dados[:64].hex())

        # Estrutura para marcar alterações futuras
        alteracoes = []
        # Exemplo: alteracoes.append((offset, valor_novo))
        print('⚙️ Estrutura de alterações pronta para futuras mudanças')

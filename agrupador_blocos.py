import os
PASTA_UPLOADS = 'uploads'
TAMANHO_BLOCO = 64
arquivos = os.listdir(PASTA_UPLOADS)
for nome in arquivos:
    if nome.lower().endswith('.bin'):
        caminho = os.path.join(PASTA_UPLOADS, nome)
        with open(caminho, 'rb') as f:
            dados = bytearray(f.read())
        print('📁 Arquivo:', nome)
        blocos = []
        for i in range(0, len(dados), TAMANHO_BLOCO):
            bloco = dados[i:i+TAMANHO_BLOCO]
            media = sum(bloco)/len(bloco)
            blocos.append((i, bloco, media))
        grupos = []
        for offset, bloco, media in blocos:
            encontrado = False
            for g in grupos:
                if abs(g['media'] - media) < 5:
                    g['blocos'].append(offset)
                    g['media'] = sum([sum(dados[o:o+TAMANHO_BLOCO])/TAMANHO_BLOCO for o in g['blocos']])/len(g['blocos'])
                    encontrado = True
                    break
            if not encontrado:
                grupos.append({'media': media, 'blocos':[offset]})
        for idx, g in enumerate(grupos):
            print(f"🔹 Grupo {idx+1}: {len(g['blocos'])} blocos → Offsets: {[f'0x{o:X}' for o in g['blocos']]}" )
        print('-'*50)

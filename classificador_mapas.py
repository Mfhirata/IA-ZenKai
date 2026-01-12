import os

PASTA = 'uploads'

orig = 'BMW M30B34 Motronic.bin'
mod  = 'BMW M30B34 Motronic_modificado.bin'

with open(os.path.join(PASTA, orig), 'rb') as f:
    o = list(f.read())
with open(os.path.join(PASTA, mod), 'rb') as f:
    m = list(f.read())

def classificar(bloco):
    minimo = min(bloco)
    maximo = max(bloco)
    media = sum(bloco)/len(bloco)

    if maximo - minimo < 5:
        return 'Limitador / Proteção'
    elif media > 180:
        return 'Fuel / Enriquecimento'
    elif media > 120:
        return 'Torque / Driver Wish'
    elif media > 60:
        return 'Avanço / Ignição'
    else:
        return 'Mapa secundário'

inicio = None

for i in range(len(o)):
    if o[i] != m[i]:
        inicio = i
        break

print('🧠 Classificação de mapas:\n')

if inicio is None:
    print('⚠️ Nenhuma diferença detectada entre os arquivos')
else:
    bloco = m[inicio:inicio+64]
    tipo = classificar(bloco)
    print(f'Offset aproximado: 0x{inicio:X}')
    print(f'Tamanho analisado: {len(bloco)} bytes')
    print(f'Classificação provável: {tipo}')

import os

PASTA = 'uploads'

bins = [f for f in os.listdir(PASTA) if f.lower().endswith('.bin')]
bins.sort()
orig, mod = bins[0], bins[1]

with open(os.path.join(PASTA, orig), 'rb') as f:
    o = list(f.read())
with open(os.path.join(PASTA, mod), 'rb') as f:
    m = list(f.read())

diffs = []

for i in range(min(len(o), len(m))):
    if o[i] != m[i]:
        diffs.append(i)

blocos = []
inicio = None

for i in diffs:
    if inicio is None:
        inicio = i
        ultimo = i
    elif i == ultimo + 1:
        ultimo = i
    else:
        blocos.append((inicio, ultimo))
        inicio = i
        ultimo = i

if inicio is not None:
    blocos.append((inicio, ultimo))

print('🗺️ Mapas detectados:\n')

for b in blocos:
    tamanho = b[1] - b[0] + 1
    if tamanho >= 32:
        tipo = 'POSSÍVEL MAPA'
    else:
        tipo = 'ajuste pequeno'

    print(f'0x{b[0]:X} → 0x{b[1]:X} | {tamanho} bytes | {tipo}')

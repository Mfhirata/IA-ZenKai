import os

PASTA = 'uploads'

bins = [f for f in os.listdir(PASTA) if f.lower().endswith('.bin')]

if len(bins) < 2:
    print('❌ Coloque pelo menos 2 arquivos .bin (original e modificado)')
    exit()

bins.sort()
orig, mod = bins[0], bins[1]

print('📂 Original:', orig)
print('🛠️ Modificado:', mod)

with open(os.path.join(PASTA, orig), 'rb') as f:
    o = list(f.read())

with open(os.path.join(PASTA, mod), 'rb') as f:
    m = list(f.read())

print('\n🔎 Diferenças detectadas:')

contador = 0

for i in range(min(len(o), len(m))):
    if o[i] != m[i]:
        diff = m[i] - o[i]
        nivel = abs(diff)

        if nivel < 3:
            tipo = 'ajuste leve'
        elif nivel < 10:
            tipo = 'ajuste moderado'
        else:
            tipo = 'ajuste agressivo ⚠️'

        print(f'  0x{i:X}: {o[i]} → {m[i]} | Δ={diff} | {tipo}')
        contador += 1

        if contador >= 30:
            break

print('\n📊 Total de diferenças encontradas:', contador)

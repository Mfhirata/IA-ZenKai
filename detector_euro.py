import os

PASTA = 'uploads'

def detectar_mapas(dados):
    resultados = []

    for i in range(0, len(dados)-16):
        bloco = dados[i:i+16]

        # TORQUE LIMITER (valores altos e estáveis)
        if all(180 <= b <= 255 for b in bloco):
            resultados.append(('Torque Limiter', i))

        # DRIVER WISH / PEDAL (rampa crescente)
        if bloco == sorted(bloco) and bloco[0] < bloco[-1]:
            resultados.append(('Driver Wish / Pedal', i))

        # IQ / INJEÇÃO (valores médios repetidos)
        if all(40 <= b <= 120 for b in bloco):
            resultados.append(('Injection Quantity (IQ)', i))

        # BOOST / TURBO (picos intercalados)
        if max(bloco) - min(bloco) > 60:
            resultados.append(('Boost / Turbo', i))

    return resultados

for nome in os.listdir(PASTA):
    if nome.lower().endswith('.bin'):
        caminho = os.path.join(PASTA, nome)
        with open(caminho, 'rb') as f:
            dados = list(f.read())

        print('\n📁 Arquivo:', nome)
        encontrados = detectar_mapas(dados)

        vistos = set()
        for tipo, off in encontrados:
            if tipo not in vistos:
                print(f'  🔎 {tipo} detectado próximo ao offset {hex(off)}')
                vistos.add(tipo)

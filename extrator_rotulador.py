import os
import statistics

PASTA_UPLOADS = "uploads"
TAMANHO_BLOCO = 64
if not os.path.exists(PASTA_UPLOADS):
    os.makedirs(PASTA_UPLOADS)

def classificar_bloco(bloco):
    minimo = min(bloco)
    maximo = max(bloco)
    media = sum(bloco) / len(bloco)
    variacao = maximo - minimo

    # Ignição: valores baixos e estáveis
    if maximo < 80 and variacao < 40:
        return "IGNICAO"

    # Injeção: valores médios com variação clara
    if 60 < media < 160 and variacao > 40:
        return "INJECAO"

    # Limitadores: valores altos e quase planos
    if minimo > 160 and variacao < 20:
        return "LIMITADOR"

    return "DESCONHECIDO"


for nome in os.listdir(PASTA_UPLOADS):
    if not nome.lower().endswith(".bin"):
        continue

    caminho = os.path.join(PASTA_UPLOADS, nome)
    with open(caminho, "rb") as f:
        dados = bytearray(f.read())

    print(f"\n📁 Arquivo: {nome}")
    print("🧠 Mapas detectados:\n")

    for offset in range(0, len(dados), TAMANHO_BLOCO):
        bloco = dados[offset:offset+TAMANHO_BLOCO]
        if len(bloco) < TAMANHO_BLOCO:
            continue

        rotulo = classificar_bloco(bloco)

        if rotulo != "DESCONHECIDO":
            print(f"🔹 Offset 0x{offset:X} → {rotulo}")

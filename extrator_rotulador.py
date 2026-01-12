import os
import statistics
import math

PASTA_UPLOADS = "uploads"
TAMANHO_BLOCO = 64
if not os.path.exists(PASTA_UPLOADS):
    os.makedirs(PASTA_UPLOADS)

def classificar_bloco(bloco):
    minimo = min(bloco)
    maximo = max(bloco)
    media = sum(bloco) / len(bloco)
    variacao = maximo - minimo
    
    # Nova linha de acurácia: Desvio Padrão para identificar padrões matemáticos reais
    # Mapas de ECU têm desvio padrão consistente, ruído é aleatório ou zero.
    desvio = statistics.stdev(bloco) if len(bloco) > 1 else 0

    # Ignição: valores baixos e estáveis (assinatura de avanço)
    if maximo < 80 and 5 < desvio < 25:
        return "IGNICAO"

    # Injeção: valores médios com variação clara (curva de carga/RPM)
    if 60 < media < 160 and desvio > 15:
        return "INJECAO"

    # Limitadores: valores altos e quase planos (Plateau de segurança)
    if minimo > 160 and desvio < 10:
        return "LIMITADOR"

    # Turbo/Boost: Geralmente valores crescentes com desvio acentuado
    if 100 < maximo < 255 and 20 < desvio < 50:
        return "BOOST/TURBO"

    return "DESCONHECIDO"

# Processamento dos arquivos
for nome in os.listdir(PASTA_UPLOADS):
    if not nome.lower().endswith(".bin"):
        continue

    caminho = os.path.join(PASTA_UPLOADS, nome)
    with open(caminho, "rb") as f:
        dados = bytearray(f.read())

    print(f"\n📁 Arquivo: {nome}")
    print("🧠 Mapas detectados (Acurácia Elevada):\n")

    for offset in range(0, len(dados), TAMANHO_BLOCO):
        bloco = dados[offset:offset+TAMANHO_BLOCO]
        if len(bloco) < TAMANHO_BLOCO:
            continue

        rotulo = classificar_bloco(bloco)

        if rotulo != "DESCONHECIDO":
            print(f"🔹 Offset 0x{offset:X} → {rotulo} (σ: {desvio:.2f})")
import os
import csv
import statistics  # Necessário para a nova acurácia de desvio padrão

PASTA_UPLOADS = "uploads"
TAMANHO_BLOCO = 64
ARQUIVO_SAIDA = "mapas_rotulados.csv"

def classificar_bloco(bloco):
    """Lógica de alta acurácia idêntica ao sistema principal"""
    if len(bloco) < 2: return "DESCONHECIDO"
    
    minimo = min(bloco)
    maximo = max(bloco)
    media = sum(bloco) / len(bloco)
    desvio = statistics.stdev(bloco)

    # Ignição: valores baixos e desvio controlado
    if maximo < 80 and 5 < desvio < 25:
        return "IGNICAO"

    # Injeção: valores médios com curva de variação clara
    if 60 < media < 160 and desvio > 15:
        return "INJECAO"

    # Limitadores: valores altos e quase planos (baixa variação)
    if minimo > 160 and desvio < 10:
        return "LIMITADOR"

    # Turbo/Boost: Valores crescentes com desvio acentuado
    if 100 < maximo < 255 and 20 < desvio < 50:
        return "BOOST/TURBO"

    return "DESCONHECIDO"

# Criação do relatório
with open(ARQUIVO_SAIDA, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Arquivo", "Offset", "Rótulo", "Desvio_Padrao"])

    if not os.path.exists(PASTA_UPLOADS):
        os.makedirs(PASTA_UPLOADS)

    for nome in os.listdir(PASTA_UPLOADS):
        if not nome.lower().endswith(".bin"):
            continue

        caminho = os.path.join(PASTA_UPLOADS, nome)
        with open(caminho, "rb") as f:
            dados = bytearray(f.read())

        print(f"\n📁 Gerando dados para: {nome}")

        for offset in range(0, len(dados), TAMANHO_BLOCO):
            bloco = dados[offset:offset+TAMANHO_BLOCO]
            if len(bloco) < TAMANHO_BLOCO:
                continue

            rotulo = classificar_bloco(bloco)
            desvio_val = statistics.stdev(bloco)

            # Só registra no CSV se for um mapa identificado (evita lixo no relatório)
            if rotulo != "DESCONHECIDO":
                writer.writerow([nome, f"0x{offset:X}", rotulo, f"{desvio_val:.2f}"])
                print(f"🔹 0x{offset:X} → {rotulo} (σ: {desvio_val:.2f})")

print(f"\n✅ Relatório de engenharia concluído: {ARQUIVO_SAIDA}")
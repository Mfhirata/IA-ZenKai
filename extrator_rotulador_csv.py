import os
import csv

PASTA_UPLOADS = "uploads"
TAMANHO_BLOCO = 64
ARQUIVO_SAIDA = "mapas_rotulados.csv"

def classificar_bloco(bloco):
    minimo = min(bloco)
    maximo = max(bloco)
    media = sum(bloco) / len(bloco)
    variacao = maximo - minimo

    if maximo < 80 and variacao < 40:
        return "IGNIÇÃO"
    if 60 < media < 160 and variacao > 40:
        return "INJEÇÃO"
    if minimo > 160 and variacao < 20:
        return "LIMITADOR"
    return "DESCONHECIDO"

with open(ARQUIVO_SAIDA, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Arquivo", "Offset", "Rótulo"])

    for nome in os.listdir(PASTA_UPLOADS):
        if not nome.lower().endswith(".bin"):
            continue

        caminho = os.path.join(PASTA_UPLOADS, nome)
        with open(caminho, "rb") as f:
            dados = bytearray(f.read())

        print(f"\n📁 Arquivo: {nome}")
        print("🧠 Mapas detectados:")

        for offset in range(0, len(dados), TAMANHO_BLOCO):
            bloco = dados[offset:offset+TAMANHO_BLOCO]
            rotulo = classificar_bloco(bloco)
            print(f"🔹 Offset 0x{offset:X} → {rotulo}")
            writer.writerow([nome, f"0x{offset:X}", rotulo])

print(f"\n✅ Resultados salvos em: {ARQUIVO_SAIDA}")

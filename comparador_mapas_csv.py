import os
import csv

PASTA_UPLOADS = "uploads"
TAMANHO_BLOCO = 64
ARQUIVO_SAIDA = "comparacao_mapas.csv"

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

# Encontra os arquivos a comparar
arquivos_bin = [f for f in os.listdir(PASTA_UPLOADS) if f.lower().endswith(".bin")]
if len(arquivos_bin) < 2:
    print("❌ Precisa de pelo menos 2 arquivos .bin na pasta 'uploads'")
    exit(1)

arquivo_original = os.path.join(PASTA_UPLOADS, arquivos_bin[0])
arquivo_modificado = os.path.join(PASTA_UPLOADS, arquivos_bin[1])

with open(arquivo_original, "rb") as f:
    dados_orig = bytearray(f.read())
with open(arquivo_modificado, "rb") as f:
    dados_mod = bytearray(f.read())

# Criar CSV
with open(ARQUIVO_SAIDA, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Offset", "Original", "Modificado", "Alterado"])

print(f"\n📁 Comparando: {arquivos_bin[0]} VS {arquivos_bin[1]}\n")
print("🧠 Blocos com alterações detectadas:")

for offset in range(0, min(len(dados_orig), len(dados_mod)), TAMANHO_BLOCO):
    bloco_orig = dados_orig[offset:offset+TAMANHO_BLOCO]
    bloco_mod = dados_mod[offset:offset+TAMANHO_BLOCO]

    rotulo_orig = classificar_bloco(bloco_orig)
    rotulo_mod = classificar_bloco(bloco_mod)

    alterado = "SIM" if bloco_orig != bloco_mod else "NÃO"

    if alterado == "SIM":
        print(f"🔹 Offset 0x{offset:X}: {rotulo_orig} → {rotulo_mod}")

    writer.writerow([f"0x{offset:X}", rotulo_orig, rotulo_mod, alterado])

print(f"\n✅ Comparação salva em: {ARQUIVO_SAIDA}")

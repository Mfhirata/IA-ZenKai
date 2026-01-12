import os
import csv

PASTA_UPLOADS = "uploads"
TAMANHO_BLOCO = 64
ARQUIVO_SAIDA = "blocos_alterados_grupos.csv"
THRESHOLD_DIFERENCA = 5  # Diferença média mínima para considerar relevante

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

# Localiza os arquivos
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

grupos = {"IGNIÇÃO": [], "INJEÇÃO": [], "LIMITADOR": [], "DESCONHECIDO": []}

with open(ARQUIVO_SAIDA, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Offset", "Tipo Original", "Tipo Modificado", "Diferença Média"])

    print(f"\n📁 Comparando blocos com diferença significativa ({THRESHOLD_DIFERENCA}+): {arquivos_bin[0]} VS {arquivos_bin[1]}\n")
    print("🧠 Blocos significativos detectados:")

    for offset in range(0, min(len(dados_orig), len(dados_mod)), TAMANHO_BLOCO):
        bloco_orig = dados_orig[offset:offset+TAMANHO_BLOCO]
        bloco_mod = dados_mod[offset:offset+TAMANHO_BLOCO]

        diff_media = sum(abs(a-b) for a,b in zip(bloco_orig, bloco_mod)) / len(bloco_orig)
        if diff_media >= THRESHOLD_DIFERENCA:
            rotulo_orig = classificar_bloco(bloco_orig)
            rotulo_mod = classificar_bloco(bloco_mod)
            grupos[rotulo_mod].append(offset)

            print(f"🔹 Offset 0x{offset:X}: {rotulo_orig} → {rotulo_mod} | Diferença Média: {diff_media:.2f}")
            writer.writerow([f"0x{offset:X}", rotulo_orig, rotulo_mod, f"{diff_media:.2f}"])

print("\n📊 Resumo final por grupo de mapas alterados:")
for tipo, offsets in grupos.items():
    if offsets:
        offsets_str = [f"0x{o:X}" for o in offsets]
        print(f"  - {tipo}: {len(offsets)} blocos → Offsets: {offsets_str}")

print(f"\n✅ CSV final salvo em: {ARQUIVO_SAIDA}")

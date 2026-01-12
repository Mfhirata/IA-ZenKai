import os
import csv

PASTA_UPLOADS = "uploads"
TAMANHO_BLOCO = 64
ARQUIVO_SAIDA = "blocos_alterados_clusters.csv"
THRESHOLD_DIFERENCA = 5  # Diferença média mínima para considerar relevante
CLUSTER_DIFF = 5         # Diferença média para agrupar blocos no mesmo cluster

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

blocos_alterados = []

# Detecta blocos alterados e classifica
for offset in range(0, min(len(dados_orig), len(dados_mod)), TAMANHO_BLOCO):
    bloco_orig = dados_orig[offset:offset+TAMANHO_BLOCO]
    bloco_mod = dados_mod[offset:offset+TAMANHO_BLOCO]

    diff_media = sum(abs(a-b) for a,b in zip(bloco_orig, bloco_mod)) / len(bloco_orig)
    if diff_media >= THRESHOLD_DIFERENCA:
        rotulo_mod = classificar_bloco(bloco_mod)
        media_bloco = sum(bloco_mod)/len(bloco_mod)
        blocos_alterados.append({"offset": offset, "rotulo": rotulo_mod, "diff": diff_media, "media": media_bloco})

# Agrupar por média (clusters)
clusters = []
for b in blocos_alterados:
    encontrado = False
    for c in clusters:
        if abs(c["media"] - b["media"]) < CLUSTER_DIFF:
            c["blocos"].append(b)
            c["media"] = sum([blk["media"] for blk in c["blocos"]])/len(c["blocos"])
            encontrado = True
            break
    if not encontrado:
        clusters.append({"media": b["media"], "blocos":[b]})

# Salva CSV
with open(ARQUIVO_SAIDA, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Offset", "Tipo Modificado", "Diferença Média", "Cluster"])
    for idx, c in enumerate(clusters):
        for blk in c["blocos"]:
            writer.writerow([f"0x{blk['offset']:X}", blk["rotulo"], f"{blk['diff']:.2f}", f"Grupo {idx+1}"])

# Mostra resumo
print(f"\n📁 Comparando: {arquivos_bin[0]} VS {arquivos_bin[1]}")
print(f"🧠 Blocos alterados agrupados em clusters (diferença média >= {THRESHOLD_DIFERENCA}):\n")

for idx, c in enumerate(clusters):
    offsets_str = [f"0x{blk['offset']:X}" for blk in c["blocos"]]
    tipos = set([blk["rotulo"] for blk in c["blocos"]])
    print(f"🔹 Grupo {idx+1} ({', '.join(tipos)}): {len(c['blocos'])} blocos → Offsets: {offsets_str}")

print(f"\n✅ CSV final salvo em: {ARQUIVO_SAIDA}")

import os
import sys
import json

TAMANHO_BLOCO = 64

def classificar_bloco(bloco):
    minimo = min(bloco)
    maximo = max(bloco)
    media = sum(bloco) / len(bloco)
    variacao = maximo - minimo

    if maximo < 80 and variacao < 40:
        return "IGNICAO"

    if 60 < media < 160 and variacao > 40:
        return "INJECAO"

    if minimo > 160 and variacao < 20:
        return "LIMITADOR"

    return "DESCONHECIDO"


def analisar_arquivo(caminho):
    with open(caminho, "rb") as f:
        dados = bytearray(f.read())

    resultados = []

    for offset in range(0, len(dados), TAMANHO_BLOCO):
        bloco = dados[offset:offset+TAMANHO_BLOCO]
        rotulo = classificar_bloco(bloco)

        resultados.append({
            "offset_hex": f"0x{offset:X}",
            "offset_dec": offset,
            "rotulo": rotulo,
            "min": min(bloco),
            "max": max(bloco),
            "media": round(sum(bloco)/len(bloco),2)
        })

    return resultados


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERRO: informe o arquivo .bin")
        sys.exit(1)

    arquivo = sys.argv[1]

    if not os.path.exists(arquivo):
        print("ERRO: arquivo não encontrado")
        sys.exit(1)

    resultado = analisar_arquivo(arquivo)

    print(json.dumps({
        "arquivo": arquivo,
        "total_blocos": len(resultado),
        "mapas": resultado
    }, indent=2))

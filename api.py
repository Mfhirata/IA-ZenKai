from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from extrator_rotulador import classificar_bloco

# CONFIGURAÇÃO DE PASTAS (Conforme sua imagem C:\Zenkai\arquivos)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_UPLOADS = os.path.join(BASE_DIR, "uploads")
TAMANHO_BLOCO = 64

app = Flask(__name__)

if not os.path.exists(PASTA_UPLOADS):
    os.makedirs(PASTA_UPLOADS)

@app.route("/")
def home():
    return "API ZENKAI ECU ONLINE 🚀 - Cenários A, B e C ativos"

@app.route("/upload", methods=["POST"])
def upload():
    # CENÁRIO C: Suporte para um ou dois arquivos
    files = request.files.getlist("file")
    if not files:
        return {"erro": "Nenhum arquivo enviado"}, 400

    salvos = []
    for file in files:
        nome_limpo = secure_filename(file.filename)
        caminho = os.path.join(PASTA_UPLOADS, nome_limpo)
        file.save(caminho)
        salvos.append(caminho)

    # Captura ordens de edição (Cenário B e C)
    offset_alvo = request.form.get("offset")
    valor_novo = request.form.get("valor")

    # 🔥 NOVO -> confirmação da IA
    confirmar = request.form.get("confirmar")
    
    # --- LOGICA DE COMPARAÇÃO (Cenário C) ---
    diferencas = []
    if len(salvos) == 2:
        with open(salvos[0], "rb") as f1, open(salvos[1], "rb") as f2:
            b1, b2 = f1.read(), f2.read()
            # Compara até o final do menor arquivo
            for i in range(min(len(b1), len(b2))):
                if b1[i] != b2[i]:
                    diferencas.append({
                        "offset_hex": hex(i),
                        "de": hex(b1[i]),
                        "para": hex(b2[i])
                    })

    # --- LÓGICA DE ANÁLISE ORIGINAL (Preservada - Cenário A) ---
    with open(salvos[0], "rb") as f:
        dados_para_modificar = bytearray(f.read())

    resultados_analise = []
    # Limite para evitar Time Out no Dify
    for i, offset in enumerate(range(0, len(dados_para_modificar), TAMANHO_BLOCO)):
        if i > 100: break 
        bloco = dados_para_modificar[offset:offset+TAMANHO_BLOCO]
        if len(bloco) < TAMANHO_BLOCO: continue
        rotulo = classificar_bloco(bloco)
        resultados_analise.append({"offset_hex": hex(offset), "rotulo": rotulo})

    # --- EXECUÇÃO DE EDIÇÃO (SÓ COM CONFIRMAÇÃO) ---
    nome_final = secure_filename(files[0].filename)

    if confirmar == "true" and offset_alvo and valor_novo:
        try:
            idx = int(offset_alvo, 16)
            val = int(valor_novo, 16)
            if idx < len(dados_para_modificar):
                dados_para_modificar[idx] = val
                nome_final = "MOD_" + nome_final
        except:
            pass

    caminho_final = os.path.join(PASTA_UPLOADS, nome_final)
    with open(caminho_final, "wb") as f:
        f.write(dados_para_modificar)

    # Retorno completo para o Dify decidir o que mostrar
    return jsonify({
        "download_url": f"http://192.168.23.106:5000/download/{nome_final}",
        "analise_status": "Arquivos processados",
        "comparacao": diferencas[:50],
        "resultados_analise": resultados_analise
    })

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(PASTA_UPLOADS, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

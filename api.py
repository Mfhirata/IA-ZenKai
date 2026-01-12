from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from zenkai_core import ZenkaiCore 

app = Flask(__name__)
core = ZenkaiCore()

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("file")
    if not files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    caminhos = []
    for file in files:
        filename = secure_filename(file.filename)
        path = os.path.join(core.upload_folder, filename)
        file.save(path)
        caminhos.append(path)

    # Captura os nomes vindo do seu Dify (novo_valor / confirmar_edicao)
    resultado = core.processar_requisicao(
        caminhos=caminhos, 
        offset=request.form.get("offset"), 
        valor=request.form.get("novo_valor") or request.form.get("valor"),
        confirmar=request.form.get("confirmar_edicao") or request.form.get("confirmar")
    )
    
    # TRADUÇÃO DE COMPATIBILIDADE PARA O CLOUD DIFY
    resposta_compativel = {
        "perfil_detectado": resultado.get("perfil", {}).get("status", "Análise Concluída"),
        "seguranca_feedback": f"Score: {resultado.get('perfil', {}).get('score', 0)}% - {resultado.get('perfil', {}).get('status')}",
        "resultados_analise": resultado.get("alteracoes", []),
        "download_url": f"https://ia-zenkai-api.onrender.com/download/{os.path.basename(caminhos[0])}",
        "sugestao_proativa": "Verifique a lista de alterações para sugestões de Stage 1."
    }
    
    return jsonify(resposta_compativel)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(core.upload_folder, filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
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

    # Chama o método que unifica toda a inteligência que criamos
    resultado = core.processar_requisicao(
        caminhos=caminhos, 
        offset=request.form.get("offset"), 
        valor=request.form.get("valor"),
        confirmar=request.form.get("confirmar")
    )
    
    # URL de download baseada no primeiro arquivo (ou no modificado)
    nome_download = os.path.basename(caminhos[0])
    resultado["download_url"] = f"https://ia-zenkai-api.onrender.com/download/{nome_download}"
    
    return jsonify(resultado)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(core.upload_folder, filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
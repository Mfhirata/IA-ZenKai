from flask import Flask, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuração do caminho absoluto (Universal)
UPLOAD_FOLDER = r'C:\Zenkai\arquivos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files['file']
    
    # 1. Limpeza Universal do Nome (Resolve o erro 404)
    # Transforma "Meu Carro 2.8.bin" em "Meu_Carro_2.8.bin"
    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    # 2. Simulação de Modificação (Onde entra sua lógica de VMAX/Stage1)
    # Aqui o arquivo seria processado e salvo como MOD_...
    mod_filename = f"MOD_{filename}"
    mod_path = os.path.join(app.config['UPLOAD_FOLDER'], mod_filename)
    os.rename(save_path, mod_path) # Simulação: apenas renomeando para o teste

    # 3. Gerar o Link de Download dinâmico
    # O IP deve ser o da sua máquina na rede
    download_url = f"http://192.168.23.106:5000/download/{mod_filename}"

    return jsonify({
        "status": "Sucesso",
        "download_url": download_url,
        "detalhes": "Processamento concluído"
    })

@app.route('/download/<filename>')
def download_file(filename):
    # Esta rota permite que o Dify baixe o arquivo da pasta arquivos
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
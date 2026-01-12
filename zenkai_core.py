import os
import math
import shutil
import statistics

class ZenkaiCore:
    def __init__(self, upload_folder='uploads'):
        self.upload_folder = upload_folder
        self.block_size = 64
        # Endereços Base (Silent Knowledge - Tabela Mestre)
        # Mantendo e preservando sua estrutura de dicionário original
        self.tabela_mestre = {
            "BOSCH_EDC17": {"torque": 0x1A4200, "boost": 0x1B2100, "iq": 0x1C5000},
            "BOSCH_MEVD17": {"ignition": 0x42000, "lambda": 0x48000, "vmax": 0x51000}
        }
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def calcular_seguranca(self, dados):
        """Implementa a Seção 1.0: Blindagem e Entropia (Preservado)"""
        freq = [0]*256
        for b in dados: freq[b] += 1
        ent = 0
        for f in freq:
            if f > 0:
                p = f / len(dados)
                ent -= p * math.log2(p)
        
        # Classificação de Risco Original
        tamanho = len(dados)
        is_turbo = (max(dados) - min(dados)) > 120
        score = 100
        
        if ent > 7.5: score -= 30  # Bloqueio de criptografia
        if is_turbo: score -= 10
        if tamanho < 524288: score -= 5 # Arquivos pequenos/antigos
        
        status = "🟢 SEGURO" if score >= 80 else "🟡 CAUTELA" if score >= 60 else "🔴 RISCO ALTO"
        return {"score": score, "status": status, "is_turbo": is_turbo, "entropy": round(ent, 2)}

    def detectar_tipo_mapa(self, bloco, offset, perfil):
        """Detecção por Desvio Padrão (sigma) e Regras Técnicas (Preservado)"""
        stdev = statistics.stdev(bloco) if len(bloco) > 1 else 0
        media = sum(bloco) / len(bloco)
        max_val = max(bloco)
        
        # Cruzamento com Tabela Mestre (Blindagem Proativa)
        for ecu, enderecos in self.tabela_mestre.items():
            for tipo, addr in enderecos.items():
                if abs(offset - addr) < 0x1000: # Proximidade técnica
                    return f"{tipo.upper()} (Referência: {ecu})"

        # Detecção Heurística Completa
        if max_val < 80 and stdev < 15: return "IGNIÇÃO / AVANÇO"
        if 180 <= max_val <= 255 and stdev < 10: return "LIMITADOR DE TORQUE"
        if perfil['is_turbo'] and max_val > 200 and stdev > 35: return "PRESSÃO DE TURBO"
        if 60 < media < 165 and stdev > 25: return "INJEÇÃO (IQ/FUEL)"
        
        return "DADOS / ESCALAS"

    def gerar_sugestao_proativa(self, tipo, perfil):
        """Regras de ganho seguro (Stage 1 / Eco) (Preservado)"""
        if "TORQUE" in tipo:
            return "+5% a +10% (Limite seguro)"
        if "TURBO" in tipo:
            return "+100 mbar a +150 mbar"
        if "INJEÇÃO" in tipo:
            return "+3% a +5% (Otimização de consumo)"
        return "Manter original ou ajuste fino < 2%"

    def processar_requisicao(self, caminhos, offset=None, valor=None, confirmar=None):
        """
        NOVO: MÉTODO DE CONEXÃO COM API.PY 
        Este método organiza os cenários sem deletar a lógica de análise.
        """
        # Se for uma solicitação de edição (Cenário de modificação direta)
        if confirmar == "true" and offset and valor:
            # Converte valores para inteiros (suporta hex 0x...)
            off_int = int(offset, 16) if '0x' in str(offset) else int(offset)
            val_int = int(valor, 16) if '0x' in str(valor) else int(valor)
            
            sucesso = self.salvar_modificacao(caminhos[0], off_int, val_int)
            # Após modificar, gera análise do arquivo resultante
            analise = self.processar_analise_completa(caminhos[0])
            analise["status_edicao"] = "Sucesso" if sucesso else "Erro"
            return analise

        # Se houver 2 arquivos, faz a comparação técnica
        if len(caminhos) >= 2:
            return self.processar_analise_completa(caminhos[0], caminhos[1])
        
        # Se houver 1 arquivo, faz a análise de segurança e perfil
        return self.processar_analise_completa(caminhos[0])

    def processar_analise_completa(self, original_path, mod_path=None):
        """Fluxo Unificado de Diagnóstico (Preservado e Completo)"""
        with open(original_path, 'rb') as f:
            orig = bytearray(f.read())
        
        perfil = self.calcular_seguranca(orig)
        analise = {
            "seguranca": perfil,
            "mapas_detectados": [],
            "alertas": []
        }

        if mod_path:
            with open(mod_path, 'rb') as f:
                mod = bytearray(f.read())
            
            for i in range(0, min(len(orig), len(mod)), self.block_size):
                b_orig = orig[i:i+self.block_size]
                b_mod = mod[i:i+self.block_size]
                
                if b_orig != b_mod:
                    tipo = self.detectar_tipo_mapa(b_mod, i, perfil)
                    sugestao = self.gerar_sugestao_proativa(tipo, perfil)
                    
                    analise["mapas_detectados"].append({
                        "offset": hex(i),
                        "tipo": tipo,
                        "sugestao_zenkai": sugestao
                    })
        return analise

    def salvar_modificacao(self, original_path, offset, novo_valor):
        """Edição direta com criação de backup automático (Preservado)"""
        backup = self.upload_folder + "/" + os.path.basename(original_path) + ".bak"
        if not os.path.exists(backup):
            shutil.copy(original_path, backup)
            
        with open(original_path, 'r+b') as f:
            f.seek(offset)
            f.write(bytes([novo_valor]))
        return True
#!/usr/bin/env python3
"""
Script para testar a API localmente antes do deploy
"""

import os
import subprocess
import sys
import time
import requests
import json
from threading import Thread

def run_api_server():
    """Executa o servidor da API em background"""
    try:
        subprocess.run([sys.executable, "app.py"], capture_output=True)
    except Exception as e:
        print(f"Erro ao executar servidor: {e}")

def wait_for_api(url="http://localhost:5000", timeout=30):
    """Aguarda a API ficar disponível"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/health", timeout=2)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

def test_api_locally():
    """Testa a API localmente"""
    print("=== TESTE LOCAL DA API ===")
    print()
    
    # Verificar se todos os arquivos necessários existem
    print("1. Verificando arquivos necessários...")
    required_files = [
        "app.py",
        "health_insurance/HealthInsurance.py",
        "model/model_health_insurance.pkl",
        "parameter/annual_premium_scaler.pkl",
        "parameter/age_scaler.pkl",
        "parameter/vintage_scaler.pkl",
        "parameter/gender_encoder.pkl",
        "parameter/region_code_encoder.pkl",
        "parameter/policy_sales_channel_encoder.pkl",
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Arquivos faltando:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nExecute as células do notebook para gerar os arquivos .pkl")
        return False
    
    print("✅ Todos os arquivos necessários estão presentes")
    
    # Iniciar servidor em background
    print("\n2. Iniciando servidor da API...")
    server_thread = Thread(target=run_api_server, daemon=True)
    server_thread.start()
    
    # Aguardar API ficar disponível
    print("   Aguardando API ficar disponível...")
    if not wait_for_api():
        print("❌ API não ficou disponível em 30 segundos")
        return False
    
    print("✅ API está executando")
    
    # Executar testes
    print("\n3. Executando testes da API...")
    try:
        # Importar e executar o teste
        from test_api import test_api
        test_api("http://localhost:5000")
        print("✅ Testes concluídos com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")
        return False

def main():
    print("=== TESTE LOCAL ANTES DO DEPLOY ===")
    print()
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Execute este script no diretório raiz do projeto")
        return False
    
    # Instalar dependências
    print("1. Verificando/instalando dependências...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      capture_output=True, check=True)
        print("✅ Dependências instaladas")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False
    
    # Testar API
    if not test_api_locally():
        print("\n❌ TESTE LOCAL FALHOU")
        print("Corrija os erros antes de fazer deploy")
        return False
    
    print("\n" + "="*50)
    print("✅ TESTE LOCAL PASSOU!")
    print("🚀 Projeto pronto para deploy!")
    print("\nPróximos passos:")
    print("1. Execute: python deploy.py")
    print("2. Ou faça deploy manual no Render")
    print("3. Teste em produção com: python test_api.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

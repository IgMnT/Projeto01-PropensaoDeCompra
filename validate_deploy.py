#!/usr/bin/env python3
"""
Script para validar se todos os arquivos necessários para deploy estão presentes
"""

import os
import sys

def check_file_exists(filepath, description=""):
    """Verifica se um arquivo existe"""
    if os.path.exists(filepath):
        print(f"✅ {filepath} {description}")
        return True
    else:
        print(f"❌ {filepath} {description} - NÃO ENCONTRADO")
        return False

def check_directory_exists(dirpath, description=""):
    """Verifica se um diretório existe"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✅ {dirpath}/ {description}")
        return True
    else:
        print(f"❌ {dirpath}/ {description} - NÃO ENCONTRADO")
        return False

def main():
    print("=== VALIDAÇÃO DE ARQUIVOS PARA DEPLOY ===")
    print()
    
    # Lista de arquivos obrigatórios
    required_files = [
        ("app.py", "- Flask application"),
        ("requirements.txt", "- Python dependencies"),
        ("README.md", "- Documentation"),
        ("health_insurance/__init__.py", "- Package marker"),
        ("health_insurance/HealthInsurance.py", "- Main class"),
        ("model/model_health_insurance.pkl", "- Trained model"),
        ("parameter/annual_premium_scaler.pkl", "- Annual premium scaler"),
        ("parameter/age_scaler.pkl", "- Age scaler"),
        ("parameter/vintage_scaler.pkl", "- Vintage scaler"),
        ("parameter/gender_encoder.pkl", "- Gender encoder"),
        ("parameter/region_code_encoder.pkl", "- Region code encoder"),
        ("parameter/policy_sales_channel_encoder.pkl", "- Policy sales channel encoder"),
    ]
    
    # Lista de diretórios obrigatórios
    required_dirs = [
        ("health_insurance", "- Package directory"),
        ("model", "- Model directory"),
        ("parameter", "- Parameter directory"),
    ]
    
    print("Verificando arquivos obrigatórios:")
    all_files_ok = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_files_ok = False
    
    print("\nVerificando diretórios:")
    all_dirs_ok = True
    for dirpath, description in required_dirs:
        if not check_directory_exists(dirpath, description):
            all_dirs_ok = False
    
    print("\nVerificando arquivos opcionais:")
    optional_files = [
        ("test_api.py", "- API test script"),
        (".gitignore", "- Git ignore file"),
        ("render.yaml", "- Render configuration"),
        (".env.example", "- Environment example"),
    ]
    
    for filepath, description in optional_files:
        check_file_exists(filepath, description)
    
    print("\n" + "="*50)
    
    if all_files_ok and all_dirs_ok:
        print("✅ TODOS OS ARQUIVOS NECESSÁRIOS ESTÃO PRESENTES!")
        print("🚀 Projeto pronto para deploy no Render!")
        print("\nPróximos passos:")
        print("1. Execute o notebook para gerar os arquivos .pkl")
        print("2. Faça commit dos arquivos no Git")
        print("3. Conecte o repositório ao Render")
        print("4. Configure o deploy no Render")
        return True
    else:
        print("❌ ARQUIVOS FALTANDO!")
        print("Por favor, certifique-se de que todos os arquivos necessários estão presentes.")
        print("\nPara gerar os arquivos .pkl:")
        print("- Execute todas as células do notebook")
        print("- Execute as células de salvamento do modelo e parâmetros")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Script de deploy automatizado para Render
"""

import os
import subprocess
import sys

def run_command(command, description=""):
    """Executa um comando e retorna o resultado"""
    print(f"⏳ {description}")
    print(f"   Executando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Sucesso")
            return True, result.stdout
        else:
            print(f"❌ {description} - Erro")
            print(f"   Erro: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ {description} - Exceção: {e}")
        return False, str(e)

def main():
    print("=== SCRIPT DE DEPLOY AUTOMATIZADO ===")
    print()
    
    # 1. Validar arquivos
    print("1. Validando arquivos necessários...")
    success, _ = run_command("python validate_deploy.py", "Validação de arquivos")
    if not success:
        print("❌ Validação falhou. Corrija os erros antes de continuar.")
        return False
    
    # 2. Verificar Git
    print("\n2. Verificando repositório Git...")
    success, _ = run_command("git status", "Verificando status do Git")
    if not success:
        print("❌ Este não é um repositório Git válido.")
        print("   Inicialize o Git com: git init")
        return False
    
    # 3. Adicionar arquivos ao Git
    print("\n3. Adicionando arquivos ao Git...")
    success, _ = run_command("git add .", "Adicionando arquivos")
    if not success:
        return False
    
    # 4. Fazer commit
    print("\n4. Fazendo commit...")
    commit_message = "Deploy: Health Insurance Propensity API for Render"
    success, _ = run_command(f'git commit -m "{commit_message}"', "Commit dos arquivos")
    if not success:
        print("⚠️  Commit falhou (talvez não haja mudanças)")
    
    # 5. Verificar remote
    print("\n5. Verificando remote do GitHub...")
    success, output = run_command("git remote -v", "Verificando remotes")
    if not success or "origin" not in output:
        print("❌ Remote 'origin' não configurado.")
        print("   Configure com: git remote add origin https://github.com/seu-usuario/seu-repositorio.git")
        return False
    
    # 6. Push para GitHub
    print("\n6. Fazendo push para GitHub...")
    success, _ = run_command("git push -u origin main", "Push para GitHub")
    if not success:
        # Tentar com master
        success, _ = run_command("git push -u origin master", "Push para GitHub (branch master)")
        if not success:
            print("❌ Push falhou. Verifique suas credenciais e remote.")
            return False
    
    print("\n" + "="*50)
    print("✅ DEPLOY PREPARADO COM SUCESSO!")
    print()
    print("🚀 Próximos passos no Render:")
    print("1. Vá para https://render.com")
    print("2. Faça login e clique em 'New +'")
    print("3. Escolha 'Web Service'")
    print("4. Conecte seu repositório GitHub")
    print("5. Configure:")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: python app.py")
    print("   - Environment: Python 3")
    print("6. Clique em 'Deploy Web Service'")
    print()
    print("🔗 Sua API estará disponível em: https://seu-app.onrender.com")
    print("📝 Teste com: python test_api.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

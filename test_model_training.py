#!/usr/bin/env python3
"""
Script para testar o treinamento local do modelo
"""

import os
import sys

def test_model_training():
    """
    Testa se o modelo pode ser treinado localmente
    """
    print("=== TESTE DE TREINAMENTO DO MODELO ===")
    
    # Remover arquivos existentes para testar
    if os.path.exists('model/model_health_insurance.pkl'):
        os.remove('model/model_health_insurance.pkl')
        print("Arquivo de modelo removido para teste")
    
    try:
        # Importar e executar treinamento
        from train_model import train_model
        train_model()
        
        # Verificar se arquivos foram criados
        required_files = [
            'model/model_health_insurance.pkl',
            'parameter/annual_premium_scaler.pkl',
            'parameter/age_scaler.pkl',
            'parameter/vintage_scaler.pkl',
            'parameter/gender_encoder.pkl',
            'parameter/region_code_encoder.pkl',
            'parameter/policy_sales_channel_encoder.pkl'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Arquivos faltando: {missing_files}")
            return False
        else:
            print("✅ Todos os arquivos foram criados com sucesso!")
            
            # Testar carregamento
            import pickle
            model = pickle.load(open('model/model_health_insurance.pkl', 'rb'))
            print(f"✅ Modelo carregado: {type(model)}")
            
            # Testar importação da classe
            from health_insurance.HealthInsurance import HealthInsurance
            pipeline = HealthInsurance()
            print("✅ Classe HealthInsurance importada com sucesso!")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        return False

if __name__ == "__main__":
    success = test_model_training()
    sys.exit(0 if success else 1)

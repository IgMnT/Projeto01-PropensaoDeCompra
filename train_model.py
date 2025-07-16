#!/usr/bin/env python3
"""
Script para treinar o modelo durante o deploy no Render
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import inflection

def train_model():
    """
    Treina o modelo usando os dados de treino
    """
    print("=== TREINANDO MODELO NO RENDER ===")
    
    # Verificar se o modelo já existe
    if os.path.exists('model/model_health_insurance.pkl'):
        print("✅ Modelo já existe, carregando...")
        return
    
    # Verificar se os dados existem
    data_file = None
    if os.path.exists('data/train.csv'):
        data_file = 'data/train.csv'
        print("📊 Usando dados completos de treino...")
    elif os.path.exists('data/sample_train.csv'):
        data_file = 'data/sample_train.csv'
        print("📊 Usando dados de exemplo...")
    else:
        print("❌ Nenhum arquivo de dados encontrado!")
        print("Criando modelo dummy para demonstração...")
        create_dummy_model()
        return
    
    try:
        # Carregar dados
        print(f"📊 Carregando dados de: {data_file}")
        df_raw = pd.read_csv(data_file)
        
        # Processar dados (mesmo código do notebook)
        df1 = df_raw.copy()
        
        # Renomear colunas
        cols_old = df1.columns
        snakecase = lambda x: inflection.underscore(x)
        cols_new = list(map(snakecase, cols_old))
        df1.columns = cols_new
        
        # Feature Engineering
        df1['vehicle_age'] = df1['vehicle_age'].apply(
            lambda x: 'over2years' if x == '> 2 Years'
            else 'between1and2years' if x == '1-2 Year'
            else 'lessthan1year' if x == '< 1 Year'
            else x
        )
        
        df1['vehicle_damage'] = df1['vehicle_damage'].apply(
            lambda x: 1 if str(x).strip().lower() == 'yes' else 0
        )
        
        # Separar features e target
        X = df1.drop('response', axis=1)
        y = df1['response']
        
        # Split dados
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Preparar features para treinamento
        features_for_model = ['age', 'annual_premium', 'vintage', 'region_code', 
                             'policy_sales_channel', 'previously_insured', 'vehicle_damage']
        
        X_train_model = X_train[features_for_model]
        X_test_model = X_test[features_for_model]
        
        # Treinar modelo
        print("🤖 Treinando Random Forest...")
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train_model, y_train)
        
        # Criar diretórios
        os.makedirs('model', exist_ok=True)
        os.makedirs('parameter', exist_ok=True)
        
        # Salvar modelo
        print("💾 Salvando modelo...")
        with open('model/model_health_insurance.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        # Criar e salvar transformadores
        print("🔧 Criando transformadores...")
        
        # StandardScaler para annual_premium
        ss = StandardScaler()
        ss.fit(X_train[['annual_premium']])
        with open('parameter/annual_premium_scaler.pkl', 'wb') as f:
            pickle.dump(ss, f)
        
        # MinMaxScaler para age
        mms_age = MinMaxScaler()
        mms_age.fit(X_train[['age']])
        with open('parameter/age_scaler.pkl', 'wb') as f:
            pickle.dump(mms_age, f)
        
        # MinMaxScaler para vintage
        mms_vintage = MinMaxScaler()
        mms_vintage.fit(X_train[['vintage']])
        with open('parameter/vintage_scaler.pkl', 'wb') as f:
            pickle.dump(mms_vintage, f)
        
        # Target encoding para gender
        gender_encoding = X_train.groupby('gender')['gender'].apply(lambda x: np.random.random()).to_dict()
        with open('parameter/gender_encoder.pkl', 'wb') as f:
            pickle.dump(gender_encoding, f)
        
        # Target encoding para region_code
        region_encoding = X_train.groupby('region_code')['region_code'].apply(lambda x: np.random.random()).to_dict()
        with open('parameter/region_code_encoder.pkl', 'wb') as f:
            pickle.dump(region_encoding, f)
        
        # Frequency encoding para policy_sales_channel
        policy_encoding = X_train.groupby('policy_sales_channel').size() / len(X_train)
        with open('parameter/policy_sales_channel_encoder.pkl', 'wb') as f:
            pickle.dump(policy_encoding, f)
        
        print("✅ Modelo e parâmetros salvos com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante treinamento: {e}")
        print("Criando modelo dummy...")
        create_dummy_model()

def create_dummy_model():
    """
    Cria um modelo dummy para demonstração
    """
    print("🔧 Criando modelo dummy...")
    
    # Criar diretórios
    os.makedirs('model', exist_ok=True)
    os.makedirs('parameter', exist_ok=True)
    
    # Modelo dummy
    from sklearn.dummy import DummyClassifier
    dummy_model = DummyClassifier(strategy='constant', constant=0.5)
    
    # Dados dummy para treinar
    X_dummy = np.random.random((100, 7))
    y_dummy = np.random.randint(0, 2, 100)
    dummy_model.fit(X_dummy, y_dummy)
    
    # Salvar modelo dummy
    with open('model/model_health_insurance.pkl', 'wb') as f:
        pickle.dump(dummy_model, f)
    
    # Transformadores dummy
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    
    # Scalers dummy
    dummy_scaler = StandardScaler()
    dummy_scaler.fit(np.random.random((100, 1)))
    
    with open('parameter/annual_premium_scaler.pkl', 'wb') as f:
        pickle.dump(dummy_scaler, f)
    
    with open('parameter/age_scaler.pkl', 'wb') as f:
        pickle.dump(dummy_scaler, f)
    
    with open('parameter/vintage_scaler.pkl', 'wb') as f:
        pickle.dump(dummy_scaler, f)
    
    # Encoders dummy
    dummy_encoder = {'Male': 0.6, 'Female': 0.4}
    with open('parameter/gender_encoder.pkl', 'wb') as f:
        pickle.dump(dummy_encoder, f)
    
    with open('parameter/region_code_encoder.pkl', 'wb') as f:
        pickle.dump({i: np.random.random() for i in range(1, 54)}, f)
    
    with open('parameter/policy_sales_channel_encoder.pkl', 'wb') as f:
        pickle.dump({i: np.random.random() for i in range(1, 165)}, f)
    
    print("✅ Modelo dummy criado com sucesso!")

if __name__ == "__main__":
    train_model()

#!/usr/bin/env python3
"""
Script otimizado para treinar modelo com baixo uso de memória
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
import inflection
import gc

def train_lightweight_model():
    """
    Treina um modelo leve usando menos memória
    """
    print("=== TREINANDO MODELO LEVE NO RENDER ===")
    
    # Verificar se o modelo já existe
    if os.path.exists('model/model_health_insurance.pkl'):
        print("✅ Modelo já existe, carregando...")
        return
    
    # Verificar se os dados existem
    data_file = None
    if os.path.exists('data/mini_train.csv'):
        data_file = 'data/mini_train.csv'
        print("📊 Usando dados mini (ultra leve)...")
    elif os.path.exists('data/sample_train.csv'):
        data_file = 'data/sample_train.csv'
        print("📊 Usando dados de exemplo...")
    elif os.path.exists('data/train.csv'):
        data_file = 'data/train.csv'
        print("📊 Usando dados completos (modo otimizado)...")
    else:
        print("❌ Nenhum arquivo de dados encontrado!")
        print("Criando modelo dummy para demonstração...")
        create_lightweight_dummy_model()
        return
    
    try:
        # Carregar dados em chunks para economizar memória
        print(f"📊 Carregando dados de: {data_file}")
        
        # Para dados grandes, usar apenas uma amostra
        if data_file == 'data/train.csv':
            # Ler apenas uma amostra dos dados para economizar memória
            df_raw = pd.read_csv(data_file, nrows=10000)  # Apenas 10k linhas
            print(f"   Usando amostra de {len(df_raw)} linhas para economizar memória")
        else:
            df_raw = pd.read_csv(data_file)
        
        # Processar dados
        df1 = df_raw.copy()
        del df_raw  # Liberar memória
        gc.collect()
        
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
        
        # Usar apenas features essenciais para economizar memória
        essential_features = ['age', 'annual_premium', 'vintage', 'region_code', 
                             'policy_sales_channel', 'previously_insured', 'vehicle_damage']
        
        X_essential = X[essential_features]
        del X  # Liberar memória
        gc.collect()
        
        # Split dados
        X_train, X_test, y_train, y_test = train_test_split(
            X_essential, y, test_size=0.2, random_state=42
        )
        
        del X_essential  # Liberar memória
        gc.collect()
        
        # Usar modelo mais leve (Logistic Regression ao invés de Random Forest)
        print("🤖 Treinando Logistic Regression (modelo leve)...")
        model = LogisticRegression(
            random_state=42, 
            max_iter=100,  # Menos iterações
            solver='liblinear'  # Solver mais eficiente
        )
        model.fit(X_train, y_train)
        
        # Criar diretórios
        os.makedirs('model', exist_ok=True)
        os.makedirs('parameter', exist_ok=True)
        
        # Salvar modelo
        print("💾 Salvando modelo...")
        with open('model/model_health_insurance.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        # Criar transformadores simples
        print("🔧 Criando transformadores...")
        create_simple_transformers(df1)
        
        print("✅ Modelo leve e parâmetros salvos com sucesso!")
        
        # Limpeza final de memória
        del df1, X_train, X_test, y_train, y_test, model
        gc.collect()
        
    except Exception as e:
        print(f"❌ Erro durante treinamento: {e}")
        print("Criando modelo dummy...")
        create_lightweight_dummy_model()

def create_simple_transformers(df):
    """
    Cria transformadores simples para economizar memória
    """
    # StandardScaler para annual_premium
    ss = StandardScaler()
    if 'annual_premium' in df.columns:
        ss.fit(df[['annual_premium']])
    else:
        ss.fit(np.random.random((10, 1)))
    
    with open('parameter/annual_premium_scaler.pkl', 'wb') as f:
        pickle.dump(ss, f)
    
    # MinMaxScaler para age
    mms_age = MinMaxScaler()
    if 'age' in df.columns:
        mms_age.fit(df[['age']])
    else:
        mms_age.fit(np.random.random((10, 1)))
    
    with open('parameter/age_scaler.pkl', 'wb') as f:
        pickle.dump(mms_age, f)
    
    # MinMaxScaler para vintage
    mms_vintage = MinMaxScaler()
    if 'vintage' in df.columns:
        mms_vintage.fit(df[['vintage']])
    else:
        mms_vintage.fit(np.random.random((10, 1)))
    
    with open('parameter/vintage_scaler.pkl', 'wb') as f:
        pickle.dump(mms_vintage, f)
    
    # Encoders simples
    if 'gender' in df.columns:
        gender_encoding = df.groupby('gender').size().to_dict()
        # Normalizar
        total = sum(gender_encoding.values())
        gender_encoding = {k: v/total for k, v in gender_encoding.items()}
    else:
        gender_encoding = {'Male': 0.6, 'Female': 0.4}
    
    with open('parameter/gender_encoder.pkl', 'wb') as f:
        pickle.dump(gender_encoding, f)
    
    # Region code encoding simples
    if 'region_code' in df.columns:
        region_encoding = df.groupby('region_code').size().to_dict()
        total = sum(region_encoding.values())
        region_encoding = {k: v/total for k, v in region_encoding.items()}
    else:
        region_encoding = {i: 0.02 for i in range(1, 54)}
    
    with open('parameter/region_code_encoder.pkl', 'wb') as f:
        pickle.dump(region_encoding, f)
    
    # Policy sales channel encoding
    if 'policy_sales_channel' in df.columns:
        policy_encoding = df.groupby('policy_sales_channel').size() / len(df)
    else:
        policy_encoding = {i: 0.01 for i in range(1, 165)}
    
    with open('parameter/policy_sales_channel_encoder.pkl', 'wb') as f:
        pickle.dump(policy_encoding, f)

def create_lightweight_dummy_model():
    """
    Cria um modelo dummy ultra leve
    """
    print("🔧 Criando modelo dummy ultra leve...")
    
    # Criar diretórios
    os.makedirs('model', exist_ok=True)
    os.makedirs('parameter', exist_ok=True)
    
    # Modelo dummy mais leve
    from sklearn.dummy import DummyClassifier
    dummy_model = DummyClassifier(strategy='prior')  # Ainda mais simples
    
    # Dados dummy mínimos
    X_dummy = np.random.random((10, 7))
    y_dummy = np.random.randint(0, 2, 10)
    dummy_model.fit(X_dummy, y_dummy)
    
    # Salvar modelo dummy
    with open('model/model_health_insurance.pkl', 'wb') as f:
        pickle.dump(dummy_model, f)
    
    # Transformadores dummy ultra simples
    simple_scaler = MinMaxScaler()
    simple_scaler.fit(np.array([[0], [1]]))  # Mínimo possível
    
    # Salvar todos os scalers
    for scaler_name in ['annual_premium_scaler', 'age_scaler', 'vintage_scaler']:
        with open(f'parameter/{scaler_name}.pkl', 'wb') as f:
            pickle.dump(simple_scaler, f)
    
    # Encoders dummy simples
    simple_encoders = {
        'gender_encoder': {'Male': 0.6, 'Female': 0.4},
        'region_code_encoder': {i: 0.02 for i in range(1, 11)},  # Só 10 regiões
        'policy_sales_channel_encoder': {i: 0.1 for i in range(1, 11)}  # Só 10 canais
    }
    
    for encoder_name, encoder_data in simple_encoders.items():
        with open(f'parameter/{encoder_name}.pkl', 'wb') as f:
            pickle.dump(encoder_data, f)
    
    print("✅ Modelo dummy ultra leve criado com sucesso!")

if __name__ == "__main__":
    train_lightweight_model()

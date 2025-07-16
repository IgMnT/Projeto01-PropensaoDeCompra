Claro\! Com base no seu notebook Jupyter, preparei um README completo e profissional para o seu projeto no GitHub. Ele destaca a metodologia, os desafios de implantação e a solução final.

-----

# Health Insurance Cross-Sell Prediction

Este projeto tem como objetivo desenvolver um modelo de machine learning para prever a propensão de clientes de um seguro de automóvel a se interessarem também por um seguro de saúde. A solução final é uma API REST implementada com Flask e hospedada na plataforma Render.

O problema de negócio consiste em otimizar a campanha de cross-sell, direcionando os esforços de marketing para os clientes com maior probabilidade de adesão, aumentando a eficiência e o ROI da campanha.

## 1\. Estratégia da Solução

O projeto seguiu uma metodologia baseada no CRISP-DM, com as seguintes etapas:

1.  **Descrição e Limpeza dos Dados:** Análise inicial das variáveis, renomeação de colunas para o padrão `snake_case` e verificação de dados faltantes.
2.  **Feature Engineering:** Transformação de variáveis categóricas (`Vehicle_Age` e `Vehicle_Damage`) para um formato numérico e mais interpretável.
3.  **Análise Exploratória de Dados (EDA):** Investigação de hipóteses e insights através da análise univariada e bivariada, buscando entender o comportamento das variáveis e sua relação com a variável resposta (`Response`).
4.  **Preparação dos Dados:** Aplicação de diversas técnicas de pré-processamento para otimizar a performance dos modelos:
      * **Normalização/Escalonamento:** `StandardScaler` e `MinMaxScaler` em variáveis numéricas.
      * **Encoding:** `Target Encoding`, `One-Hot Encoding` e `Frequency Encoding` em variáveis categóricas.
5.  **Seleção de Features:** Uso do `ExtraTreesClassifier` para ranquear a importância das features e selecionar as mais relevantes para o modelo.
6.  **Modelagem e Avaliação:** Treinamento e avaliação de múltiplos algoritmos de classificação, como K-Nearest Neighbors (KNN), Random Forest e Regressão Logística, com foco em métricas de negócio como Acurácia, Recall e Precisão.
7.  **Deploy em Produção:** Encapsulamento de todo o pipeline em uma classe Python e criação de uma API com Flask para disponibilizar as predições.

## 2\. Top 3 Insights da Análise de Dados

1.  **Clientes Sem Seguro Prévio são o Alvo Principal:** A análise mostrou que **100% dos clientes que já possuíam um seguro de veículo não têm interesse** no seguro de saúde (`previously_insured = 1`). Em contrapartida, clientes que **não tinham seguro prévio representam a totalidade dos interessados**. Isso torna a variável `previously_insured` o fator mais importante na predição.
2.  **Danos no Veículo Aumentam a Propensão:** Clientes que já tiveram o veículo danificado (`Vehicle_Damage = Yes`) demonstram uma propensão de compra **24 vezes maior** do que aqueles que nunca tiveram o veículo danificado.
3.  **Idade e Canal de Venda:** A propensão de compra aumenta significativamente para clientes na faixa etária de **30 a 60 anos**. Além disso, certos canais de venda (`Policy_Sales_Channel`) concentram a grande maioria dos clientes interessados, sugerindo que a otimização da campanha deve focar nesses canais.

## 3\. Modelo de Machine Learning

Foram testados três modelos: KNN, Random Forest e Regressão Logística.

  - **Random Forest** apresentou a melhor acurácia geral (86.52%), porém com baixo recall (12.18%), indicando dificuldade em identificar os clientes interessados devido ao grande desbalanceamento de classes.
  - **Regressão Logística** foi o modelo escolhido para o deploy final devido aos desafios de memória na plataforma Render. Embora a versão padrão tenha apresentado performance similar, a versão com pesos balanceados (`class_weight='balanced'`) atingiu um **Recall de 97.64%**, sendo ideal para o negócio (maximizar a identificação de potenciais clientes), mesmo com uma precisão menor (25.38%).

| Modelo | Acurácia | Recall | Precisão |
| :--- | :--- | :--- | :--- |
| Random Forest | 86.52% | 12.18% | 36.35% |
| Regressão Logística (Balanceada) | 64.26% | 97.64% | 25.38% |

## 4\. Desafios e Soluções no Deploy

A implantação na plataforma Render apresentou desafios significativos que moldaram a solução final:

1.  **Problema de Tamanho do Modelo:** O arquivo do modelo Random Forest (`.pkl`) era muito grande (\>1 GB), excedendo os limites de repositórios Git e plataformas de deploy gratuitas.
2.  **Problema de Memória:** O processo de treinamento do Random Forest consumia mais de 512MB de RAM, estourando o limite do plano gratuito do Render.

**Solução Implementada:**

A solução foi criar um **pipeline de treinamento automático e leve** que é executado durante o build no Render:

  - **Modelo Leve:** Substituição do Random Forest pela **Regressão Logística**, cujo arquivo de modelo tem menos de 1 KB.
  - **Treinamento no Deploy:** Um script `train_lightweight_model.py` foi criado para treinar o modelo e gerar os arquivos `.pkl` dos pré-processadores (scalers, encoders) durante a fase de build no Render.
  - **Dados Mínimos:** O treinamento no build utiliza uma pequena amostra dos dados (`mini_train.csv`) para garantir que o processo seja rápido e consuma pouca memória.

Essa abordagem resolveu ambos os problemas, permitindo um deploy bem-sucedido, robusto e automatizado.

## 5\. Como Usar a API

A API está disponível e pode ser acessada através de requisições POST para o endpoint de predição.

### Endpoint

`POST /healthinsurance/predict`

### Exemplo de Requisição (Python)

```python
import requests
import json

# Exemplo com um único cliente
data = {
    "Gender": "Male",
    "Age": 44,
    "Driving_License": 1,
    "Region_Code": 28.0,
    "Previously_Insured": 0,
    "Vehicle_Age": "< 1 Year",
    "Vehicle_Damage": "Yes",
    "Annual_Premium": 40454.0,
    "Policy_Sales_Channel": 26.0,
    "Vintage": 217
}

# URL da API (substitua pela sua URL do Render)
url = "https://SEU-APP.onrender.com/healthinsurance/predict"
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Prediction: {response.json()}")

```

### Exemplo de Resposta

A API retorna um JSON com os dados do cliente e a coluna `score`, que representa a probabilidade (de 0 a 1) do cliente ter interesse no seguro de saúde.

```json
[
  {
    "id": 1,
    "gender": "Male",
    "age": 44,
    // ...outras colunas...
    "vintage": 217,
    "response": 1,
    "score": 0.2375
  }
]
```

## 6\. Próximos Passos

  - [ ] Implementar um pipeline de CI/CD para automatizar testes e deploys.
  - [ ] Experimentar modelos mais robustos (XGBoost, LightGBM) em uma plataforma com mais recursos de memória.
  - [ ] Realizar mais engenharia de features para melhorar a performance do modelo.
  - [ ] Conduzir um teste A/B para validar o impacto do modelo nos resultados da campanha.

## 7\. Estrutura do Projeto

```
.
├── app.py                  # Handler da API Flask
├── requirements.txt        # Dependências Python
├── train_lightweight_model.py # Script de treinamento para deploy
├── health_insurance/
│   └── HealthInsurance.py  # Classe de encapsulamento do pipeline
├── model/
│   └── model_health.pkl    # Modelo treinado (gerado no deploy)
├── parameter/
│   └── ...                 # Arquivos de pré-processamento (.pkl)
└── notebooks/
    └── sales-prediction.ipynb # Notebook de análise e desenvolvimento
```
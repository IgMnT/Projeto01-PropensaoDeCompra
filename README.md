# Health Insurance Propensity API

Esta API prediz a propensão de clientes comprarem seguro de saúde com base em características demográficas e de veículos.

## Estrutura do Projeto

```
health-insurance-api/
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── health_insurance/
│   ├── __init__.py
│   └── HealthInsurance.py         # Class implementation
├── model/
│   └── model_health_insurance.pkl # Trained model
└── parameter/
    ├── annual_premium_scaler.pkl
    ├── age_scaler.pkl
    ├── vintage_scaler.pkl
    ├── gender_encoder.pkl
    ├── region_code_encoder.pkl
    └── policy_sales_channel_encoder.pkl
```

## Endpoints

### GET /
Página inicial da API com informações básicas.

### GET /health
Endpoint de health check que retorna o status da API.

### POST /healthinsurance/predict
Endpoint principal para fazer predições.

**Formato de entrada (JSON):**
```json
{
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
```

**Formato de saída (JSON):**
```json
{
    "Gender": "Male",
    "Age": 44,
    "Driving_License": 1,
    "Region_Code": 28.0,
    "Previously_Insured": 0,
    "Vehicle_Age": "< 1 Year",
    "Vehicle_Damage": "Yes",
    "Annual_Premium": 40454.0,
    "Policy_Sales_Channel": 26.0,
    "Vintage": 217,
    "score": 0.85
}
```

## Deploy no Render

### Pré-requisitos
1. Conta no GitHub
2. Conta no Render
3. Arquivos do modelo treinado salvos nas pastas corretas

### Passos para Deploy

1. **Prepare o repositório:**
   - Faça commit de todos os arquivos para o GitHub
   - Certifique-se de que os arquivos do modelo estão na pasta `model/`
   - Certifique-se de que os transformadores estão na pasta `parameter/`

2. **Configure no Render:**
   - Conecte seu repositório GitHub ao Render
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Environment:** Python 3

3. **Variáveis de ambiente (opcionais):**
   - `PYTHON_VERSION`: 3.11.0
   - `PORT`: 5000 (automaticamente configurado pelo Render)

4. **Deploy:**
   - Faça o deploy e aguarde a build
   - Sua API estará disponível em: `https://your-app-name.onrender.com`

### Deploy Automatizado

Use o script de deploy automatizado:

```bash
# Validar arquivos
python validate_deploy.py

# Deploy automatizado
python deploy.py
```

## Deploy com Docker (Alternativo)

### Desenvolvimento local com Docker

```bash
# Construir e executar com Docker Compose
docker-compose up --build

# Ou construir e executar manualmente
docker build -t health-insurance-api .
docker run -p 5000:5000 health-insurance-api
```

### Deploy em plataformas que suportam Docker

1. **Render (Docker):**
   - Escolha "Docker" em vez de "Web Service"
   - Use o Dockerfile fornecido

2. **Google Cloud Run:**
   ```bash
   # Fazer build da imagem
   docker build -t gcr.io/seu-projeto/health-insurance-api .
   
   # Push para Container Registry
   docker push gcr.io/seu-projeto/health-insurance-api
   
   # Deploy no Cloud Run
   gcloud run deploy --image gcr.io/seu-projeto/health-insurance-api
   ```

3. **AWS App Runner:**
   - Conecte seu repositório GitHub
   - Configure para usar Dockerfile

## Teste Local

Para testar localmente:

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar a API
python app.py

# Testar endpoints
curl http://localhost:5000/health
curl -X POST http://localhost:5000/healthinsurance/predict \
  -H "Content-Type: application/json" \
  -d '{"Gender": "Male", "Age": 44, "Driving_License": 1, "Region_Code": 28.0, "Previously_Insured": 0, "Vehicle_Age": "< 1 Year", "Vehicle_Damage": "Yes", "Annual_Premium": 40454.0, "Policy_Sales_Channel": 26.0, "Vintage": 217}'
```

## Exemplo de Uso em Python

```python
import requests
import json

# Dados de exemplo
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

# Fazer predição
url = "https://your-app-name.onrender.com/healthinsurance/predict"
headers = {"Content-Type": "application/json"}
response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.json())
```

## Estrutura dos Dados de Entrada

| Campo | Tipo | Descrição |
|-------|------|-----------|
| Gender | string | Gênero do cliente ("Male" ou "Female") |
| Age | integer | Idade do cliente |
| Driving_License | integer | Se possui carteira de motorista (0 ou 1) |
| Region_Code | float | Código da região |
| Previously_Insured | integer | Se já teve seguro anteriormente (0 ou 1) |
| Vehicle_Age | string | Idade do veículo ("< 1 Year", "1-2 Year", "> 2 Years") |
| Vehicle_Damage | string | Se o veículo tem danos ("Yes" ou "No") |
| Annual_Premium | float | Prêmio anual do seguro |
| Policy_Sales_Channel | float | Canal de vendas da apólice |
| Vintage | integer | Número de dias desde que o cliente se associou à empresa |

## Saída

A API retorna os mesmos dados de entrada mais um campo `score` que representa a probabilidade (0-1) do cliente comprar o seguro de saúde.

## Monitoramento

- Health check: `GET /health`
- Logs disponíveis no dashboard do Render
- Métricas de performance no Render
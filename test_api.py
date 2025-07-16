import requests
import json

def test_api(base_url="http://localhost:5000"):
    """
    Teste completo da API Health Insurance
    """
    print("=== Testando Health Insurance API ===")
    print(f"Base URL: {base_url}")
    print()
    
    # 1. Test health endpoint
    print("1. Testando endpoint de health...")
    try:
        health_url = f"{base_url}/health"
        response = requests.get(health_url)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Erro: {e}")
    print()
    
    # 2. Test home endpoint
    print("2. Testando endpoint home...")
    try:
        home_url = f"{base_url}/"
        response = requests.get(home_url)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   Home page funcionando!")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Erro: {e}")
    print()
    
    # 3. Test prediction endpoint - single prediction
    print("3. Testando predição única...")
    try:
        predict_url = f"{base_url}/healthinsurance/predict"
        
        # Sample data for testing
        sample_data = {
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
        
        headers = {'Content-type': 'application/json'}
        response = requests.post(predict_url, data=json.dumps(sample_data), headers=headers)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                print(f"   Score: {result[0].get('score', 'N/A')}")
                print(f"   Resultado completo: {result[0]}")
            else:
                print(f"   Resultado: {result}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   Erro: {e}")
    print()
    
    # 4. Test prediction endpoint - multiple predictions
    print("4. Testando múltiplas predições...")
    try:
        predict_url = f"{base_url}/healthinsurance/predict"
        
        # Multiple sample data
        sample_data = [
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
            },
            {
                "Gender": "Female",
                "Age": 35,
                "Driving_License": 1,
                "Region_Code": 15.0,
                "Previously_Insured": 1,
                "Vehicle_Age": "1-2 Year",
                "Vehicle_Damage": "No",
                "Annual_Premium": 25000.0,
                "Policy_Sales_Channel": 152.0,
                "Vintage": 180
            }
        ]
        
        headers = {'Content-type': 'application/json'}
        response = requests.post(predict_url, data=json.dumps(sample_data), headers=headers)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list):
                print(f"   Número de predições: {len(result)}")
                for i, pred in enumerate(result):
                    print(f"   Cliente {i+1} - Score: {pred.get('score', 'N/A')}")
            else:
                print(f"   Resultado: {result}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   Erro: {e}")
    print()
    
    # 5. Test error handling
    print("5. Testando tratamento de erro...")
    try:
        predict_url = f"{base_url}/healthinsurance/predict"
        
        # Invalid data
        invalid_data = {"invalid": "data"}
        
        headers = {'Content-type': 'application/json'}
        response = requests.post(predict_url, data=json.dumps(invalid_data), headers=headers)
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   Erro: {e}")
    print()
    
    print("=== Teste concluído ===")

if __name__ == "__main__":
    # Teste local
    print("Testando API local...")
    test_api("http://localhost:5000")
    
    # Teste de produção - descomente e atualize com sua URL do Render
    # print("\nTestando API em produção...")
    # test_api("https://health-insurance-api-xxxx.onrender.com")
    
    # Exemplos de URLs comuns do Render:
    # test_api("https://health-insurance-propensity-api.onrender.com")
    # test_api("https://propensao-compra-api.onrender.com")

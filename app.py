import os
import pickle
import pandas as pd
from flask import Flask, request, Response
from health_insurance.HealthInsurance import HealthInsurance

# Check if model exists, if not train it
if not os.path.exists('model/model_health_insurance.pkl'):
    print("Model not found. Training model...")
    try:
        from train_model import train_model
        train_model()
        print("Model trained successfully!")
    except Exception as e:
        print(f"Error training model: {e}")
        print("Creating minimal model for demonstration...")
        
        # Create directories
        os.makedirs('model', exist_ok=True)
        os.makedirs('parameter', exist_ok=True)
        
        # Create minimal dummy model
        from sklearn.dummy import DummyClassifier
        import numpy as np
        
        dummy_model = DummyClassifier(strategy='constant', constant=0.5)
        dummy_model.fit(np.random.random((10, 7)), np.random.randint(0, 2, 10))
        
        with open('model/model_health_insurance.pkl', 'wb') as f:
            pickle.dump(dummy_model, f)
        
        # Create minimal transformers
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        scaler.fit(np.random.random((10, 1)))
        
        for param_name in ['annual_premium_scaler', 'age_scaler', 'vintage_scaler']:
            with open(f'parameter/{param_name}.pkl', 'wb') as f:
                pickle.dump(scaler, f)
        
        for encoder_name in ['gender_encoder', 'region_code_encoder', 'policy_sales_channel_encoder']:
            with open(f'parameter/{encoder_name}.pkl', 'wb') as f:
                pickle.dump({'default': 0.5}, f)

# loading model
model = pickle.load( open( 'model/model_health_insurance.pkl', 'rb') )

# initialize API
app = Flask( __name__ )

@app.route( '/', methods=['GET'] )
def home():
    return '''
    <h1>Health Insurance Propensity API</h1>
    <p>Use POST /healthinsurance/predict to get predictions</p>
    <p>Status: Running on Render</p>
    <p>Available endpoints:</p>
    <ul>
        <li>GET / - This page</li>
        <li>GET /health - Health check</li>
        <li>POST /healthinsurance/predict - Get predictions</li>
    </ul>
    '''

@app.route( '/health', methods=['GET'] )
def health_check():
    return Response( '{"status": "healthy"}', status=200, mimetype='application/json' )

@app.route( '/healthinsurance/predict', methods=['POST'] )
def healthinsurance_predict():
    test_json = request.get_json()
   
    if test_json: # there is data
        try:
            if isinstance( test_json, dict ): # unique example
                test_raw = pd.DataFrame( test_json, index=[0] )
                
            else: # multiple examples
                test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() )
                
            # Instantiate HealthInsurance class
            pipeline = HealthInsurance()
            
            # data cleaning
            df1 = pipeline.data_cleaning( test_raw )
            
            # feature engineering
            df2 = pipeline.feature_engineering( df1 )
            
            # data preparation
            df3 = pipeline.data_preparation( df2 )
            
            # prediction
            df_response = pipeline.get_prediction( model, test_raw, df3 )
            
            return df_response
            
        except Exception as e:
            return Response( f'{{"error": "{str(e)}"}}', status=500, mimetype='application/json' )
        
    else:
        return Response( '{"error": "No data provided"}', status=400, mimetype='application/json' )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run( host='0.0.0.0', port=port, debug=False )

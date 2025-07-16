import pickle
import inflection
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

class HealthInsurance( object ):
    def __init__( self ):
        self.home_path = ''  # Relative path for deployment
        self.annual_premium_scaler = pickle.load( open( self.home_path + 'parameter/annual_premium_scaler.pkl', 'rb') )
        self.age_scaler = pickle.load( open( self.home_path + 'parameter/age_scaler.pkl', 'rb') )
        self.vintage_scaler = pickle.load( open( self.home_path + 'parameter/vintage_scaler.pkl', 'rb') )
        self.gender_encoder = pickle.load( open( self.home_path + 'parameter/gender_encoder.pkl', 'rb') )
        self.region_code_encoder = pickle.load( open( self.home_path + 'parameter/region_code_encoder.pkl', 'rb') )
        self.policy_sales_channel_encoder = pickle.load( open( self.home_path + 'parameter/policy_sales_channel_encoder.pkl', 'rb') )
        
        
    def data_cleaning( self, df1 ): 
        
        ## 1.1. Rename Columns
        cols_old = df1.columns
        snakecase = lambda x: inflection.underscore( x )
        cols_new = list( map( snakecase, cols_old ) )
        
        # rename
        df1.columns = cols_new
        
        ## 1.2. Data Types - convert if necessary
        # No specific data type changes needed for this dataset
        
        ## 1.3. Check for missing values and handle them
        # This dataset doesn't have missing values based on previous analysis
        
        return df1 


    def feature_engineering( self, df2 ):
        
        ## 2.1. Vehicle Age Processing
        df2['vehicle_age'] = df2['vehicle_age'].apply(
            lambda x: 'over2years' if x == '> 2 Years'
            else 'between1and2years' if x == '1-2 Year'
            else 'lessthan1year' if x == '< 1 Year'
            else x
        )
        
        ## 2.2. Vehicle Damage Processing
        df2['vehicle_damage'] = df2['vehicle_damage'].apply(
            lambda x: 1 if str(x).strip().lower() == 'yes' else 0
        )
        
        return df2


    def data_preparation( self, df5 ):

        ## 5.1. Normalization
        # annual_premium
        df5['annual_premium'] = self.annual_premium_scaler.transform( df5[['annual_premium']].values )

        ## 5.2. Rescaling 
        # age
        df5['age'] = self.age_scaler.transform( df5[['age']].values )
        
        # vintage
        df5['vintage'] = self.vintage_scaler.transform( df5[['vintage']].values )

        ## 5.3. Encoding
        # Target Encoding for gender
        df5['gender'] = df5['gender'].map( self.gender_encoder )
        
        # Target Encoding for region_code
        df5['region_code'] = df5['region_code'].map( self.region_code_encoder )
        
        # One Hot Encoding for vehicle_age
        df5 = pd.get_dummies( df5, prefix='vehicle_age', columns=['vehicle_age'] )
        
        # Frequency Encoding for policy_sales_channel
        df5['policy_sales_channel'] = df5['policy_sales_channel'].map( self.policy_sales_channel_encoder )
        
        # Select columns used in the model
        cols_selected = ['annual_premium', 'age', 'vintage', 'region_code', 'policy_sales_channel', 'previously_insured', 'vehicle_damage']
        
        # Handle missing columns after encoding
        available_cols = [col for col in cols_selected if col in df5.columns]
        
        # Add vehicle_age dummy columns if they exist
        vehicle_age_cols = [col for col in df5.columns if col.startswith('vehicle_age_')]
        available_cols.extend(vehicle_age_cols)
        
        return df5[available_cols]
    
    
    def get_prediction( self, model, original_data, test_data ):
        # prediction
        pred = model.predict_proba( test_data )
        
        # join pred into the original data
        original_data['score'] = pred[:, 1]  # probability of buying insurance
        
        return original_data.to_json( orient='records', date_format='iso' )

import json,pickle as pkl
import numpy as np
import pandas as pd
import config
from src.database import get_data_collection


class Teen_Depression:
    def __init__(self):
        pass
    
    def load_model(self):
        """This method is used to load model"""
        with open(config.ML_MODEL_PATH,'rb') as f:
            self.model = pkl.load(f)
        return
    
    def load_column_data(self):
        """"this method is used to load column data"""
        with open(config.JSON_DATA_PATH,'r') as j:
            self.input_columns = json.load(j)
        return self.input_columns
    
    def create_test_df(self):
        """This method is used to create testing DataFrame"""
        self.load_model()
        self.load_column_data()

        test_array = np.zeros((1,self.model.n_features_in_))
        test_array[0,0] = self.data['age']
        test_array[0,1] = self.input_columns['gender'][self.data['gender']]
        test_array[0,2] = self.data['daily_social_media_hours']
        test_array[0,3] = self.data['sleep_hours']
        test_array[0,4] = self.data['screen_time_before_sleep']
        test_array[0,5] = self.data['academic_performance']
        test_array[0,6] = self.data['physical_activity']
        test_array[0,7] = self.input_columns['social_interaction_level'][self.data['social_interaction_level']]
        test_array[0,8] = self.data['stress_level']
        test_array[0,9] = self.data['anxiety_level']
        test_array[0,10] = self.data['addiction_level']
        
        platform_usage = f'platform_usage_{self.data["platform_usage"]}'

        platform_usage_idx = np.where(self.model.feature_names_in_ == platform_usage)[0]
        test_array[0,platform_usage_idx] = 1
        self.test_df = pd.DataFrame(test_array, columns=self.model.feature_names_in_)
        return test_array
    
    def predict_depression_label(self,user_input_data):
        """This method is used to predict depression level"""
        
        self.data = dict(user_input_data)
        self.data['age'] = int(self.data['age'])
        self.data['daily_social_media_hours'] = float(self.data['daily_social_media_hours'])
        self.data['sleep_hours'] = float(self.data['sleep_hours'])
        self.data['screen_time_before_sleep'] = float(self.data['screen_time_before_sleep'])
        self.data['academic_performance'] = float(self.data['academic_performance'])
        self.data['physical_activity'] = float(self.data['physical_activity'])
        self.data['stress_level'] = int(self.data['stress_level'])
        self.data['anxiety_level'] = int(self.data['anxiety_level'])
        self.data['addiction_level'] = int(self.data['addiction_level'])
        
        self.create_test_df() #Calling function for dataframe creation
        self.prediction = self.model.predict(self.test_df)
        print(f"Predicted Depression Label (1 means Yes 0 means No): {self.prediction}")
        return self.prediction
    
    def save_data_in_db(self):
        input_data = self.data
        input_data.update({'Prediction':int(self.prediction[0])})
        data_collection = get_data_collection()
        data_collection.insert_one(input_data)
        return
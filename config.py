import os

FLASK_HOST = '0.0.0.0'
FLASK_PORT = "5000"

MONGO_URL = "mongodb://localhost:27017"
db_name = 'Teen_Depression_db'
user_collection_name = 'user_data'
data_collection_name = 'model_data'

ML_MODEL_PATH = os.path.join(os.getcwd(),'artifacts','Teen_Depr_final_model.pkl')
JSON_DATA_PATH = os.path.join(os.getcwd(),'artifacts','Teen_depr_coln_data.json')
INPUT_DATA_PATH = os.path.join(os.getcwd(),'data',"Teen_Mental_Health_Dataset.csv")

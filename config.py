import os

FLASK_HOST = '0.0.0.0'
FLASK_PORT = "8000"
MONGO_USERNAME = "rishabhp"
MONGO_PASSWORD = "test123$"
MONGO_URL = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@docdb-cluster-20260630-0923.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
db_name = 'Teen_Depression_db'
user_collection_name = 'user_data'
data_collection_name = 'model_data'

STD_SCALER_PATH = os.path.join(os.getcwd(),'artifacts','std_scaler.pkl')
ML_MODEL_PATH = os.path.join(os.getcwd(),'artifacts','Teen_Depr_final_model.pkl')
JSON_DATA_PATH = os.path.join(os.getcwd(),'artifacts','Teen_depr_coln_data.json')
INPUT_DATA_PATH = os.path.join(os.getcwd(),'data',"Teen_Mental_Health_Dataset.csv")

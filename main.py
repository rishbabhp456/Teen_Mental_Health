from flask import Flask,request, jsonify, render_template, redirect, url_for, session
from flask_jwt_extended import JWTManager, create_access_token # Removed jwt_required, get_jwt_identity as they are not used in the provided routes
import config,pymongo
import datetime,pandas as pd
from src.utils import Teen_Depression
obj_teen_depression = Teen_Depression()


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'secret'
app.config['SECRET_KEY'] = 'flask-session-secret'
jwt = JWTManager(app)

client = pymongo.MongoClient(config.MONGO_URL)
db = client[config.db_name]
user_collection = db[config.user_collection_name]

@app.route('/')
def index():
    return redirect(url_for('login_page'))


@app.route("/login_page")
def login_page():
    return render_template('login.html')

@app.route("/register_page")
def register_page():
    return render_template('register.html')

@app.route("/forgot_password_page")
def forgot_password_page():
    return render_template('forgot_password.html')

# The /register route remains an API endpoint for POST requests from JS


@app.route('/register', methods=['POST'])
def register():

    user_data = request.form
    user_name = user_data['user_name']
    user_password = user_data['password']
    user_email = user_data['email']
    contact =  user_data['contact']
    dob =  user_data['dob']
    gender =  user_data['gender']
    response = user_collection.find_one({'user_name':user_name,'email':user_email})
    if not response:
        user_collection.insert_one({'user_name':user_name,'password':user_password,
                                    'email':user_email,'contact':contact,'dob':dob,'gender':gender})
        return jsonify({"status": "success", "message": "Registration Successful"})
    else:
        return jsonify({"status": "failure", "message": "User Already Exists"})

# The /login route remains an API endpoint for POST requests from JS

@app.route('/login', methods=['POST'])
def login():
    
    user_data = request.form
    user_name =  user_data['user_name']
    user_password = user_data['password']
    response = user_collection.find_one({'user_name':user_name,'password':user_password})
    if response:
        access_token = create_access_token(
            identity=user_name,            
            expires_delta=datetime.timedelta(minutes=1))
        return jsonify({"status": "success","message": "Login Successful", 
                        "access_token":access_token})
    else:
        return jsonify({"status": "failure", "message": "Invalid Credentials"})
    
    
@app.route("/prediction_form_page")
# @jwt_required() # You might want to uncomment this line if you want to protect the prediction page
def prediction_form_page():
    return render_template('predict.html')

@app.route("/predict_depression",methods=['POST'])
def predict_depression():
    user_input_data = request.form
    prediction_array = obj_teen_depression.predict_depression_label(user_input_data) # prediction_array is a numpy array like [0] or [1]
    # Extract the integer prediction from the numpy array
    prediction_label = int(prediction_array[0])
    obj_teen_depression.save_data_in_db() # Call to save the input data and prediction to the database
    return jsonify({"status": "success", "prediction": prediction_label, "prediction_meaning": "1 means Yes, 0 means No"})


@app.route("/gender_options")
def gender_options():
    """
    this Method is used for showing options in dropdown
    """
    col_data = obj_teen_depression.load_column_data()
    gender_values = list(col_data['gender'].keys())
    return jsonify(gender_values)

@app.route("/social_interaction_level_options")
def social_interact_lvl_opt():
    """
    this Method is used for showing options in dropdown
    """
    col_data = obj_teen_depression.load_column_data()
    social_interact_lvl_values = list(col_data['social_interaction_level'].keys())
    return jsonify(social_interact_lvl_values)

@app.route("/platform_usage_options")
def platform_usage_opt():
    """
    This method is for showing options in dropdown
    """   
    df = pd.read_csv(config.INPUT_DATA_PATH)
    platform_usage_values = list(df['platform_usage'].unique())
    return jsonify(platform_usage_values)



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
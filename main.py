from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_jwt_extended import JWTManager, create_access_token
import config
import pymongo
import datetime
import pandas as pd
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


@app.route('/login_page')
def login_page():
    return render_template('login.html')


@app.route('/register_page')
def register_page():
    return render_template('register.html')


@app.route('/forgot_password_page')
def forgot_password_page():
    return render_template('forgot_password.html')


@app.route('/register', methods=['POST'])
def register():
    user_data = request.form
    user_name = user_data.get('user_name', '').strip()
    user_password = user_data.get('password', '').strip()
    user_email = user_data.get('email', '').strip()
    contact = user_data.get('contact', '').strip()
    dob = user_data.get('dob', '').strip()
    gender = user_data.get('gender', '').strip()

    if not all([user_name, user_password, user_email]):
        return jsonify({"status": "failure", "message": "Please fill in the required fields"})

    response = user_collection.find_one({'user_name': user_name, 'email': user_email})
    if not response:
        user_collection.insert_one({
            'user_name': user_name,
            'password': user_password,
            'email': user_email,
            'contact': contact,
            'dob': dob,
            'gender': gender
        })
        return jsonify({"status": "success", "message": "Registration successful"})
    return jsonify({"status": "failure", "message": "User already exists"})


@app.route('/login', methods=['POST'])
def login():
    user_data = request.form
    user_name = user_data.get('user_name', '').strip()
    user_password = user_data.get('password', '').strip()

    response = user_collection.find_one({'user_name': user_name, 'password': user_password})
    if response:
        session['user_name'] = user_name
        access_token = create_access_token(
            identity=user_name,
            expires_delta=datetime.timedelta(minutes=20)
        )
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "access_token": access_token
        })
    return jsonify({"status": "failure", "message": "Invalid username or password"})


@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    user_data = request.form
    user_name = user_data.get('user_name', '').strip()
    user_email = user_data.get('email', '').strip()
    new_password = user_data.get('new_password', '').strip()
    
    if not all([user_name, user_email, new_password]):
        return jsonify({"status": "failure", "message": "Please fill in all fields"})
    
    response = user_collection.find_one({'user_name': user_name, 'email': user_email})
    if response:
        user_collection.update_one(
            {'user_name': user_name, 'email': user_email},
            {"$set": {"password": new_password}}
        )
        return jsonify({"status": "success", "message": "Password Updated Successfully"})
    else:
        return jsonify({"status": "failure", "message": "Invalid User Credentials"})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


@app.route('/prediction_form_page')
def prediction_form_page():
    if 'user_name' not in session:
        return redirect(url_for('login_page'))
    return render_template('predict.html', user_name=session['user_name'])


@app.route('/predict_depression', methods=['POST'])
def predict_depression():
    user_input_data = request.form
    prediction_array = obj_teen_depression.predict_depression_label(user_input_data)
    prediction_label = int(prediction_array[0])
    obj_teen_depression.save_data_in_db()
    
    # Generate meaningful message based on prediction
    if prediction_label == 1:
        message = "⚠️ Depression Risk Detected - Please seek a professional support for your mental health."
        is_depressed = True
    else:
        message = "✅ You're Doing Well - Keep up the healthy habits!"
        is_depressed = False
    
    return jsonify({
        "status": "success", 
        "prediction": prediction_label,
        "is_depressed": is_depressed,
        "message": message
    })


@app.route('/gender_options')
def gender_options():
    """
    This method is used for showing options in dropdown
    """
    col_data = obj_teen_depression.load_column_data()
    gender_values = list(col_data['gender'].keys())
    return jsonify(gender_values)


@app.route('/social_interaction_level_options')
def social_interact_lvl_opt():
    """
    This method is used for showing options in dropdown
    """
    col_data = obj_teen_depression.load_column_data()
    social_interact_lvl_values = list(col_data['social_interaction_level'].keys())
    return jsonify(social_interact_lvl_values)


@app.route('/platform_usage_options')
def platform_usage_opt():
    """
    This method is for showing options in dropdown
    """
    df = pd.read_csv(config.INPUT_DATA_PATH)
    platform_usage_values = list(df['platform_usage'].unique())
    return jsonify(platform_usage_values)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
# Teen Mental Health Predictor 🧠

A web application that predicts depression risk among teenagers using Flask, Logistic Regression ML model, and MongoDB.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Set and Run](#set-and-run)
- [API Endpoints](#api-endpoints)
- [Project Flow](#project-flow)
- [Azure Deployment](#azure-deployment)

## Features

- **User Authentication**: Secure registration, login, password reset with JWT
- **Depression Prediction**: 11-field assessment using Logistic Regression model
- **Dynamic Dropdowns**: Backend-populated gender, interaction level, platform options
- **Data Logging**: MongoDB persistence for user inputs and predictions
- **Modern UI**: Animated gradient background, glassmorphic design

## Tech Stack

**Backend**: Flask | **ML Model**: Scikit-learn (Logistic Regression) | **Database**: MongoDB | **Auth**: Flask-JWT-Extended | **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5

## Set and Run

```bash
cd Teen_Mental_Health
python -m venv .venv
.\.venv\scripts\activate  # Windows
source .venv/bin/activate # macOS/Linux

pip install -r requirements.txt

# Configure config.py with MongoDB credentials
python main.py
```
Access at: `http://127.0.0.1:5000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register new user |
| POST | `/login` | Authenticate user, return JWT token |
| POST | `/forgot_password` | Reset password via username + email |
| POST | `/predict_depression` | Get depression risk prediction |
| GET | `/gender_options`, `/social_interaction_level_options`, `/platform_usage_options` | Dynamic dropdown data |

## Project Flow

1. **Register** → 2. **Login** → 3. **Assessment Form** → 4. **Submit Data** → 5. **ML Prediction** → 6. **MongoDB Logging** → 7. **Display Result** (0=No Depression ✅ or 1=Risk Detected ⚠️)

## Azure Deployment

### Prerequisites
- Azure App Service (Python 3.9+)
- Azure Cosmos DB or MongoDB Atlas
- Azure Key Vault for secrets

### Environment Variables
```
MONGO_URL=<your_mongodb_connection_string>
db_name=teen_mental_health
user_collection_name=users
JWT_SECRET_KEY=<secure_random_key>
SECRET_KEY=<secure_session_key>
FLASK_ENV=production
```

### Deployment Steps

1. **Create Azure App Service**
   ```bash
   az webapp create --resource-group <group> --plan <plan> --name <app-name> --runtime "PYTHON|3.9"
   ```

2. **Configure App Settings**
   - Go to App Service → Configuration → Application Settings
   - Add all environment variables from above

3. **Deploy Code**
   ```bash
   az webapp deployment source config-zip --resource-group <group> --name <app-name> --src app.zip
   ```

4. **Set Startup Command** (Configuration → General)
   ```
   gunicorn --bind 0.0.0.0 --workers 4 main:app
   ```

5. **Install gunicorn**
   ```bash
   pip install gunicorn
   echo gunicorn >> requirements.txt
   ```

6. **Enable Logging**
   - App Service → App Service logs → Enable Application Logging (Filesystem)

### Production Checklist
- ✅ Use Azure Key Vault for secrets (don't store in config.py)
- ✅ Set `debug=False` in production
- ✅ Use HTTPS only (`SESSION_COOKIE_SECURE=True`)
- ✅ Set CORS headers appropriately
- ✅ Monitor via Application Insights

### Troubleshooting
- Check logs: `az webapp log tail --resource-group <group> --name <app-name>`
- Verify MongoDB connection string
- Ensure all pip packages in requirements.txt

---

## ⚠️ Disclaimer

**Predictive tool only—NOT a substitute for professional mental health evaluation.** Seek professional help if needed. 💙

**Version**: 1.0.0 | Python 3.9+ | Last Updated: July 3, 2026

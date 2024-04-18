from django.shortcuts import render
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder
# Create your views here.

data = pd.read_csv("aqi_app/city_day.csv")
data.dropna(axis = 0, inplace = True)


# Select features and target
feature_columns = ['City', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2',
                   'O3', 'Benzene', 'Toluene', 'Xylene']
x = data[feature_columns]
y = data['AQI']

# Convert 'City' to numerical labels using LabelEncoder
city_encoder = LabelEncoder()
x['City'] = city_encoder.fit_transform(x['City'])

# load the model
with open('aqi_app/random_forest_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('aqi_app/city_encoder.pkl', 'rb') as file:
    city_encoder = pickle.load(file)
    print(city_encoder)

def predict_aqi(request):
    if request.method == 'POST':
        # Get input parameters from the form
        city = request.POST.get('city')
        pm25 = float(request.POST.get('pm25'))
        pm10 = float(request.POST.get('pm10'))
        no = float(request.POST.get('no'))
        no2 = float(request.POST.get('no2'))
        nox = float(request.POST.get('nox'))
        nh3 = float(request.POST.get('nh3'))
        co = float(request.POST.get('co'))
        so2 = float(request.POST.get('so2'))
        o3 = float(request.POST.get('o3'))
        benzene = float(request.POST.get('benzene'))
        toluene = float(request.POST.get('toluene'))
        xylene = float(request.POST.get('xylene'))

        city_encoder = LabelEncoder()
        city_encoded = city_encoder.fit_transform([city])
        # Encode 'City' input

        # try: 
        #     city_encoded = city_encoder.transform([city])
        # except ValueError:
        #     # Handle unseen label by assigning a default value or special treatment
        #     # For example, you can assign a numerical code for unseen labels
        #     city_encoded = [0] 
        # create input data for prediction
        user_input = pd.DataFrame({
            'City' : city_encoded,
            'PM2.5': [pm25], 'PM10': [pm10], 'NO': [no], 'NO2': [no2], 'NOx': [nox],
            'NH3': [nh3], 'CO': [co], 'SO2': [so2], 'O3': [o3], 'Benzene': [benzene],
            'Toluene': [toluene], 'Xylene': [xylene]
        })
        print("City encode is: ",city_encoded)
        # Make prediction
        predicted_aqi = model.predict(user_input)[0]
        return render(request, 'aqi_app/result.html', {'predicted_aqi' : predicted_aqi})
    return render(request, 'aqi_app/predict.html')
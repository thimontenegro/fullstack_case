import streamlit as st
import requests 
import json 

st.title('Model Prediciton')
"""
'latitude', 'longitude',
       'garageSpaces', 'hasSpa', 'yearBuilt', 'numOfPatioAndPorchFeatures',
       'lotSizeSqFt', 'avgSchoolRating', 'MedianStudentsPerTeacher',
       'numOfBathrooms', 'numOfBedrooms','priceRange', 'year_1900-1920', 'year_1920-1940', 'year_1940-1960',
       'year_1960-1980', 'year_1980-2000', 'year_2000-2010', 'year_2010-2020',
       'home_type_Multi Residential', 'home_type_Other',
       'home_type_Single Residential'"
"""

#continuous variables
latitude = st.number_input('Latitude', value = 0.0)
longitude = st.number_input('longitude', value = 0.0)
garageSpaces = st.number_input('garageSpaces', value = 0.0)
numOfPatioAndPorchFeatures = st.number_input('numOfPatioAndPorchFeatures', value = 0.0)
lotSizeSqFt = st.number_input('lotSizeSqFt', value = 0.0)
avgSchoolRating = st.number_input('avgSchoolRating', value = 0.0)
MedianStudentsPerTeacher = st.number_input('MedianStudentsPerTeacher', value = 0.0)
numOfBathrooms = st.number_input('numOfBathrooms', value = 0.0)
numOfBedrooms = st.number_input('numOfBedrooms', value = 0.0)

# dummy variables
hasSpa = st.selectbox('Has Spa?', ['Yes','No'])
#treat has spa
hasSpa_value = 1 if hasSpa.lower() == 'yes' else 0

#year variable 
year_options_list = ['year_1900-1920', 'year_1920-1940', 'year_1940-1960',
       'year_1960-1980', 'year_1980-2000', 'year_2000-2010', 'year_2010-2020']
year_option =st.selectbox('Choose the desire year of the house.', year_options_list)

year_dict_values = {option: 0 for  option in year_options_list}
year_dict_values[year_option] = 1

# home type
home_options_list = ['home_type_Multi Residential', 'home_type_Other',
       'home_type_Single Residential']
home_option =st.selectbox('Choose the home type of your desire house.', home_options_list)

home_dict_values = {option: 0 for  option in home_options_list}
home_dict_values[home_option] = 1

if st.button('Predict'):
    payload = {'latitude':latitude, 'longitude':longitude,
       'garageSpaces':garageSpaces, 'hasSpa':hasSpa_value,
       'numOfPatioAndPorchFeatures':numOfPatioAndPorchFeatures,
       'lotSizeSqFt':lotSizeSqFt, 'avgSchoolRating':avgSchoolRating, 'MedianStudentsPerTeacher':MedianStudentsPerTeacher,
       'numOfBathrooms':numOfBathrooms, 'numOfBedrooms':numOfBedrooms,
       **year_dict_values,
       **home_dict_values
    }
    st.write(payload)

    def predict(data):
        url = 'http://127.0.0.1:8000/predict'
        headers = {'Content-Type': 'application/json'}
        print(data)
        try:
            response = requests.post(url, data = json.dumps(data), headers =headers)
            return response.json()

        except requests.exceptions.RequestException as e:
            st.error(e)
            return None 
    prediction = predict(payload)
    print(prediction)
    if prediction and 'prediction' in prediction:
        st.success(f"Price {prediction['prediction']}")
    else:
        st.error('Wrong API Call')

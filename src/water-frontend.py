import streamlit as st
from PIL import Image
import requests
import joblib

st.title("Water Potability Classifier")
st.markdown('by: Chris Trihardy')
st.divider()
st.subheader("Type the values and click 'Predict'")


# form input
with st.form("water-ap-form"):

    ph = st.number_input("pH:")
    hardness = st.number_input("Hardness:")
    solids = st.number_input("Solids:")
    chloramines = st.number_input("Chloramines:")
    sulfate = st.number_input("Sulfate:")
    conductivity = st.number_input("Conductivity:")
    organic_carbon = st.number_input("Organic Carbon:")
    trihalomethanes = st.number_input("Trihalomethanes:")
    turbidity = st.number_input("Turbidity:")

    # submmit button
    submitted = st.form_submit_button("Predict")

    #check if button clicked
    if submitted:
        # post data
        data = {
            "ph": ph,
            "Hardness": hardness,
            "Solids": solids,
            "Chloramines": chloramines,
            "Sulfate": sulfate,
            "Conductivity": conductivity,
            "Organic_carbon": organic_carbon,
            "Trihalomethanes": trihalomethanes,
            "Turbidity": turbidity
        }

        # post request
        response = requests.post("http://backend:8000/predict", json = data)

        # get response
        result = response.json()

        # check response
        if result['code'] == 200:
            if result['prediction'] == 'non-potable':
                
                messages = "The water is: " + result['prediction'] + ", do not drink this"
                st.write('Prediction success!!')
                st.success(messages)

            else:
                messages = "The water is: " + result['prediction'] + ", safe to drink"
                st.write('Prediction success!!')
                st.success(messages)

        else:
            st.error(result['messages'])




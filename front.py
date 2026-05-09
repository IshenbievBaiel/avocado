import streamlit as st
import requests


api_url = 'http://127.0.0.1:8000/predict'

st.title('Avocado')
firmness = st.number_input('firmness',min_value=0.0, step=0.1)
hue = st.number_input('hue', min_value=0.0, step=0.1)
saturation = st.number_input('saturation', min_value=0.0, step=0.1)
brightness = st.number_input('brightness', min_value=0.0, step=0.0)
color_category = st.selectbox('color_category', ['dark', 'green', 'purple'])
sound_db = st.number_input('sound_db', min_value=0.0, step=0.1)
weight_g = st.number_input('weight_g', min_value=0.0, step=0.1)
size_cm3 = st.number_input('size_cm3', min_value=0.0, step=0.1)



data = {
    'firmness': firmness,
    'hue': hue,
    'saturation': saturation,
    'brightness': brightness,
    'color_category': color_category,
    'sound_db': sound_db,
    'weight_g': weight_g,
    'size_cm3': size_cm3
}


if st.button('Predict'):
    try:
        answer = requests.post(api_url, json=data, timeout=10)
        if answer.status_code == 200:
            result = answer.json()
            st.success(f"Answer: {result.get('Answer')}")
        else:
            st.error(f'Ошибка: {answer.status_code}')
    except requests.exceptions.RequestException:
        st.error('Ошибка подключения к API')
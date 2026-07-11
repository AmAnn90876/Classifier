import streamlit as st
import pickle
import re
import sklearn

# [ضع الكود الخاص بـ category_map و CustomUnpickler و load model هنا كما هو]

st.title("نظام تصنيف الشكاوى")

complaint_text = st.text_area("أدخل نص الشكوى:")

if st.button("تصنيف"):
    if complaint_text:
        cleaned = clean_text(complaint_text)
        vectorized_text = vectorizer.transform([cleaned])
        prediction_numeric = int(model.predict(vectorized_text)[0])
        prediction_text = category_map.get(prediction_numeric, f"قسم رقم {prediction_numeric}")
        
        st.success(f"التصنيف المتوقع هو: {prediction_text}")
    else:
        st.warning("يرجى إدخال نص الشكوى أولاً.")

import streamlit as st
import pickle
import re
import sklearn

# 1. إعدادات الصفحة
st.set_page_config(page_title="نظام تصنيف البلاغات", page_icon="🤖")

# 2. كود الـ CSS لتعديل الألوان وتطابق التصميم
st.markdown("""
    <style>
    /* جعل الزر باللون الأخضر */
    div.stButton > button:first-child {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold;
        width: 100%;
    }
    /* تنسيق مربع النتيجة */
    .stAlert {
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. القاموس والتحميل
category_map = {
    0: "إنارة", 1: "الإنارة", 2: "التشوه البصري", 3: "الحدائق", 4: "الصيانة",
    5: "الطرق", 6: "المرور", 7: "النظافة", 8: "تشوه بصري", 9: "تصريف الأمطار",
    10: "حدائق", 11: "حفريات", 12: "طرق", 13: "مبانٍ قابلة للسقوط", 14: "نظافة"
}

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'sklearn.linear_model._logistic':
            return super().find_class('sklearn.linear_model', name)
        return super().find_class(module, name)

@st.cache_resource
def load_models():
    with open('model.pkl', 'rb') as f:
        model = CustomUnpickler(f).load()
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = CustomUnpickler(f).load()
    return model, vectorizer

# تحميل النماذج
try:
    model, vectorizer = load_models()
except:
    st.error("خطأ: تأكد من وجود ملفات model.pkl و vectorizer.pkl")

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'[\d\u0660-\u0669]+', '', text)
    return text.strip()

# 4. الواجهة البرمجية (Layout)
st.markdown("<h2 style='text-align: center;'>نظام تصنيف البلاغات الذكي 🤖</h2>", unsafe_allow_html=True)
st.write("<p style='text-align: center;'>أدخل نص الشكوى أو البلاغ ليقوم النموذج بتحديد التصنيف المناسب تلقائياً.</p>", unsafe_allow_html=True)

# مربع النص
complaint_input = st.text_area("", placeholder="هنا اكتب نص الشكوى...")

# الزر
if st.button("تصنيف البلاغ الحالي"):
    if complaint_input:
        cleaned = clean_text(complaint_input)
        vectorized_text = vectorizer.transform([cleaned])
        prediction_numeric = int(model.predict(vectorized_text)[0])
        prediction_text = category_map.get(prediction_numeric, f"قسم رقم {prediction_numeric}")
        
        # النتيجة
        st.write("التصنيف المتوقع بواسطة النموذج:")
        st.success(prediction_text)
    else:
        st.warning("يرجى إدخال نص الشكوى أولاً.")

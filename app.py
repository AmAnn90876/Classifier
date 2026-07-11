import streamlit as st
import pickle
import re
import sklearn

# 1. إعدادات الصفحة
st.set_page_config(page_title="نظام تصنيف البلاغات", page_icon="🤖")

# 2. كود الـ CSS لجعل الشكل "صندوق" ولون الزر الأخضر
st.markdown("""
    <style>
    /* تنسيق الحاوية (الصندوق) */
    .main-box {
        border: 1px solid #e6e6e6;
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    /* جعل الزر باللون الأخضر */
    div.stButton > button:first-child {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 3. تحميل النماذج (نفس منطقك)
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

model, vectorizer = load_models()

# 4. الواجهة داخل "صندوق"
with st.container():
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center;'>نظام تصنيف البلاغات الذكي 🤖</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>أدخل نص الشكوى أو البلاغ ليقوم النموذج بتحديد التصنيف المناسب تلقائياً.</p>", unsafe_allow_html=True)
    
    complaint_input = st.text_area("", placeholder="هنا اكتب نص الشكوى...")
    
    if st.button("تصنيف البلاغ الحالي"):
        if complaint_input:
            # معالجة النص
            cleaned = re.sub(r'[^\w\s]', '', complaint_input)
            cleaned = re.sub(r'[\d\u0660-\u0669]+', '', cleaned).strip()
            
            vectorized_text = vectorizer.transform([cleaned])
            prediction_numeric = int(model.predict(vectorized_text)[0])
            
            # القاموس
            category_map = {
                0: "إنارة", 1: "الإنارة", 2: "التشوه البصري", 3: "الحدائق", 4: "الصيانة",
                5: "الطرق", 6: "المرور", 7: "النظافة", 8: "تشوه بصري", 9: "تصريف الأمطار",
                10: "حدائق", 11: "حفريات", 12: "طرق", 13: "مبانٍ قابلة للسقوط", 14: "نظافة"
            }
            
            prediction_text = category_map.get(prediction_numeric, f"قسم رقم {prediction_numeric}")
            
            st.write("التصنيف المتوقع بواسطة النموذج:")
            st.success(prediction_text)
        else:
            st.warning("يرجى إدخال نص الشكوى أولاً.")
            
    st.markdown('</div>', unsafe_allow_html=True)

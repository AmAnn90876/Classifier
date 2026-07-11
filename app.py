import streamlit as st
import pickle
import re
import sklearn

# إعدادات الصفحة
st.set_page_config(page_title="نظام تصنيف البلاغات", page_icon="🤖")

# كود CSS المطور لتحسين الشكل
st.markdown("""
    <style>
    /* خلفية الصفحة */
    .stApp { background-color: #f0f2f6; }
    
    /* الحاوية الرئيسية */
    .main-box {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    
    /* تنسيق العنوان */
    .title-text { color: #1e1e1e; font-size: 24px; font-weight: 800; text-align: center; margin-bottom: 10px; }
    
    /* تنسيق النص الفرعي */
    .subtitle-text { color: #666; text-align: center; margin-bottom: 30px; font-size: 15px; }
    
    /* تنسيق مربع النص */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        font-size: 16px;
        padding: 10px;
    }
    
    /* تحسين الزر */
    div.stButton > button {
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 10px !important;
        height: 50px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
        transition: 0.3s !important;
    }
    div.stButton > button:hover { background-color: #218838 !important; transform: scale(1.02); }
    
    /* مربع النتيجة */
    .result-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #c3e6cb;
        margin-top: 20px;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# المنطق البرمجي (النماذج)
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'sklearn.linear_model._logistic':
            return super().find_class('sklearn.linear_model', name)
        return super().find_class(module, name)

@st.cache_resource
def load_models():
    with open('model.pkl', 'rb') as f: model = CustomUnpickler(f).load()
    with open('vectorizer.pkl', 'rb') as f: vectorizer = CustomUnpickler(f).load()
    return model, vectorizer

model, vectorizer = load_models()

# واجهة المستخدم
st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.markdown('<p class="title-text">نظام تصنيف البلاغات الذكي 🤖</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">أدخل تفاصيل البلاغ ليقوم الذكاء الاصطناعي بتصنيفه</p>', unsafe_allow_html=True)

user_input = st.text_area("", placeholder="مثال: هناك حفرة في الطريق تحتاج صيانة...")

if st.button("تصنيف البلاغ الحالي"):
    if user_input:
        cleaned = re.sub(r'[^\w\s]', '', user_input)
        vec = vectorizer.transform([cleaned])
        pred = int(model.predict(vec)[0])
        
        cats = {0: "إنارة", 1: "الإنارة", 2: "التشوه البصري", 3: "الحدائق", 4: "الصيانة", 5: "الطرق", 6: "المرور", 7: "النظافة", 8: "تشوه بصري", 9: "تصريف الأمطار", 10: "حدائق", 11: "حفريات", 12: "طرق", 13: "مبانٍ قابلة للسقوط", 14: "نظافة"}
        
        st.markdown(f'<div class="result-box">التصنيف المتوقع:<br><b style="font-size: 22px;">{cats.get(pred)}</b></div>', unsafe_allow_html=True)
    else:
        st.warning("الرجاء كتابة نص البلاغ!")
st.markdown('</div>', unsafe_allow_html=True)

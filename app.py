import streamlit as st
import pickle
import re
import sklearn
import time

# إعدادات الصفحة
st.set_page_config(page_title="نظام التصنيف الذكي", layout="centered")

# CSS لتصميم احترافي
st.markdown("""
    <style>
    .card { background: white; padding: 2rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .stApp { background-color: #f8f9fa; }
    div.stButton > button { width: 100%; border-radius: 50px; background: linear-gradient(135deg, #4fd1c5, #38b2ac); color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# القاموس (تأكد أن هذا هو نفس الترتيب الذي استخدمته في الـ LabelEncoder عند التدريب)
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
    with open('model.pkl', 'rb') as f: model = CustomUnpickler(f).load()
    with open('vectorizer.pkl', 'rb') as f: vectorizer = CustomUnpickler(f).load()
    return model, vectorizer

model, vectorizer = load_models()

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'[\d\u0660-\u0669]+', '', text)
    return text.strip()

# الواجهة
st.markdown('<div class="card">', unsafe_allow_html=True)
st.title("🤖 نظام التصنيف الذكي")

user_input = st.text_area("نص البلاغ", placeholder="اكتب تفاصيل البلاغ هنا...")

if st.button("تحليل وتصنيف البلاغ 🚀"):
    if user_input:
        with st.spinner('جاري التحليل...'):
            cleaned = clean_text(user_input)
            vec = vectorizer.transform([cleaned])
            
            # التنبؤ
            pred_index = int(model.predict(vec)[0])
            
            # --- أداة الفحص (لحل مشكلة التصنيف الخاطئ) ---
            with st.expander("🛠️ أداة فحص الموديل (للمطور)"):
                st.write("النص بعد التنظيف:", cleaned)
                st.write("الرقم الذي توقعه الموديل:", pred_index)
            # ---------------------------------------------
            
            prediction = category_map.get(pred_index, "غير معروف")
            
            st.success(f"✅ التصنيف المتوقع: {prediction}")
    else:
        st.warning("يرجى كتابة نص البلاغ!")
st.markdown('</div>', unsafe_allow_html=True)

# مثال لتصميم لوحة التدقيق
with st.sidebar:
    st.subheader("⚙️ إعدادات المدقق")
    confidence_level = st.slider("درجة الثقة الدنيا", 0.5, 1.0, 0.8)
    show_details = st.checkbox("عرض التفاصيل الفنية")

col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_area("نص البلاغ المراد تدقيقه:", height=200)

with col2:
    st.subheader("نتائج التدقيق")
    if st.button("بدء التدقيق"):
        # محاكاة حالة العمل
        with st.status("جاري التدقيق...", expanded=True) as status:
            st.write("تنظيف النص...")
            time.sleep(1)
            st.write("تحليل المعطيات...")
            time.sleep(1)
            status.update(label="تم التصنيف بنجاح!", state="complete")
        
        st.metric("التصنيف", "حفريات", "98%")

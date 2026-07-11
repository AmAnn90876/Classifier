import streamlit as st
import pickle
import re
import sklearn

# القاموس الخاص بك
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

# تحميل النماذج
@st.cache_resource
def load_models():
    with open('model.pkl', 'rb') as f:
        model = CustomUnpickler(f).load()
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = CustomUnpickler(f).load()
    return model, vectorizer

model, vectorizer = load_models()

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'[\d\u0660-\u0669]+', '', text)
    return text.strip()

# واجهة المستخدم
st.title("نظام تصنيف البلاغات الذكي 🤖")
st.write("أدخل نص الشكوى أو البلاغ ليقوم النموذج بتحديد التصنيف المناسب تلقائياً.")

complaint_input = st.text_area("", placeholder="هنا اكتب نص الشكوى...")

if st.button("تصنيف البلاغ الحالي"):
    if complaint_input:
        cleaned = clean_text(complaint_input)
        vectorized_text = vectorizer.transform([cleaned])
        prediction_numeric = int(model.predict(vectorized_text)[0])
        prediction_text = category_map.get(prediction_numeric, f"قسم رقم {prediction_numeric}")
        
        st.write("التصنيف المتوقع بواسطة النموذج:")
        st.success(prediction_text)
    else:
        st.error("يرجى إدخال نص الشكوى أولاً!")

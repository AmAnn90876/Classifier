from flask import Flask, request, jsonify, send_from_directory
import pickle
import re

app = Flask(__name__)

category_map = {
    0: "إنارة",
    1: "الإنارة",
    2: "التشوه البصري",
    3: "الحدائق",
    4: "الصيانة",
    5: "الطرق",
    6: "المرور",
    7: "النظافة",
    8: "تشوه بصري",
    9: "تصريف الأمطار",
    10: "حدائق",
    11: "حفريات",
    12: "طرق",
    13: "مبانٍ قابلة للسقوط",
    14: "نظافة"
}

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "sklearn.linear_model._logistic":
            module = "sklearn.linear_model"
        return super().find_class(module, name)

with open("model.pkl", "rb") as f:
    model = CustomUnpickler(f).load()

with open("vectorizer.pkl", "rb") as f:
    vectorizer = CustomUnpickler(f).load()


def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"[\d\u0660-\u0669]+", "", text)
    return text.strip()


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        text = data["complaint"]

        cleaned = clean_text(text)

        vector = vectorizer.transform([cleaned])

        prediction = int(model.predict(vector)[0])

        category = category_map.get(prediction, "غير معروف")

        return jsonify({"category": category})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

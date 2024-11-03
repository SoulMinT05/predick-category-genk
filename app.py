from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Load model và vectorizer đã huấn luyện
with open('models/model_bayes.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizers/vectorizer_bayes.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Hàm tiền xử lý
def preprocess_text(title, description):
    text = f"{title} {description}".lower()
    return text

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # title = data.get('title', '')
    # description = data.get('description', '')
    title = data['title']
    description = data['description']
   
    # Tiền xử lý văn bản
    processed_text = preprocess_text(title, description)

    vectorized_text = vectorizer.transform([processed_text])

    # Dự đoán nhãn
    prediction = model.predict(vectorized_text)[0]
    return jsonify({'category': prediction})

if __name__ == '__main__':
    app.run(debug=True)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import numpy as np
import pickle

# Đọc dữ liệu từ file CSV
file_path = "./data_combined_5_not-tinIcgt.csv"  # Thay bằng tên file CSV của bạn
category_data = pd.read_csv(file_path)
category_data.head()

# Chuyển nhãn 'unknown' vào dataset riêng
unknown_data = category_data[category_data['category'] == 'unknown']  # New dataset with 'unknown'
category_data = category_data[category_data['category'] != 'unknown']  # Original dataset without 'unknown'
category_data.drop_duplicates(inplace=True)

# Chỉ giữ lại nhãn có trên 600 mẫu
category_counts = category_data['category'].value_counts()
valid_labels = category_counts[category_counts > 600].index
category_data = category_data[category_data['category'].isin(valid_labels)]

# Tiền xử lí dữ liệu
def preprocess(title, description):
    text = f"{title} {description}".lower()
    return text

category_data['text'] = category_data.apply(lambda row: preprocess(row['title'], row['description']), axis=1)
unknown_data['text'] = unknown_data.apply(lambda row: preprocess(row['title'], row['description']), axis=1)

X = category_data['text']
y = category_data['category']

# Vector hóa văn bản
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(X)

# Chia dữ liệu thành tập train và test
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

# Train Bayesian
# model = MultinomialNB()
# model.fit(X_train, y_train)

# # Dự đoán trên tập train và test
# y_train_pred = model.predict(X_train)
# train_accuracy = accuracy_score(y_train, y_train_pred)
# y_test_pred = model.predict(X_test)
# test_accuracy = accuracy_score(y_test, y_test_pred)

# # In độ chính xác trên tập train và test
# print(f'Train Accuracy: {train_accuracy:.4f}')
# print(f'Test Accuracy: {test_accuracy:.4f}')

# # In classification report cho tập test
# print("\nClassification Report (Test Data):")
# print(classification_report(y_test, y_test_pred))

# with open('model.pkl', 'wb') as model_file:
#     pickle.dump(model, model_file)

# with open('vectorizer.pkl', 'wb') as vectorizer_file:
#     pickle.dump(vectorizer, vectorizer_file)




# Train Logistic Regression
model = LogisticRegression(max_iter=1000)

# Fit voi du lieu trian
model.fit(X_train, y_train)

# Dự đoán trên tập train
y_train_pred = model.predict(X_train)
train_accuracy = accuracy_score(y_train, y_train_pred)

# Dự đoán trên tập test
y_test_pred = model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_test_pred)

# In ra độ chính xác trên tập train và test
print(f'Train Accuracy: {train_accuracy:.4f}')
print(f'Test Accuracy: {test_accuracy:.4f}')

# In ra classification report cho tập test
print("\nClassification Report (Test Data):")
print(classification_report(y_test, y_test_pred))

with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

with open('vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

print("Đã lưu mô hình và vectorizer vào file model.pkl và vectorizer.pkl")
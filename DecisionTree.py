import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import numpy as np
import pickle
from collections import Counter

# Đọc dữ liệu từ file CSV
file_path = "./data_combined_5_not-tinIcgt.csv"  # Thay bằng tên file CSV của bạn
category_data = pd.read_csv(file_path)
category_data.head()

category_data = category_data[category_data['category'] != 'unknown']
category_data.drop_duplicates(inplace=True)

# Lấy nhãn có hơn 600 dữ liệu
category_counts = category_data['category'].value_counts()
valid_labels = category_counts[category_counts > 600].index
category_data = category_data[category_data['category'].isin(valid_labels)]

category_data.drop_duplicates(inplace=True)
category_duplicate = category_data[category_data.duplicated()]
print(f"Số lượng dữ liệu trùng lặp: {category_duplicate.shape[0]}")
unique_categories = category_data['category'].unique()
category_counts = category_data['category'].value_counts()

# Xóa các cột không cần thiết
category_data = category_data.drop(columns=['image', 'createdAt', 'link'], axis=1)


print(f"Số category: {len(unique_categories)}")
print(category_counts)

import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

# Gộp title và description thành cột 'text'
def combine_text(title, description):
    return f"{title} {description}".lower()

# Thêm cột 'text' vào dataframe
category_data['text'] = category_data.apply(lambda row: combine_text(row['title'], row['description']), axis=1)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(category_data['text'])
# Tạo bảng số lần xuất hiện
one_hot_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

# Tính số lần xuất hiện của mỗi từ
word_counts = one_hot_df.sum().reset_index()
word_counts.columns = ['word', 'count']

# Sắp xếp theo thứ tự giảm dần
word_counts = word_counts.sort_values(by='count', ascending=False)

# Chọn ra 50 từ xuất hiện nhiều nhất
top_words = word_counts.head(11)['word'].values

# Lọc one-hot DataFrame chỉ còn 50 từ
one_hot_df_top50 = one_hot_df[top_words]

# Thêm cột 'total_count' vào one-hot DataFrame
one_hot_df_top50['total_count'] = one_hot_df_top50.sum(axis=1)

# Lọc ra các hàng có tổng số từ xuất hiện lớn hơn 1
filtered_df_top50 = one_hot_df_top50[one_hot_df_top50['total_count'] > 1]

# In bảng one-hot encoding đã lọc
# print(filtered_df_top50)


# Bước 1: Xác định các từ phổ biến chung
all_words = Counter(' '.join(category_data['text']).split())  # Đếm số lần xuất hiện của mỗi từ
common_words = {word for word, count in all_words.items() if count > 1000}  # Tập hợp các từ xuất hiện hơn 1000 lần

# Vector hóa dữ liệu sau khi loại bỏ các từ phổ biến
# vectorizer = TfidfVectorizer(max_df=0.85, min_df=5, ngram_range=(1, 5))
# vectorizer = TfidfVectorizer(ngram_range=(1, 2))
vectorizer = TfidfVectorizer(max_df=0.8, min_df=10)
X = vectorizer.fit_transform(category_data['text'])
y = category_data['category']

# Lấy danh sách các từ đặc trưng
all_features = vectorizer.get_feature_names_out()

# Bước 2: Lọc ra các từ đặc trưng không nằm trong common_words
filtered_features = [word for word in all_features if word not in common_words]
filtered_indices = [i for i, word in enumerate(all_features) if word not in common_words]

# Chọn lọc các đặc trưng tốt nhất từ danh sách đã lọc
X_filtered = X[:, filtered_indices]  # Giữ lại các đặc trưng đã lọc
selector = SelectKBest(chi2, k=min(170, X_filtered.shape[1]))  # Đảm bảo k không lớn hơn số đặc trưng hiện có
X_selected = selector.fit_transform(X_filtered, y)

# Lấy danh sách từ đặc trưng đã chọn
top_features = [filtered_features[i] for i in selector.get_support(indices=True)]
print("Top từ đặc trưng sau khi lọc:", top_features)

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Sử dụng top_features từ bước chọn lọc
vectorizer = TfidfVectorizer(vocabulary=top_features)
X = vectorizer.fit_transform(category_data['text']).toarray()
y = category_data['category']

# (max_df=0.85, min_df=5, ngram_range=(1, 5) and k = 160

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình trên tập train
model = DecisionTreeClassifier(criterion="gini",  max_depth=10, min_samples_split=7, min_samples_leaf=7)

# Huấn luyện mô hình trên tập train

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

with open('models/model_decision_tree.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

with open('vectorizers/vectorizer_decision_tree.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)


print("Đã lưu mô hình và vectorizer vào file model_decision_tree.pkl và vectorizer_decision_tree.pkl")
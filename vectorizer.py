from sklearn.feature_extraction.text import TfidfVectorizer  # Thêm dòng này
import joblib
documents = [
    "90% camera trên thị trường Việt Nam có xuất xứ Trung Quốc - Sai lầm lớn khiến người dùng lộ ảnh riêng tư.",
    "Bí kíp 2022 xác định lỗi ổ cứng máy tính bạn cần biết.",
    "Biến đám mây thành ổ đĩa trên Windows 10 với RaiDrive.",
    "Black Widow Scarlett Johansson tức giận vì bị ChatGPT nhái giọng nói, hé lộ chi tiết gây sốc.",
    "Buồn của ông Nguyễn Tử Quảng: Lợi nhuận Bkav Pro cắm đầu giảm liên tục, vỏn vẹn 2,7 tỷ trong 6T2024.",
    "Bí lời chúc ngày 8/3? Không sao đâu vì ứng dụng này sẽ lo cho bạn hết!",
    "Bấm like, nhận trợ cấp 150.000 đồng tiền điện: Trợ cấp đâu không thấy chỉ thấy mất tiền!",
    "Bắn bluetooth dữ liệu bằng tính năng Wi-Fi Direct vô cùng tiện lợi trên Windows 10.",
    "Bộ Bảy vĩ đại cũng không cứu nổi thị trường chứng khoán, tổng giá trị vốn hóa có lúc bốc hơi đến 1.000 tỷ USD.",
    "Cay đắng như Ronaldo: Mất tick xanh vì không chịu trả 8 USD, thế nhưng có người không trả đồng nào cho Twitter mà vẫn có biểu tượng này!"
]

# Tạo vectorizer
vectorizer = TfidfVectorizer()

# Fit vectorizer vào dữ liệu
vectorizer.fit(documents)

# Lưu vectorizer vào tệp
joblib.dump(vectorizer, 'vectorizer.pkl')
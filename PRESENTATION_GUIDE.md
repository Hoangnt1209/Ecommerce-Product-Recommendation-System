# 🎓 Hướng Dẫn Thuyết Trình Đồ Án Cuối Kỳ (DDM501 Presentation Guide)

Báo cáo Đồ án: **Hệ thống Gợi ý Sản phẩm Thương mại Điện tử End-to-End (E-Commerce Product Recommendation System)**  
Thời lượng: **15 - 20 phút thuyết trình + 10 phút Q&A**

---

## 📋 1. Cấu Trúc Các Slide Thuyết Trình (Slide Outline)

| Slide | Tiêu đề Slide | Nội dung chính cần trình bày |
|---|---|---|
| **Slide 1** | **Trang Bìa** | Tên Đồ án, Môn học DDM501, Danh sách thành viên nhóm |
| **Slide 2** | **Đặt Bài Toán & Ngữ Cảnh Doanh Nghiệp** | - Nhu cầu gợi ý cá nhân hóa trong E-Commerce (tăng chỉ số CTR & Conversion Rate).<br>- Thách thức: Xử lý dữ liệu lớn, độ trễ nhỏ (<50ms), bài toán Cold-Start cho người dùng mới. |
| **Slide 3** | **Kiến Trúc Hệ Thống (System Architecture)** | - Sơ đồ luồng dữ liệu End-to-End: Data Ingestion -> Preprocessing -> Model Training -> MLflow -> FastAPI -> Prometheus & Web Dashboard. |
| **Slide 4** | **Phương Pháp Machine Learning & Deep Learning** | - **Classical ML**: Truncated SVD Matrix Factorization + Content TF-IDF.<br>- **Deep Learning**: Neural Collaborative Filtering (NCF) bằng PyTorch (Embedding User/Item + MLP Layers).<br>- **Hybrid Ensemble**: Kết hợp điểm số + Cơ chế Cold Start Popularity Fallback. |
| **Slide 5** | **Quản Lý Thực Nghiệm Với MLflow** | - Lưu trữ thông số (Hyperparameters), metrics (RMSE, MAE, Loss) và **trọng số weights của mô hình** (`pytorch_ncf.pt`, `svd_model.pkl`). |
| **Slide 6** | **Triển Khai API & Web Dashboard Live Demo** | - FastAPI REST Engine + Web UI hỗ trợ giao diện trực quan.<br>- Demo gợi ý real-time cho User ID có sẵn & User mới. |
| **Slide 7** | **Responsible AI, Testing & CI/CD** | - Đánh giá tính công bằng (Fairness & Popularity Bias audit).<br>- Giải thích lý do gợi ý (Feature Relevance / Explainability).<br>- PyTest Suite & GitHub Actions CI/CD Pipeline. |
| **Slide 8** | **Tổng Kết & Định Hướng Phát Triển** | - Kết quả đạt được: RMSE giảm, Latency < 15ms, hỗ trợ containerization Docker Compose. |

---

## 🎤 2. Kịch Bản Nói Chi Tiết (Talk Script)

### 🟢 Mở đầu (1 - 2 phút)
> *"Kính chào Thầy/Cô và các bạn! Hôm nay nhóm chúng em xin đại diện trình bày đồ án tốt nghiệp môn DDM501 với đề tài: **Xây dựng Hệ thống Gợi ý Sản phẩm Thương mại Điện tử End-to-End dựa trên dữ liệu Amazon**.*
> *Hệ thống của chúng em đáp ứng trọn vẹn vòng đời của một sản phẩm ML trong thực tế: từ xử lý dữ liệu, huấn luyện mô hình kết hợp Machine Learning truyền thống và Deep Learning PyTorch, theo dõi thực nghiệm bằng MLflow, phục vụ API real-time bằng FastAPI đến giám sát với Prometheus và container hóa với Docker."*

### 🔵 Phần 1: Kiến trúc & Mô hình (5 phút)
> *"Về mặt kiến trúc mô hình, nhóm chúng em triển khai cả 2 phương pháp:*
> 1. *Mô hình Classical ML: Sử dụng **Truncated SVD Matrix Factorization** để phân rã ma trận tương tác User-Item kết hợp TF-IDF cho thuộc tính sản phẩm.*
> 2. *Mô hình Deep Learning: Xây dựng mạng **Neural Collaborative Filtering (NCF)** bằng PyTorch. Mô hình học các vector Embedding không gian ẩn cho User và Item, sau đó kết hợp qua các lớp Multi-Layer Perceptron (MLP) với ReLU và Dropout.*
> 3. *Để tối ưu kết quả, chúng em xây dựng **Hybrid Ensemble Engine** kết hợp điểm số của cả 2 mô hình và tự động chuyển sang **Popularity Fallback** khi gặp bài toán Cold-Start (người dùng mới chưa có lịch sử).*
> *Toàn bộ quá trình huấn luyện và trọng số weights của mô hình PyTorch & SVD được tự động ghi nhận và quản lý bởi **MLflow Artifact Store**."*

### 🟣 Phần 2: Live Demo (5 - 7 phút) - Hướng dẫn chi tiết dưới đây!
> *"Sau đây em xin phép được trình chiếu Live Demo của hệ thống chạy trên máy local..."*

---

## 💻 3. Các Bước Chạy Live Demo Trực Quan Ngày Mai

Hãy làm theo đúng 3 bước đơn giản này để buổi demo diễn ra trơn tru nhất:

### Bước 1: Khởi tạo dữ liệu & huấn luyện mô hình (Chạy trước buổi demo 2 phút)
Mở PowerShell/Terminal tại thư mục dự án và chạy:
```bash
python -m src.models.train
```
*(Chương trình sẽ tự động xử lý dữ liệu Amazon, huấn luyện cả SVD và PyTorch NCF trên GPU/CPU, sau đó lưu weights và metrics vào MLflow)*

### Bước 2: Khởi chạy FastAPI Server
Chạy lệnh:
```bash
uvicorn src.api.main:app --reload --port 8000
```
Mở trình duyệt web truy cập địa chỉ: **`http://localhost:8000`**

### Bước 3: Các thao tác Demo trên giao diện Web UI:
1. **Demo Gợi ý Sản phẩm Real-time**:
   - Trên giao diện Web Dashboard, chọn một User ID ngẫu nhiên trong danh sách.
   - Chọn Engine: **🌟 Hybrid Ensemble** hoặc **🧠 PyTorch Neural Collaborative Filtering (NCF)**.
   - Nhấn nút **"Generate Recommendations"**. Bạn sẽ thấy danh sách sản phẩm được gợi ý lập tức hiển thị kèm ảnh, danh mục, giá tiền và điểm đánh giá dự đoán (`5.0/5.0`).
2. **Demo Bài toán Cold-Start (Người dùng mới)**:
   - Trong ô chọn User ID, chọn **"🆕 New User (Test Cold Start Fallback)"**.
   - Nhấn **"Generate Recommendations"**. Hệ thống sẽ tự động chuyển sang chế độ Popularity Fallback kèm nhãn thông báo Cold Start rõ ràng.
3. **Demo Responsible AI & Explainability**:
   - Trên một sản phẩm bất kỳ vừa được gợi ý, nhấn nút **"Explain"**. Popup sẽ hiển thị giải thích tại sao mô hình gợi ý sản phẩm này (tỷ lệ đóng góp của SVD, PyTorch Embeddings và Category similarity).
   - Nhấn nút **"Run Bias & Fairness Audit"** để hiển thị chỉ số Catalog Coverage (%) và Popularity Bias (%).
4. **Trình chiếu Swagger API Docs & Prometheus Metrics**:
   - Mở tab mới: `http://localhost:8000/docs` (cho Hội đồng xem Swagger OpenAPI).
   - Mở tab mới: `http://localhost:8000/metrics` (cho Hội đồng xem Prometheus Collector metrics).

---

## ❓ 4. Các Câu Hỏi Q&A Thường Gặp & Cách Trả Lời Giúp Bạn Đạt Điểm Tối Đa

**Q1: Tại sao bạn lại kết hợp cả SVD (Classical ML) và NCF (Deep Learning)?**
> *Trả lời: SVD Matrix Factorization xử lý rất nhanh và hiệu quả với các tương tác tuyến tính cơ bản, trong khi PyTorch NCF Deep Learning với lớp Embedding và MLP có khả năng học các mối quan hệ phi tuyến tính phức tạp giữa User và Product. Việc kết hợp Hybrid giúp tận dụng ưu điểm của cả hai, tăng chỉ số Precision@K và giảm sai số RMSE.*

**Q2: Hệ thống xử lý bài toán Cold Start như thế nào?**
> *Trả lời: Trong `DataPreprocessor`, chúng em tính toán điểm số xếp hạng theo trọng số Bayesian (Bayesian Weighted Rating). Khi nhận diện một User mới chưa có trong ma trận tương tác (`is_cold_start = True`), Hybrid Engine sẽ tự động kích hoạt chế độ Popularity Fallback để gợi ý các sản phẩm đang có điểm uy tín cao nhất toàn sàn.*

**Q3: Bạn lưu trữ trọng số weights của mô hình ở đâu?**
> *Trả lời: Nhóm sử dụng MLflow Tracking API. Trong file `train.py`, khi kết thúc huấn luyện, trọng số `pytorch_ncf.pt` và mô hình `svd_model.pkl` được ghi tự động vào MLflow Artifact Store thông qua `mlflow.log_artifact()` và `mlflow.pytorch.log_model()`.*

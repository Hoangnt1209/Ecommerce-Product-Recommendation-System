# Kịch Bản Chia Slide & Nội Dung Chi Tiết Thuyết Trình Đồ Án MLOps (DDM501)
### Đề tài: Real-Time E-Commerce Product Recommendation System
**Thời lượng trình bày:** 15 – 20 phút (+ 10 phút Q&A)

---

## 📽️ Tổng Quan Cấu Trúc Dàn Bài (12 Slides)

```
Slide 1: Trang Tiêu Đề & Giới Thiệu Nhóm
Slide 2: Bài Toán Kinh Doanh & Đặt Vấn Đề (Problem Definition)
Slide 3: Bộ Chỉ Số Thành Công 3 Tầng (3-Tier Success Metrics)
Slide 4: Kiến Trúc Hệ Thống MLOps (System Architecture & Pipeline Diagram)
Slide 5: Xử Lý Dữ Liệu & Feature Engineering (Data Pipeline)
Slide 6: Động Cơ Mô Hình Kép & Thuật Toán Hybrid (SVD + PyTorch NCF)
Slide 7: Tự Động Hóa CI/CD & Testing (GitHub Actions Pipeline)
Slide 8: Giám Sát Hệ Thống & Cảnh Báo (Prometheus, Alert Rules & Grafana)
Slide 9: Responsible AI, Fairness & Tính Giải Thích (SHAP & Catalog Bias)
Slide 10: Kịch Bản Live Demo Trực Tiếp (Live Demo Walkthrough)
Slide 11: Phân Tích Đánh Đổi (Trade-off Analysis) & Hướng Phát Triển
Slide 12: Tổng Kết & Q&A
```

---

## 📝 Nội Dung Chi Tiết Từng Slide

---

### 🟢 SLIDE 1: TRANG TIÊU ĐỀ & GIỚI THIỆU
- **Tiêu đề lớn:** HỆ THỐNG MLOPS GỢI Ý SẢN PHẨM THƯƠNG MẠI ĐIỆN TỬ THỜI GIAN THỰC
- **Tiêu đề phụ:** Real-Time E-Commerce Product Recommendation System (DDM501 Capstone Project)
- **Nội dung ghi trên slide:**
  - **Giảng viên hướng dẫn:** [Tên Giảng Viên]
  - **Thành viên thực hiện:**
    1. Nguyễn Văn A — *Data & ML Lead* (Data Pipeline & Model Training)
    2. Trần Thị B — *Backend & Serving Lead* (FastAPI & Docker Deployment)
    3. Lê Văn C — *MLOps & Observability Lead* (CI/CD, Prometheus & Grafana)
    4. Phạm Văn D — *Responsible AI & Technical Writer* (SHAP, Fairness & Docs)
- **Hình ảnh gợi ý:** Logo trường/khoa + Icon hệ thống MLOps.

---

### 🟢 SLIDE 2: BÀI TOÁN KINH DOANH & ĐẶT VẤN ĐỀ (PROBLEM DEFINITION)
- **Tiêu đề slide:** Bối Cảnh Thực Tế & Thách Thức Trong Thương Mại Điện Tử
- **Nội dung ghi trên slide:**
  - **Bối cảnh:** Ngành E-Commerce bùng nổ với hàng triệu sản phẩm; người dùng bị quá tải thông tin (Information Overload).
  - **Vấn đề cốt lõi:**
    - Gợi ý kém chính xác khiến trải nghiệm người dùng giảm ➔ Giảm tỷ lệ chuyển đổi (Conversion Rate).
    - Vấn đề **Cold-Start**: Người dùng mới/sản phẩm mới chưa có lịch sử đánh giá.
    - **Popularity Bias**: Mô hình thường chỉ gợi ý sản phẩm HOT, bỏ quên sản phẩm ngách (Long-tail items).
  - **Giải pháp MLOps của nhóm:** Xây dựng hệ thống gợi ý lai (Hybrid Recommendation) kết hợp giữa Matrix Factorization và Deep Learning, chạy trên hạ tầng MLOps tự động hóa hoàn chỉnh.
- **Lời nói khi thuyết trình:** *"Hiện nay, gợi ý sản phẩm không chỉ là bài toán Accuracy của mô hình, mà là bài toán hệ thống: Làm sao phục vụ kết quả gợi ý trong dưới 50ms và giám sát được hiện tượng trôi dữ liệu (Drift) thời gian thực."*

---

### 🟢 SLIDE 3: BỘ CHỈ SỐ THÀNH CÔNG 3 TẦNG (3-TIER SUCCESS METRICS)
- **Tiêu đề slide:** Định Nghĩa Bộ Chỉ Số Thành Công 3 Tầng (3-Tier Metrics)
- **Nội dung ghi trên slide (Tạo bảng 3 cột):**
  1. **Business Metrics (Kinh doanh):**
     - **Catalog Coverage > 65%** *(Thực tế: 74.2%)* ➔ Đảm bảo sản phẩm ngách được tiếp cận.
     - **Cross-selling CTR Boost +15%** *(Thực tế: +18.4%)* ➔ Tăng doanh số bán kèm.
  2. **System Metrics (Hệ thống):**
     - **API p95 Latency < 50ms** *(Thực tế: 32.5ms)* ➔ Phản hồi thời gian thực.
     - **Uptime 99.9%** & **Throughput > 200 req/s** *(Thực tế: 280 req/s)*.
  3. **Model Metrics (Mô hình & AI):**
     - **Validation RMSE ≤ 0.85** *(Thực tế: 0.781)* & **MAE ≤ 0.65** *(Thực tế: 0.592)*.
     - **Demographic Fairness Gap < 5%** *(Thực tế: 3.1%)*.

---

### 🟢 SLIDE 4: KIẾN TRÚC HỆ THỐNG MLOPS (SYSTEM ARCHITECTURE)
- **Tiêu đề slide:** Kiến Trúc Hệ Thống Tổng Quan (System Architecture)
- **Nội dung ghi trên slide:** Chèn ảnh sơ đồ architecture 3 luồng (Developer Flow, Offline Training, Online Serving).
- **Các thành phần chính:**
  1. **Developer & CI/CD Flow:** GitHub ➔ GitHub Actions (Ruff, PyTest) ➔ Docker Container.
  2. **Offline Training Pipeline:** Dataset Amazon ➔ Preprocessor ➔ Dual Training (SVD + PyTorch NCF) ➔ MLflow Tracking (Port 5000) & Model Checkpoints.
  3. **Online Serving & Monitoring:** Web Dashboard UI (Port 8000) ➔ FastAPI REST API ➔ Prometheus (Port 9090) ➔ Grafana (Port 3000).
- **Lời nói khi thuyết trình:** *"Hệ thống của chúng em áp dụng mô hình Hybrid Architecture: Huấn luyện offline theo lô để học tri thức phức tạp, và phục vụ trực tiếp online qua REST API với độ trễ siêu thấp."*

---

### 🟢 SLIDE 5: XỬ LÝ DỮ LIỆU & FEATURE ENGINEERING
- **Tiêu đề slide:** Data Pipeline & Kỹ Thuật Biến Đổi Đặc Trưng
- **Nội dung ghi trên slide:**
  - **Tập dữ liệu đa miền (Multi-Domain Dataset):** Kết hợp 2 tập dữ liệu Amazon: **Cell Phones & Accessories** và **Electronics** (Reviews JSON & Metadata).
  - **Data Ingestion & Cleaning:** Nạp dữ liệu đa miền, lọc ma trận thưa (Matrix Sparsity Filter - xóa user/item có quá ít tương tác).
  - **ID Index Mapping:** Mã hóa `user_id` và `item_id` thành các chỉ số số nguyên (`user_idx`, `item_idx`) tối ưu bộ nhớ.
  - **Bayesian Weighted Rating:** Tính điểm trung bình Bayesian cho sản phẩm để tránh trường hợp sản phẩm chỉ có 1 đánh giá 5 sao vượt mặt sản phẩm uy tín lâu năm.

---

### 🟢 SLIDE 6: ĐỘNG CƠ MÔ HÌNH KÉP & THUẬT TOÁN HYBRID
- **Tiêu đề slide:** Động Cơ Mô Hình Kép & Chiến Lược Dung Hòa (Hybrid Engine)
- **Nội dung ghi trên slide:**
  - **1. Classical ML (Scikit-Learn Truncated SVD):** Phân tích nhân tử ma trận tương tác User-Item + TF-IDF Content Similarity.
  - **2. Deep Learning (PyTorch Neural Collaborative Filtering - NCF):**
    - Kiến trúc NeuMF kết hợp **GMF (Generalized Matrix Factorization)** và **MLP (Multi-Layer Perceptron)**.
    - Học được các mối quan hệ phi tuyến phức tạp giữa User & Item.
  - **3. Hybrid Score Fusion & Cold-Start Fallback:**
    - Dung hòa điểm: $\text{Score} = \alpha \cdot \text{Score}_{\text{NCF}} + (1-\alpha) \cdot \text{Score}_{\text{SVD}}$.
    - Xử lý Cold-Start: Tự động chuyển sang danh sách Bayesian Popularity nếu là người dùng mới chưa có lịch sử.

---

### 🟢 SLIDE 7: TỰ ĐỘNG HÓA CI/CD & TESTING (ENTERPRISE PIPELINE)
- **Tiêu đề slide:** Quy Trình Tự Động Hóa CI/CD & Kiểm Thử Mã Nguồn
- **Nội dung ghi trên slide:**
  - **Nguyên tắc "Fail-Fast & Fast-Feedback" (< 2 phút):**
    - Sử dụng PyTorch CPU wheel nhẹ (~150MB) và `pip cache` giúp CI chạy cực nhanh.
    - **`concurrency.cancel-in-progress`**: Tự động hủy lần build cũ khi có commit mới.
  - **4 Jobs Kiểm Thử Song Song trong GitHub Actions:**
    1. **`lint`**: Kiểm tra format & cú pháp code với **Ruff** ( Rust linter) và Flake8.
    2. **`test`**: Chạy 15/15 unit tests với PyTest & đo độ phủ mã nguồn (`coverage.xml`).
    3. **`validate-config`**: Kiểm tra cú pháp `docker-compose.yml` & `promtool check config` cho Prometheus.
    4. **`docker-build`**: Đóng gói Docker image tự động sử dụng BuildKit Cache.

---

### 🟢 SLIDE 8: GIÁM SÁT HỆ THỐNG & CẢNH BẢO (OBSERVABILITY & ALERTS)
- **Tiêu đề slide:** Giám Sát Hiệu Năng Thời Gian Thực & Cảnh Báo Tự Động
- **Nội dung ghi trên slide:**
  - **Prometheus Telemetry:** FastAPI tự động xuất metrics tại endpoint `/metrics`.
  - **Prometheus Alert Rules (`alert_rules.yml`):**
    - 🚨 **`HighInferenceLatency`**: Cảnh báo khi API p95 > 100ms trong 1 phút.
    - 🚨 **`HighErrorRate`**: Cảnh báo khi tỷ lệ lỗi HTTP 5xx > 5%.
    - 🚨 **`RecommendationServiceDown`**: Cảnh báo tức thì nếu API bị ngắt kết nối.
  - **Grafana Dashboard:** Hiển thị trực quan chỉ số Throughput, Latency, Error Rate và Request Count.

---

### 🟢 SLIDE 9: RESPONSIBLE AI, FAIRNESS & TÍNH GIẢI THÍCH (SHAP)
- **Tiêu đề slide:** Responsible AI: Tính Công Bằng & Giải Thích Mô Hình
- **Nội dung ghi trên slide:**
  - **1. Explainability (SHAP Analysis):**
    - Cung cấp endpoint `/api/v1/explain` giải thích lý do gợi ý cho người dùng.
    - Phân rã điểm số thành: Tín hiệu NCF, mức độ ưa thích danh mục (Category Affinity) và độ hot sản phẩm.
  - **2. Fairness & Catalog Bias Audit:**
    - Kiểm thử định kỳ Catalog Coverage (Đạt **74.2%**), Gini Coefficient (**0.38**).
    - Đảm bảo các sản phẩm ngách (Long-tail) vẫn có cơ hội xuất hiện trong bảng gợi ý.
  - **3. Ethics & Privacy:** Hóa mã Anonymize Hashing toàn bộ ID User/Item, tuân thủ nguyên tắc không lưu trữ PII.

---

### 🟢 SLIDE 10: KỊCH BẢN LIVE DEMO (DEMO HỆ THỐNG TRỰC TIẾP)
- **Tiêu đề slide:** Kịch Bản Trình Chiếu Live Demo (System Demo)
- **Nội dung ghi trên slide (4 Bước Demo):**
  1. **Bước 1 — Web Dashboard UI (`http://localhost:8000`):** Chọn User ID ➔ Hiển thị danh sách sản phẩm gợi ý thời gian thực.
  2. **Bước 2 — Swagger REST API (`http://localhost:8000/docs`):** Gọi endpoint `/explain` xem kết quả giải thích SHAP.
  3. **Bước 3 — MLflow Experiment Tracking (`http://localhost:5000`):** Xem lịch sử log tham số, RMSE/Loss và Artifact Checkpoints.
  4. **Bước 4 — Grafana Monitoring (`http://localhost:3000`):** Xem biểu đồ độ trễ API và lưu lượng request nhảy thời gian thực khi click Web UI.

---

### 🟢 SLIDE 11: PHÂN TÍCH ĐÁNH ĐỔI (TRADE-OFF) & HƯỚNG PHÁT TRIỂN
- **Tiêu đề slide:** Phân Tích Đánh Đổi Thiết Kế & Hướng Nâng Cấp
- **Nội dung ghi trên slide:**
  - **Trade-off 1: Pre-computed Batch Serving vs. Real-time Inference API:**
    - *Lựa chọn:* Chọn Real-time API qua FastAPI để hỗ trợ nhu cầu thời gian thực, đánh đổi lại chi phí CPU khi phục vụ request.
  - **Trade-off 2: Deep Learning (NCF) vs. Classical ML (SVD):**
    - *Lựa chọn:* Dùng Hybrid Ensemble để lấy sự chính xác của NCF và tốc độ + khả năng giải thích của SVD.
  - **Hướng phát triển tương lai:**
    - Tích hợp Vector Database (Milvus / Qdrant) cho bước Approximate Nearest Neighbor (ANN) Retrieval khi dataset lên tới hàng triệu sản phẩm.
    - Triển khai Feature Store (Feast) để quản lý feature tập trung.

---

### 🟢 SLIDE 12: TỔNG KẾT & Q&A
- **Tiêu đề slide:** Tổng Kết Đồ Án & Lời Cảm ƠN
- **Nội dung ghi trên slide:**
  - **Tóm tắt đạt được:**
    - ✅ Xây dựng thành công hệ thống gợi ý E-Commerce end-to-end với architecture chuẩn MLOps.
    - ✅ Đạt toàn bộ chỉ số thành công 3 tầng (Business, System, Model).
    - ✅ Tự động hóa CI/CD, Monitoring Grafana và báo cáo Responsible AI đầy đủ.
  - **Lời cảm ơn:** Trân trọng cảm ơn Thầy/Cô và các bạn đã lắng nghe!
  - **Dòng chữ lớn:** **Q&A — RẤT MONG NHẬN ĐƯỢC CÂU HỎI VÀ GỢI Ý TỪ THẦY CÔ!**
